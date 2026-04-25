"""Core agent: extracts drug names via Ollama, queries Neo4j for interactions."""

import os
import requests
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

KNOWN_DRUGS = ["Aspirin", "Warfarin", "Ibuprofen", "Paracetamol", "Metformin"]


def _get_all_drugs() -> list[str]:
    """Fetch current drug list from Neo4j."""
    driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))
    try:
        with driver.session() as session:
            result = session.run("MATCH (d:Drug) RETURN d.name AS name ORDER BY d.name")
            return [r["name"] for r in result]
    finally:
        driver.close()


def extract_drugs(query: str) -> list[str]:
    """Extract drug names from natural language using Ollama, fall back to string matching."""
    try:
        drugs_in_db = _get_all_drugs()
    except Exception:
        drugs_in_db = KNOWN_DRUGS

    prompt = (
        f"Extract ONLY the drug names from this text. "
        f"Return them as a comma-separated list, nothing else. "
        f"Only include drugs from this list: {', '.join(drugs_in_db)}.\n"
        f"Text: \"{query}\"\n"
        f"Drug names:"
    )

    try:
        resp = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=30,
        )
        resp.raise_for_status()
        raw = resp.json()["response"].strip()
        extracted = [d.strip().title() for d in raw.split(",") if d.strip()]
        matched = [d for d in extracted if d in drugs_in_db]
        if matched:
            return matched
    except Exception:
        pass

    # Fallback: case-insensitive substring match
    query_lower = query.lower()
    return [d for d in drugs_in_db if d.lower() in query_lower]


def check_interaction(drug1: str, drug2: str) -> list[dict]:
    """Check interaction in both directions."""
    driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))
    try:
        with driver.session() as session:
            result = session.run(
                """
                MATCH (a:Drug {name: $d1})-[r:INTERACTS_WITH]->(b:Drug {name: $d2})
                RETURN a.name AS drug1, b.name AS drug2, r.reason AS reason
                UNION
                MATCH (a:Drug {name: $d2})-[r:INTERACTS_WITH]->(b:Drug {name: $d1})
                RETURN a.name AS drug1, b.name AS drug2, r.reason AS reason
                """,
                d1=drug1,
                d2=drug2,
            )
            return result.data()
    finally:
        driver.close()


def format_response(drug1: str, drug2: str, interactions: list[dict]) -> str:
    if interactions:
        r = interactions[0]
        return (
            f"⚠️  Yes, these drugs interact.\n"
            f"{r['drug1']} ↔ {r['drug2']}: {r['reason']}\n"
            f"🩺 Disclaimer: Consult a doctor before combining these medications."
        )
    return (
        f"✅ No known interaction found between {drug1} and {drug2} in the database.\n"
        f"🩺 Disclaimer: Always consult a healthcare professional before combining medications."
    )


def answer_query(user_query: str) -> str:
    drugs = extract_drugs(user_query)

    if len(drugs) < 2:
        return (
            f"❓ Could not identify two known drugs in your query.\n"
            f"Known drugs: {', '.join(KNOWN_DRUGS)}\n"
            f"Example: 'Can I take Aspirin with Warfarin?'"
        )

    drug1, drug2 = drugs[0], drugs[1]
    try:
        interactions = check_interaction(drug1, drug2)
    except Exception as e:
        return f"❌ Database error: {e}\nMake sure Neo4j is running and the graph is seeded."

    return format_response(drug1, drug2, interactions)
