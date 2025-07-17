import streamlit as st
import requests

st.title("📄 SmartResume Analyzer")

resume_file = st.file_uploader("Upload your Resume", type=["pdf", "docx"])
jd_file = st.file_uploader("Upload Job Description", type=["pdf", "docx"])

if st.button("Analyze") and resume_file and jd_file:
    with st.spinner("Analyzing..."):
        response = requests.post(
            "http://localhost:8000/analyze",
            files={
                "resume": resume_file,
                "jd": jd_file
            }
        )
        result = response.json()
        st.metric("Match Score", f"{result['match_score']}%")
        st.subheader("Improvement Tips")
        st.write(result['improvement_tips'])

st.caption("Built with FastAPI, OpenAI, Pinecone, and Streamlit")
