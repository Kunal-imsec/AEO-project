"""
llm_orchestrator.py
-------------------
AEO Diagnostic Tool — Phase 2 (Free-tier rewrite)

Engines used (all FREE, no credit card required):
  • "openai"  slot → Groq  / llama-3.3-70b-versatile
  • "claude"  slot → Groq  / mixtral-8x7b-32768
  • "gemini"  slot → Google Gemini 2.0 Flash  (via google-genai SDK)

API keys read from environment:
  GROQ_API_KEY   — get free at https://console.groq.com
  GOOGLE_API_KEY — get free at https://aistudio.google.com
"""

import asyncio
import os

from google import genai
from groq import AsyncGroq

# ---------------------------------------------------------------------------
# Shared prompt builder
# ---------------------------------------------------------------------------

_SYSTEM_PROMPT = "You are a helpful shopping assistant."

def _user_prompt(query: str) -> str:
    return (
        "Answer this question concisely recommending 2-3 products: "
        f"{query}"
    )


# ---------------------------------------------------------------------------
# Groq — Llama 3.3 70B  (replaces OpenAI GPT-4o)
# ---------------------------------------------------------------------------

async def query_openai(queries: list[str]) -> list[str]:
    """
    Send each query to Llama-3.3-70b via Groq (free tier).
    Reads GROQ_API_KEY from the environment.
    Returns 5 response strings; on failure returns error dicts.
    """
    try:
        client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

        async def _call(query: str) -> str:
            try:
                response = await client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": _SYSTEM_PROMPT},
                        {"role": "user", "content": _user_prompt(query)},
                    ],
                    max_tokens=256,
                    temperature=0.3,
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                return {"error": str(e)}

        results = await asyncio.gather(*[_call(q) for q in queries])
        return list(results)

    except Exception as e:
        return [{"error": str(e)}] * len(queries)


# ---------------------------------------------------------------------------
# Groq — Mixtral 8x7B  (replaces Anthropic Claude)
# ---------------------------------------------------------------------------

async def query_claude(queries: list[str]) -> list[str]:
    """
    Send each query to Mixtral-8x7b via Groq (free tier).
    Reads GROQ_API_KEY from the environment.
    Returns 5 response strings; on failure returns error dicts.
    """
    try:
        client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

        async def _call(query: str) -> str:
            try:
                response = await client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": _SYSTEM_PROMPT},
                        {"role": "user", "content": _user_prompt(query)},
                    ],
                    max_tokens=256,
                    temperature=0.3,
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                return {"error": str(e)}

        results = await asyncio.gather(*[_call(q) for q in queries])
        return list(results)

    except Exception as e:
        return [{"error": str(e)}] * len(queries)


# ---------------------------------------------------------------------------
# Google — Gemini 1.5 Flash  (unchanged)
# ---------------------------------------------------------------------------

async def query_gemini(queries: list[str]) -> list[str]:
    """
    Send each query to gemini-2.5-flash via the modern google-genai SDK.
    Reads GOOGLE_API_KEY from the environment.
    Uses native async client — no executor needed.

    Rate-limit protection:
      • 2-second delay before every call to stay within free-tier QPM.
      • On a 429 error, waits 10 seconds then retries once.
    """
    try:
        client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

        async def _call(query: str) -> str:
            # 2-second pre-call delay to avoid hitting rate limits
            await asyncio.sleep(2)
            try:
                response = await client.aio.models.generate_content(
                    model="models/gemini-2.5-flash",
                    contents=f"{_SYSTEM_PROMPT}\n\n{_user_prompt(query)}",
                )
                return response.text.strip()
            except Exception as e:
                if "429" in str(e):
                    # Rate-limited — wait and retry once
                    await asyncio.sleep(10)
                    try:
                        response = await client.aio.models.generate_content(
                            model="models/gemini-2.5-flash",
                            contents=f"{_SYSTEM_PROMPT}\n\n{_user_prompt(query)}",
                        )
                        return response.text.strip()
                    except Exception as retry_e:
                        return {"error": str(retry_e)}
                else:
                    return {"error": str(e)}

        results = await asyncio.gather(*[_call(q) for q in queries])
        return list(results)

    except Exception as e:
        return [{"error": str(e)}] * len(queries)


# ---------------------------------------------------------------------------
# Orchestrator — all three LLMs in parallel
# ---------------------------------------------------------------------------

async def query_all_llms(queries: list[str]) -> dict:
    """
    Fire all three LLM providers simultaneously via asyncio.gather().

    Returns:
        {
            "openai": [5 response strings],   ← actually Llama 3.3 70B via Groq
            "claude": [5 response strings],   ← actually Mixtral 8x7B via Groq
            "gemini": [5 response strings],   ← Google Gemini 1.5 Flash
        }
    """
    openai_results, claude_results, gemini_results = await asyncio.gather(
        query_openai(queries),
        query_claude(queries),
        query_gemini(queries),
    )

    return {
        "openai": openai_results,
        "claude": claude_results,
        "gemini": gemini_results,
    }


# ---------------------------------------------------------------------------
# Quick smoke-test (run directly: python llm_orchestrator.py)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    from query_generator import generate_queries
    from dotenv import load_dotenv

    load_dotenv()

    sample_queries = generate_queries(
        product_name="wireless earbuds",
        category="electronics",
    )

    print("Queries:", sample_queries)
    print("\nQuerying all LLMs in parallel …\n")

    results = asyncio.run(query_all_llms(sample_queries))

    for provider, responses in results.items():
        print(f"=== {provider.upper()} ===")
        for i, resp in enumerate(responses, 1):
            print(f"  Q{i}: {resp}")
        print()
