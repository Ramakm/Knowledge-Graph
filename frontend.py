"""Streamlit frontend for Drug Interaction Knowledge Graph."""

import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Drug Interaction Graph", page_icon="💊", layout="centered")

st.title("💊 Drug Interaction Knowledge Graph")
st.caption("Powered by Neo4j + Ollama (llama3.2)")


def get_drugs():
    try:
        r = requests.get(f"{API_URL}/drugs", timeout=5)
        return r.json().get("drugs", [])
    except Exception:
        return []


# Sidebar: known drugs
with st.sidebar:
    st.header("🗂️ Database")
    drugs = get_drugs()
    if drugs:
        st.success(f"{len(drugs)} drugs loaded")
        for d in drugs:
            st.write(f"• {d}")
    else:
        st.error("Neo4j unavailable")
    st.divider()
    st.markdown("**Known Interactions**")
    st.write("• Aspirin ↔ Warfarin")
    st.write("• Ibuprofen ↔ Aspirin")


tab1, tab2 = st.tabs(["🔎 Natural Language Query", "⚡ Direct Check"])

# --- Tab 1: Natural language ---
with tab1:
    st.subheader("Ask in plain English")
    example_queries = [
        "Can I take Aspirin with Warfarin?",
        "Is it safe to combine Ibuprofen and Aspirin?",
        "What happens if I take Paracetamol and Metformin together?",
    ]
    selected_example = st.selectbox("Try an example:", ["(type your own)"] + example_queries)

    default_text = selected_example if selected_example != "(type your own)" else ""
    query = st.text_input("Your question:", value=default_text, placeholder="e.g. Can I take Aspirin with Warfarin?")

    if st.button("🔍 Check", key="nl_check"):
        if not query.strip():
            st.warning("Please enter a query.")
        else:
            with st.spinner("Checking..."):
                try:
                    r = requests.post(f"{API_URL}/query", json={"query": query}, timeout=30)
                    data = r.json()
                    if "detail" in data:
                        st.error(data["detail"])
                    else:
                        if data.get("drugs_detected"):
                            st.info(f"Drugs detected: **{', '.join(data['drugs_detected'])}**")
                        result = data["result"]
                        if result.startswith("⚠️"):
                            st.error(result)
                        elif result.startswith("✅"):
                            st.success(result)
                        else:
                            st.warning(result)
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to API. Start it with: `python api.py`")
                except Exception as e:
                    st.error(f"Error: {e}")

# --- Tab 2: Direct drug selector ---
with tab2:
    st.subheader("Select two drugs directly")
    drug_list = drugs if drugs else ["Aspirin", "Warfarin", "Ibuprofen", "Paracetamol", "Metformin"]

    col1, col2 = st.columns(2)
    with col1:
        drug1 = st.selectbox("Drug 1", drug_list, index=0)
    with col2:
        drug2 = st.selectbox("Drug 2", drug_list, index=1)

    if st.button("⚡ Check Interaction", key="direct_check"):
        if drug1 == drug2:
            st.warning("Please select two different drugs.")
        else:
            with st.spinner("Querying graph..."):
                try:
                    r = requests.post(
                        f"{API_URL}/check",
                        json={"drug1": drug1, "drug2": drug2},
                        timeout=10,
                    )
                    data = r.json()
                    if data["has_interaction"]:
                        details = data["details"]
                        st.error(
                            f"⚠️ **Interaction found!**\n\n"
                            f"**{details['drug1']} ↔ {details['drug2']}**\n\n"
                            f"{details['reason']}\n\n"
                            f"🩺 Consult a doctor before combining these medications."
                        )
                    else:
                        st.success(
                            f"✅ No known interaction between **{drug1}** and **{drug2}**.\n\n"
                            f"🩺 Still consult a healthcare professional."
                        )
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to API. Start it with: `python api.py`")
                except Exception as e:
                    st.error(f"Error: {e}")
