"""
main.py
-------
AEO Diagnostic Tool — Phase 4 (complete pipeline).

Wire-up:
    query_generator  → generate_queries(product_name, category)  → list[str]
    llm_orchestrator → query_all_llms(queries)                   → dict
    response_parser  → parse_responses(llm_responses, brand_name)→ dict
    report_builder   → build_report(parsed, brand_name,
                                    product_name, queries)        → dict

Run with:
    uvicorn main:app --reload
"""

import traceback

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from query_generator import generate_queries
from llm_orchestrator import query_all_llms
from response_parser import parse_responses
from report_builder import build_report  # accepts optional category kwarg

# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------
load_dotenv()

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------
app = FastAPI(
    title="AEO Diagnostic Tool",
    description="Analyze how AI assistants respond to Amazon product queries.",
    version="1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------
class AnalyzeRequest(BaseModel):
    product_name: str
    brand_name: str
    category: str


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/health", summary="Health check")
def health_check():
    """Returns a simple liveness signal."""
    return {"status": "ok", "version": "1.0"}


@app.post("/analyze", summary="Run full AEO diagnostic pipeline")
async def analyze(body: AnalyzeRequest):
    """
    Runs the complete AEO diagnostic pipeline:
      1. Generate queries
      2. Query all LLMs concurrently
      3. Parse responses for brand mentions
      4. Build and return the diagnostic report
    """
    try:
        # Step 1 — query generation
        print(f"[analyze] Generating queries for '{body.product_name}' in '{body.category}'")
        queries = generate_queries(body.product_name, body.category)

        # Step 2 — LLM orchestration (async / concurrent)
        print(f"[analyze] Querying LLMs with {len(queries)} queries…")
        llm_responses = await query_all_llms(queries)

        # Step 3 — parse brand mentions from responses
        print(f"[analyze] Parsing responses for brand '{body.brand_name}'…")
        # Debug: show first 200 chars from each engine to verify API calls worked
        for engine, resps in llm_responses.items():
            preview = resps[0] if resps else "(empty)"
            print(f"  [{engine}] first response preview: {str(preview)[:200]}")
        parsed = parse_responses(llm_responses, body.brand_name)

        # Step 4 — build structured report
        print("[analyze] Building report…")
        report = build_report(parsed, body.brand_name, body.product_name, queries, body.category)

        print("[analyze] Done.")
        return report

    except Exception as e:
        print(f"[analyze] ERROR: {e}")
        print(traceback.format_exc())
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail={"error": str(e)})
