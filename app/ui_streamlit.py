"""
Simple Streamlit UI that calls the local pipeline directly.
Run:
    streamlit run app/ui_streamlit.py
"""
import streamlit as st
from .retriever import ChromaRetriever
from .agents import SupportCopilot

st.set_page_config(page_title="Multi-Agent Support Copilot", layout="wide")

st.title("🤖 Multi-Agent Support Copilot")
st.write("Ask questions grounded on your local docs (ingested into ChromaDB).")

if "copilot" not in st.session_state:
    st.session_state.copilot = SupportCopilot(ChromaRetriever())

with st.sidebar:
    st.header("Utilities")
    if st.button("Re-ingest docs"):
        from .ingest import main as ingest_main
        ingest_main()
        st.success("Re-ingested docs.")

query = st.text_input("Your question:", placeholder="e.g., How does ingestion work?")
if st.button("Ask") and query.strip():
    with st.spinner("Thinking..."):
        res = st.session_state.copilot.ask(query.strip())
    st.subheader("Answer")
    st.write(res.answer)

    st.subheader("Sources")
    for i, s in enumerate(res.sources, 1):
        st.markdown(f"**{i}.** `{s.get('metadata', {}).get('path', 'N/A')}` — chunk {s.get('metadata', {}).get('chunk', '-')}")
        st.write(s["text"])
