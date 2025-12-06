import streamlit as st
import requests

# CHANGE THIS to the compute node running rag_api.py
API_URL = "http://dn034:5050/rag"

st.title("🔬 PubMed RAG Assistant")
st.write("Enter a query and retrieve medical answers generated using PubMed + Phi-3-mini.")

query = st.text_input("Enter your question:")

if st.button("Search & Answer"):
    if not query.strip():
        st.error("Please enter a query.")
    else:
        with st.spinner("Querying compute node RAG server..."):
            resp = requests.post(API_URL, json={"query": query}).json()

        st.subheader("💡 Answer")
        st.write(resp["answer"])

        st.subheader("📄 Retrieved Documents")
        for d in resp["documents"]:
            st.markdown(f"**{d['rank']}. PMID {d['pmid']} — {d['title']}**")
            st.write(d["abstract"][:300] + "...")
            st.markdown("---")

