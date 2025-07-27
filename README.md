# SmartResume Analyzer

A modern, AI-driven platform to optimize your job search by matching resumes with job descriptions, highlighting strengths and gaps, and offering actionable improvement tips through an interactive web interface.

🔎 **Features**

**Resume & Job Description Upload:** Drag-and-drop or browse to upload PDF/DOCX files (up to 200 MB each).

**Overall Match Score:** Calculates a single percentage reflecting resume-to-job alignment.

**Section-Level Breakdown:** Detailed similarity scores for Skills, Experience, and Education sections.

**Keyword Extraction & Highlighting:** Identifies key terms in the job description; highlights matches in green and gaps in red in your resume.

**Interactive Resume Editor:** Apply AI‑generated improvement tips inline with undo/redo history for iterative editing.

**Visual Analytics:**

- Bar charts for section match scores
- Dual word clouds for matched vs. missing keywords
- Experience timeline slider to filter resume content by year

**PDF Report Export:** Generate and download a comprehensive PDF summary of your analysis.

🚀 **Quick Start**

**Clone the repository**

```bash
git clone https://github.com/<your-username>/SmartResumeAnalyzer.git
cd SmartResumeAnalyzer
```

**Install dependencies**

```bash
pip install -r requirements.txt
```

**Configure environment variables**

```bash
export OPENAI_API_KEY="sk-..."
export PINECONE_API_KEY="..."
export PINECONE_ENV="us-west1-gcp"
```

**Run the backend & frontend**

```bash
# In one terminal (backend)
uvicorn main:app --reload

# In a second terminal (frontend)
streamlit run app.py
```

⚙️ **Configuration**

- **OPENAI\_API\_KEY:** Your OpenAI secret key for embeddings
- **PINECONE\_API\_KEY:** Your Pinecone API key
- **PINECONE\_ENV:** Your Pinecone region (e.g. `us-west1-gcp`)

📂 **Project Structure**

```text
├── app.py            # Streamlit frontend UI
├── main.py           # FastAPI backend entrypoint
├── scorer.py         # AI & vector-search logic
├── resume_parser.py  # PDF/DOCX parsing utility
├── tips_generator.py # Improvement-tip engine
├── requirements.txt  # Python dependencies
├── settings.json     # UI theming config
└── .venv/            # Local Python environment (ignored)
```

