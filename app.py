import streamlit as st
import requests
import re
from resume_parser import parse_resume, parse_job_description
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Page config & styling
st.set_page_config(page_title="SmartResume Analyzer", layout="wide")
st.markdown("""
<style>
body { background-color: #f5f5f5; }
.score-circle { border-radius:50%; background:#3CB371; color:white;
  padding:20px; font-size:32px; font-weight:bold; text-align:center; }
.highlight-miss { background-color:#f8d7da; }
.highlight-match { background-color:#d4edda; }
</style>
""", unsafe_allow_html=True)

st.title("📄 SmartResume Analyzer")
col1, col2 = st.columns([1,2])

with col1:
    resume_file = st.file_uploader("Upload Resume", type=["pdf","docx"])
    jd_file = st.file_uploader("Upload Job Description", type=["pdf","docx"])
    if st.button("Analyze"):
        if resume_file and jd_file:
            # read & parse
            resume_bytes = resume_file.read()
            jd_bytes = jd_file.read()
            st.session_state["resume_bytes"] = resume_bytes
            st.session_state["jd_bytes"] = jd_bytes
            resume_str = parse_resume(resume_bytes)
            jd_str = parse_job_description(jd_bytes)
            st.session_state["resume_str"] = resume_str
            st.session_state["jd_str"] = jd_str
            # backend call
            resp = requests.post("http://localhost:8000/analyze", files={
                "resume": (resume_file.name, resume_bytes),
                "jd": (jd_file.name, jd_bytes)
            })
            st.session_state["analysis"] = resp.json()

with col2:
    if "analysis" in st.session_state:
        analysis = st.session_state["analysis"]
        # Overall Score
        st.markdown(f"<div class='score-circle'>{analysis['overall']}%</div>", unsafe_allow_html=True)

        # Section-Level Breakdown
        st.subheader("Section Match Scores")
        secs = analysis['sections']
        st.bar_chart(secs)

        # Accordion Panels
        for sec, score in secs.items():
            with st.expander(f"{sec}: {score}%"):
                st.write("**JD Section**")
                st.write(analysis['jd_sections'].get(sec, 'N/A'))
                st.write("**Your Resume**")
                st.write(analysis['resume_sections'].get(sec, 'N/A'))

        # Keyword & Gap Highlighting
        st.subheader("Keyword Highlights")
        resume_html = ""
        for word in st.session_state['resume_str'].split():
            clean = re.sub(r"\W", "", word).lower()
            if clean in analysis['matched_keywords']:
                cls = 'highlight-match'; title = 'Matched'
            elif clean in analysis['missing_keywords']:
                cls = 'highlight-miss'; title = 'Missing'
            else:
                cls = ''; title = ''
            resume_html += f"<span class='{cls}' title='{title}'>{word}</span> "
        st.markdown(resume_html, unsafe_allow_html=True)

        # Live Resume Editor
        st.subheader("Edit Resume")
        if 'history' not in st.session_state:
            st.session_state['history'] = [st.session_state['resume_str']]
            st.session_state['idx'] = 0
        text = st.text_area("Your Resume", value=st.session_state['history'][st.session_state['idx']], height=200)
        if st.button("Apply Improvement Tip"):
            tips = analysis.get('tips', [])
            if tips:
                new_text = text + "\n- " + tips.pop(0)
                st.session_state['history'] = st.session_state['history'][:st.session_state['idx']+1] + [new_text]
                st.session_state['idx'] += 1
        undo, redo = st.columns(2)
        if undo.button("Undo"): st.session_state['idx'] = max(0, st.session_state['idx']-1)
        if redo.button("Redo"): st.session_state['idx'] = min(len(st.session_state['history'])-1, st.session_state['idx']+1)

        # Interactive Visualizations: Word Clouds
        st.subheader("Keyword Word Clouds")
        wc1, wc2 = st.columns(2)
        with wc1:
            st.write("Missing Keywords")
            fig1 = plt.figure()
            wc = WordCloud(width=200, height=100).generate(" ".join(analysis['missing_keywords']))
            plt.imshow(wc.to_array()); plt.axis('off')
            st.pyplot(fig1)
        with wc2:
            st.write("Matched Keywords")
            fig2 = plt.figure()
            wc2_img = WordCloud(width=200, height=100).generate(" ".join(analysis['matched_keywords']))
            plt.imshow(wc2_img.to_array()); plt.axis('off')
            st.pyplot(fig2)

        # Experience Timeline Slider
        st.subheader("Experience Timeline")
        years = [int(y) for y in re.findall(r"\b(19|20)\d{2}\b", st.session_state['resume_str'])]
        if years:
            min_y, max_y = min(years), max(years)
            slider = st.slider("Filter by Year", min_y, max_y, (min_y, max_y))
            lines = [ln for ln in st.session_state['resume_str'].split("\n")
                     if any(str(y) in ln for y in range(slider[0], slider[1]+1))]
            st.write("\n".join(lines))

        # PDF Export & Sharing
        st.subheader("Export Report")
        if st.button("Download PDF Report"):
            resp_pdf = requests.post("http://localhost:8000/export_pdf", files={
                "resume": ("resume.pdf", st.session_state['resume_bytes']),
                "jd": ("jd.pdf", st.session_state['jd_bytes'])
            })
            st.download_button("Download PDF", data=resp_pdf.content,
                                file_name="analysis_report.pdf", mime="application/pdf")