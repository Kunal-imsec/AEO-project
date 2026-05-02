"""
query_generator.py
------------------
Generates realistic customer questions a shopper might type into an AI assistant.
No LLM calls — pure string-template logic.
"""


def generate_queries(product_name: str, category: str) -> list[str]:
    """
    Return exactly 5 natural-language questions a customer would ask an AI
    (e.g. ChatGPT) when searching for a product.

    Args:
        product_name: The specific product name (e.g. "Nature Made Magnesium").
        category:     The broader product category with any qualifiers
                      (e.g. "magnesium supplement for seniors").

    Returns:
        A list of exactly 5 query strings.
    """
    cat = category.strip().lower()
    prod = product_name.strip()

    # Use current year for recency-oriented queries
    current_year = 2026

    queries: list[str] = [
        # 1. Direct product recommendation intent
        f"best {prod} alternatives in {current_year}",

        # 2. Brand comparison intent — prompts LLMs to name specific brands
        f"which brand makes the best {prod}",

        # 3. Purchase / buying guide intent
        f"top {prod} to buy right now",

        # 4. Category-level discovery intent — still anchored to product
        f"recommend a {prod} under {cat}",

        # 5. Feature-specific intent to surface brand names
        f"what is the best {prod} and why",
    ]

    # Guarantee exactly 5 items regardless of future edits
    assert len(queries) == 5, "generate_queries must return exactly 5 queries"
    return queries
