"""
query_generator.py
------------------
Generates realistic customer questions a shopper might type into an AI assistant.
No LLM calls — pure string-template logic.
"""


def generate_queries(product_name: str, category: str) -> list[str]:
    """
    Return exactly 5 natural-language questions a real shopper would type into
    ChatGPT/Claude/Gemini — category-first, never using the brand or full
    product name so mention rates reflect genuine AI recall rather than
    keyword-prompted recall.

    product_name is used *only* to detect a sub-category keyword
    (e.g. "earbuds", "tablet", "capsules") that makes the query more specific.

    Args:
        product_name: The specific product name (e.g. "MagPure 400mg Capsules").
        category:     The broader product category (e.g. "magnesium supplement").

    Returns:
        A list of exactly 5 query strings.
    """
    cat = category.strip().lower()

    # ── Sub-category extraction ───────────────────────────────────────────
    # Pull the first meaningful word from product_name that is NOT the brand
    # (assumed to be the first token) and NOT a generic filler word.
    _FILLERS = {
        "the", "a", "an", "and", "or", "for", "with", "by", "in", "of",
        "mg", "ml", "oz", "lb", "pack", "set", "kit", "pro", "plus", "max",
        "ultra", "premium", "new", "best", "top", "brand", "product",
    }
    tokens = product_name.strip().lower().split()
    # skip the first token (likely the brand name) and any fillers / digits
    sub = next(
        (t for t in tokens[1:] if t not in _FILLERS and not t[0].isdigit()),
        None,
    )
    # subject = sub-category if found, else fall back to the full category
    subject = f"{sub}" if sub else cat

    current_year = 2026

    queries: list[str] = [
        # 1. Recency-oriented buying intent
        f"best {subject} to buy in {current_year}",

        # 2. Quality-focused comparison — makes LLMs name brands unprompted
        f"which {subject} has the best quality right now",

        # 3. Budget / value intent
        f"top rated {subject} under 5000",

        # 4. Expert / editorial recommendation intent
        f"{subject} recommended by experts",

        # 5. Popularity / trending intent
        f"most popular {cat} brand right now",
    ]

    assert len(queries) == 5, "generate_queries must return exactly 5 queries"
    return queries
