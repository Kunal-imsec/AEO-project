"""
response_parser.py
------------------
AEO Diagnostic Tool — Phase 3 (v2)

Parses the raw LLM responses returned by query_all_llms() to calculate
per-engine brand mention rates, visibility ranks, a list of likely
competitor brand names, and dynamic actionable tips.

Key fix (v2):
  - Category-aware brand matching replaces the old heuristic regex that
    was surfacing common English adjectives ("Known", "Based", "Strong").
  - Tips are now fully dynamic — personalised per rank and competitor list.
"""

import re
from collections import Counter


# ---------------------------------------------------------------------------
# Known brand lists, keyed by category
# ---------------------------------------------------------------------------

KNOWN_BRANDS: dict[str, list[str]] = {
    "electronics": [
        "Sony", "Samsung", "Apple", "Bose", "JBL", "Jabra",
        "Sennheiser", "Anker", "Beats", "LG", "Philips",
        "Skullcandy", "Bang & Olufsen", "1More", "Shure",
    ],
    "supplement": [
        "Nature Made", "Garden of Life", "NOW Foods", "Thorne",
        "Pure Encapsulations", "Solgar", "Life Extension",
        "Jarrow", "Nordic Naturals", "Designs for Health",
    ],
    "skincare": [
        "CeraVe", "Neutrogena", "La Roche-Posay", "Cetaphil",
        "Olay", "The Ordinary", "Paula's Choice", "Aveeno",
    ],
    "default": [],
}

# Words that look capitalized but are never brand names — used only in the
# fuzzy fallback path (when no category list matches).
_FUZZY_STOPLIST: set[str] = {
    "Strong", "Based", "Known", "These", "Their", "Which", "While",
    "There", "About", "Great", "Good", "Best", "High", "With",
    "When", "This", "That", "From", "Your", "Some", "Also",
    "Here", "They", "Have", "More", "Most", "Many", "Very",
    # pre-existing stop-words kept for safety
    "Note", "Each", "Both", "However", "Overall", "Additionally", "Often",
    "Pure", "Natural", "Available", "Provides", "Recommended", "Helps",
    "Comes", "Amazon", "Other", "Another", "Third", "Second", "First",
    "Options", "Option", "Products", "Product", "Brand", "Brands",
    "Supplement", "Supplements", "Magnesium", "Vitamin", "Mineral",
    "Formula", "Quality", "Value", "Dose", "Daily",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _safe_responses(responses: list) -> list[str]:
    """
    Convert the raw response list to plain strings, discarding error dicts.
    query_all_llms() may return dicts with an 'error' key on failure.
    """
    clean = []
    for r in responses:
        if isinstance(r, str):
            clean.append(r)
        # else: skip error dicts silently
    return clean


def _detect_category_key(category: str) -> str:
    """
    Map a free-text category string to one of the KNOWN_BRANDS keys.
    Returns "default" when no known category matches.
    """
    cat = category.lower()
    if any(kw in cat for kw in ("electronic", "earbud", "headphone")):
        return "electronics"
    if any(kw in cat for kw in ("supplement", "vitamin", "magnesium")):
        return "supplement"
    if any(kw in cat for kw in ("skin", "cream", "moisturizer")):
        return "skincare"
    return "default"


def _extract_competitors(
    responses: list[str],
    brand_name: str,
    category: str,
) -> list[str]:
    """
    Category-aware competitor extractor.

    Strategy
    --------
    • If a known brand list exists for the detected category, scan the
      combined response text for each brand from that list and tally hits.
    • Otherwise fall back to a conservative heuristic: capitalised words
      longer than 5 characters that are not in the fuzzy stoplist.

    Returns up to 3 competitor names (sorted by frequency), excluding the
    user's own brand.
    """
    brand_lower = brand_name.lower()
    combined_text = " ".join(responses)
    cat_key = _detect_category_key(category)
    brand_list = KNOWN_BRANDS[cat_key]

    # ------------------------------------------------------------------
    # Path A — category list is available: exact string matching
    # ------------------------------------------------------------------
    if brand_list:
        counts: Counter = Counter()
        for brand in brand_list:
            # Exclude the user's own brand and any brand whose name contains it
            # e.g. brand_name="Realme" → also excludes "Realme Narzo 60 Pro"
            if brand_lower in brand.lower() or brand.lower() in brand_lower:
                continue
            # Case-insensitive whole-phrase search
            hits = len(re.findall(re.escape(brand), combined_text, re.IGNORECASE))
            if hits > 0:
                counts[brand] = hits
        top = [name for name, _ in counts.most_common(3)]
        return top

    # ------------------------------------------------------------------
    # Path B — no category list: conservative heuristic fallback
    # Only accept tokens that are:
    #   • capitalised
    #   • longer than 5 characters
    #   • not in the fuzzy stoplist
    #   • not the user's brand
    # ------------------------------------------------------------------
    pattern = re.compile(r'\b([A-Z][a-zA-Z]{5,})\b')
    candidates: list[str] = []

    for match in pattern.finditer(combined_text):
        token = match.group(0)
        # Exclude any token that contains the brand name or is contained by it
        if brand_lower in token.lower() or token.lower() in brand_lower:
            continue
        if token in _FUZZY_STOPLIST:
            continue
        candidates.append(token)

    freq = Counter(candidates)
    top_fallback = [name for name, count in freq.most_common() if count >= 2]
    return top_fallback[:3]


def _rank(mention_rate: float) -> str:
    if mention_rate >= 0.6:
        return "high"
    if mention_rate >= 0.2:
        return "medium"
    return "low"


def _build_tip(rank: str, competitors: list[str], category: str) -> str:
    """
    Generate a dynamic, context-aware actionable tip.

    Args:
        rank:        "high" | "medium" | "low"
        competitors: top competitors for this engine (may be empty)
        category:    free-text product category string

    Returns:
        A single actionable tip string.
    """
    if rank == "high" and len(competitors) > 0:
        return (
            f"Strong visibility! But {competitors[0]} is also frequently "
            f"recommended — highlight what makes you unique."
        )
    elif rank == "high" and len(competitors) == 0:
        return (
            "Excellent AI visibility with no dominant competitor — "
            "keep your listing fresh and keyword-rich."
        )
    elif rank == "medium":
        return (
            f"Mentioned sometimes. Add more {category}-specific keywords "
            f"and customer benefit language to your listing."
        )
    else:  # low
        return (
            f"Not recognized by this AI engine. Your listing likely lacks "
            f"the terminology AI models associate with {category}. "
            f"Add detailed specs and use-case descriptions."
        )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def parse_responses(
    llm_responses: dict,
    brand_name: str,
    category: str,
) -> dict:
    """
    Parse brand visibility and competitor data from raw LLM response dicts.

    Args:
        llm_responses: {"openai": [...], "claude": [...], "gemini": [...]}
                       Each list contains 5 strings (or error dicts) from
                       query_all_llms().
        brand_name:    The brand whose visibility is being measured
                       (e.g. "MagPure").
        category:      Free-text product category (e.g. "magnesium supplement",
                       "wireless earbuds", "face moisturizer").

    Returns:
        {
            "openai": {
                "mention_count": int,       # how many of 5 responses mention brand
                "mention_rate":  float,     # mention_count / 5
                "rank":          str,       # "high" | "medium" | "low"
                "competitors":   list[str], # up to 3 competitor names
                "tip":           str,       # dynamic actionable tip
            },
            "claude":  { ... },
            "gemini":  { ... },
        }
    """
    brand_lower = brand_name.lower()
    result: dict = {}

    for engine in ("openai", "claude", "gemini"):
        raw = llm_responses.get(engine, [])
        responses = _safe_responses(raw)

        # Count how many responses contain the brand name
        mention_count = sum(
            1 for resp in responses if brand_lower in resp.lower()
        )

        # Use 5 as the expected denominator regardless of how many responses
        # survived error-filtering (keeps the rate stable against transient errors)
        total = 5
        mention_rate = round(mention_count / total, 4)
        rank = _rank(mention_rate)
        competitors = _extract_competitors(responses, brand_name, category)
        tip = _build_tip(rank, competitors, category)

        result[engine] = {
            "mention_count": mention_count,
            "mention_rate": mention_rate,
            "rank": rank,
            "competitors": competitors,
            "tip": tip,
        }

    return result


# ---------------------------------------------------------------------------
# Quick smoke-test  (run directly: python response_parser.py)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    _SAMPLE_RESPONSES = {
        "openai": [
            "I recommend MagPure for its high absorption. Nature Made and Doctor's Best are also popular.",
            "MagPure is excellent. Alternatives include Nature Made Magnesium and Thorne.",
            "Top picks: MagPure, Doctor's Best, and Pure Encapsulations.",
            "Nature Made and Doctor's Best dominate this space.",
            "Consider MagPure or Thorne for high-quality magnesium.",
        ],
        "claude": [
            "MagPure stands out for seniors. Doctor's Best is another strong choice.",
            "Try Nature Made or MagPure — both well-reviewed.",
            "Doctor's Best Magnesium is widely recommended.",
            "Pure Encapsulations and Thorne are premium options.",
            "MagPure offers great bioavailability. Nature Made is budget-friendly.",
        ],
        "gemini": [
            "Doctor's Best and Nature Made are popular. MagPure is newer.",
            "Thorne and Pure Encapsulations lead the premium segment.",
            "Nature Made Magnesium is widely available and affordable.",
            "MagPure, Doctor's Best, and Thorne are my top three.",
            "For seniors, MagPure and Nature Made are ideal.",
        ],
    }

    import json
    parsed = parse_responses(
        _SAMPLE_RESPONSES,
        brand_name="MagPure",
        category="magnesium supplement",
    )
    print(json.dumps(parsed, indent=2))
