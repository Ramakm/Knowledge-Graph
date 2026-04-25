"""FastAPI backend for Drug Interaction Knowledge Graph."""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from agent import answer_query, check_interaction, extract_drugs, _get_all_drugs

load_dotenv()

app = FastAPI(title="Drug Interaction API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    query: str


class DirectCheckRequest(BaseModel):
    drug1: str
    drug2: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/drugs")
def list_drugs():
    try:
        return {"drugs": _get_all_drugs()}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database unavailable: {e}")


@app.post("/query")
def natural_language_query(req: QueryRequest):
    """Accept a natural language question and return interaction result."""
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    result = answer_query(req.query)
    drugs = extract_drugs(req.query)
    return {
        "query": req.query,
        "drugs_detected": drugs,
        "result": result,
    }


@app.post("/check")
def direct_check(req: DirectCheckRequest):
    """Directly check interaction between two named drugs."""
    interactions = check_interaction(req.drug1, req.drug2)
    has_interaction = len(interactions) > 0
    return {
        "drug1": req.drug1,
        "drug2": req.drug2,
        "has_interaction": has_interaction,
        "details": interactions[0] if has_interaction else None,
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("api:app", host="0.0.0.0", port=port, reload=True)
