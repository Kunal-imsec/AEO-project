"""
report_builder.py
-----------------
AEO Diagnostic Tool — Phase 3

Converts the structured output of response_parser.parse_responses() into a
human-readable diagnostic report with an overall score, letter grade,
per-engine tips, and a deduplicated list of top competitors.
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _grade(score: float) -> str:
    """Map a 0-100 score to a letter grade."""
    if score >= 80:
        return "A"
    if score >= 60:
        return "B"
    if score >= 40:
        return "C"
    if score >= 20:
        return "D"
    return "F"


def _tip(rank: str, category: str = "product") -> str:
    """Generate an actionable tip string based on visibility rank."""
    if rank == "low":
        return (
            f"Your listing may lack {category} keywords AI engines recognize"
        )
    if rank == "medium":
        return "Mentioned sometimes — optimize your product description"
    # rank == "high"
    return "Strong AI visibility — maintain your listing quality"


def _unique_competitors(parsed: dict, max_count: int = 5) -> list[str]:
    """
    Collect all competitor names across the three engines, deduplicate while
    preserving approximate frequency order, and return up to *max_count*.
    """
    seen: set[str] = set()
    ordered: list[str] = []

    for engine_data in parsed.values():
        for name in engine_data.get("competitors", []):
            key = name.lower()
            if key not in seen:
                seen.add(key)
                ordered.append(name)

    return ordered[:max_count]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def build_report(
    parsed: dict,
    brand_name: str,
    product_name: str,
    queries: list[str],
    category: str = "",
) -> dict:
    """
    Build the final AEO diagnostic report.

    Args:
        parsed:       Output of response_parser.parse_responses().
        brand_name:   The brand under analysis (e.g. "MagPure").
        product_name: The specific product name (e.g. "MagPure 400mg Capsules").
        queries:      The 5 query strings originally sent to the LLMs.

    Returns:
        {
            "product":       str,
            "brand":         str,
            "overall_score": float,   # 0-100
            "grade":         str,     # A / B / C / D / F
            "queries_used":  list[str],
            "engines": {
                "openai": {
                    "mention_rate": float,
                    "rank":         str,
                    "tip":          str,
                    "competitors":  list[str],
                },
                "claude":  { ... },
                "gemini":  { ... },
            },
            "top_competitors": list[str],   # unique, max 5
            "summary":         str,
        }
    """
    engines_out: dict = {}
    mention_rates: list[float] = []

    # Use category for tips if provided, otherwise fall back to product_name
    category_hint = (category or product_name).lower()

    for engine in ("openai", "claude", "gemini"):
        data = parsed.get(engine, {})
        rate = data.get("mention_rate", 0.0)
        rank = data.get("rank", "low")
        mention_rates.append(rate)

        engines_out[engine] = {
            "mention_rate": rate,
            "rank": rank,
            "tip": _tip(rank, category_hint),
            "competitors": data.get("competitors", []),
        }

    # Overall score: average mention_rate × 100
    overall_score = round(
        (sum(mention_rates) / len(mention_rates)) * 100, 2
    )

    # Count how many engines rank "medium" or "high" (i.e., visible)
    recognized_count = sum(
        1 for e in engines_out.values() if e["rank"] in ("medium", "high")
    )

    return {
        "product": product_name,
        "brand": brand_name,
        "overall_score": overall_score,
        "grade": _grade(overall_score),
        "queries_used": queries,
        "engines": engines_out,
        "top_competitors": _unique_competitors(parsed),
        "summary": (
            f"Your brand is recognized by {recognized_count} out of 3 AI engines"
        ),
    }


# ---------------------------------------------------------------------------
# Quick smoke-test (run directly: python report_builder.py)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import json
    from response_parser import parse_responses

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

    _QUERIES = [
        "best magnesium supplement for seniors",
        "magnesium for sleep and muscle recovery",
        "top-rated magnesium capsules on Amazon",
        "magnesium glycinate vs oxide for seniors",
        "affordable magnesium supplement with high absorption",
    ]

    parsed = parse_responses(_SAMPLE_RESPONSES, brand_name="MagPure")
    report = build_report(
        parsed=parsed,
        brand_name="MagPure",
        product_name="MagPure 400mg Magnesium Capsules",
        queries=_QUERIES,
    )

    print(json.dumps(report, indent=2))
