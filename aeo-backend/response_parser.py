"""
response_parser.py
------------------
AEO Diagnostic Tool — Phase 3

Parses the raw LLM responses returned by query_all_llms() to calculate
per-engine brand mention rates, visibility ranks, and a list of likely
competitor brand names.
"""

import re
from collections import Counter


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


def _extract_competitors(responses: list[str], brand_name: str) -> list[str]:
    """
    Heuristic competitor extractor.

    Looks for capitalized tokens (Title-Case words) that:
      - appear 2+ times across all response text
      - are longer than 4 characters
      - are NOT the brand name (case-insensitive)
      - are NOT common English stop-words / generic adjectives

    Returns up to 3 candidates, ranked by frequency.
    """
    # Common words that start with a capital letter but aren't brand names
    _STOPWORDS = {
        "Here", "This", "These", "They", "Their", "There", "Some",
        "Also", "Note", "When", "With", "From", "Each", "Both",
        "However", "Overall", "Additionally", "While", "Often",
        "Best", "Good", "Great", "High", "Pure", "Natural",
        "Available", "Provides", "Recommended", "Helps", "Comes",
        "Amazon", "Other", "Another", "Third", "Second", "First",
        "Options", "Option", "Products", "Product", "Brand", "Brands",
        "Supplement", "Supplements", "Magnesium", "Vitamin", "Mineral",
        "Formula", "Quality", "Value", "Dose", "Daily",
    }

    brand_lower = brand_name.lower()
    combined_text = " ".join(responses)

    # Extract all Title-Case words (single token; multi-word handled below)
    # We look for sequences of 1-3 consecutive capitalized words (e.g. "Nature Made")
    pattern = re.compile(r'\b([A-Z][a-z]{3,})(?:\s+[A-Z][a-z]{2,}){0,2}\b')
    candidates: list[str] = []

    for match in pattern.finditer(combined_text):
        token = match.group(0).strip()
        # Skip if it matches the brand name
        if token.lower() == brand_lower or brand_lower in token.lower():
            continue
        # Skip generic stop-words (check each word in the phrase)
        words = token.split()
        if any(w in _STOPWORDS for w in words):
            continue
        # Minimum length guard on the full phrase
        if len(token) <= 4:
            continue
        candidates.append(token)

    # Rank by frequency and return top 3
    freq = Counter(candidates)
    top = [name for name, count in freq.most_common() if count >= 2]
    return top[:3]


def _rank(mention_rate: float) -> str:
    if mention_rate >= 0.6:
        return "high"
    if mention_rate >= 0.2:
        return "medium"
    return "low"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def parse_responses(llm_responses: dict, brand_name: str) -> dict:
    """
    Parse brand visibility and competitor data from raw LLM response dicts.

    Args:
        llm_responses: {"openai": [...], "claude": [...], "gemini": [...]}
                       Each list contains 5 strings (or error dicts) from
                       query_all_llms().
        brand_name:    The brand whose visibility is being measured
                       (e.g. "MagPure").

    Returns:
        {
            "openai": {
                "mention_count": int,       # how many of 5 responses mention brand
                "mention_rate":  float,     # mention_count / 5
                "rank":          str,       # "high" | "medium" | "low"
                "competitors":   list[str]  # up to 3 competitor names
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

        result[engine] = {
            "mention_count": mention_count,
            "mention_rate": mention_rate,
            "rank": _rank(mention_rate),
            "competitors": _extract_competitors(responses, brand_name),
        }

    return result


# ---------------------------------------------------------------------------
# Quick smoke-test (run directly: python response_parser.py)
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

    parsed = parse_responses(_SAMPLE_RESPONSES, brand_name="MagPure")
    import json
    print(json.dumps(parsed, indent=2))
