"""Seeds Neo4j with drug nodes and INTERACTS_WITH relationships."""

import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

SETUP_CYPHER = """
MERGE (aspirin:Drug {name: "Aspirin"})
MERGE (warfarin:Drug {name: "Warfarin"})
MERGE (ibuprofen:Drug {name: "Ibuprofen"})
MERGE (paracetamol:Drug {name: "Paracetamol"})
MERGE (metformin:Drug {name: "Metformin"})

MERGE (aspirin)-[:INTERACTS_WITH {
    reason: "Both affect blood clotting. Aspirin inhibits platelet aggregation while Warfarin is an anticoagulant — combining them significantly increases bleeding risk."
}]->(warfarin)

MERGE (ibuprofen)-[:INTERACTS_WITH {
    reason: "Both are NSAIDs. Combining them increases gastrointestinal side effects, ulcer risk, and reduces the cardioprotective effect of Aspirin."
}]->(aspirin)
"""

def setup():
    driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))
    try:
        with driver.session() as session:
            session.run(SETUP_CYPHER)
        print("✅ Graph seeded successfully.")
        print("   Drugs: Aspirin, Warfarin, Ibuprofen, Paracetamol, Metformin")
        print("   Interactions: Aspirin→Warfarin, Ibuprofen→Aspirin")
    except Exception as e:
        print(f"❌ Failed to seed graph: {e}")
        print("   Make sure Neo4j is running and credentials are correct.")
    finally:
        driver.close()

if __name__ == "__main__":
    setup()
