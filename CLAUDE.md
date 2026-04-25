# 🧪 Mini Project: Drug Interaction Knowledge Graph

## 🎯 Goal

Build a simple system that:

* Stores drug interactions in a Neo4j graph
* Takes user queries in natural language
* Returns whether two drugs interact + explanation

---

## 🧩 Graph Schema

Nodes:

* Drug {name}

Relationships:

* (Drug)-[:INTERACTS_WITH]->(Drug)

---

## 📥 Seed Data (MANDATORY)

Create the following:

Drugs:

* Aspirin
* Warfarin
* Ibuprofen
* Paracetamol
* Metformin

Relationships:

* Aspirin → Warfarin
* Ibuprofen → Aspirin

---

## 🔎 Query Task

Input:
"Can I take Aspirin with Warfarin?"

Steps:

1. Extract drug names from query
2. Query Neo4j:
   MATCH (d1:Drug {name: "Aspirin"})-[:INTERACTS_WITH]->(d2:Drug {name: "Warfarin"})
3. If exists → interaction found

---

## 📤 Output Format

If interaction exists:

"⚠️ Yes, these drugs interact.
Aspirin and Warfarin both affect blood clotting, increasing bleeding risk.
Consult a doctor before combining them."

If not:

"✅ No known interaction found in the database.
Still consult a healthcare professional."

---

## 🤖 Rules

* Do NOT hallucinate interactions
* Only use graph data
* Always include disclaimer

---

## 🧰 Deliverables

Claude should:

1. Generate Neo4j setup code (Cypher)
2. Write Python script to query graph
3. Add simple CLI or API
4. Use LLM to extract drug names from input

---

## 🎤 Demo Flow

1. Show graph in Neo4j UI
2. Ask query live:
   "Can I take Ibuprofen with Aspirin?"
3. Show result instantly

Keep it fast, clear, and visual.
