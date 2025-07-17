from langchain.embeddings import OpenAIEmbeddings
import pinecone
import os
import numpy as np
import re
from collections import Counter

# initialize Pinecone
pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENV")
)
index = pinecone.Index("resume-analyzer")
embeddings = OpenAIEmbeddings()

STOPWORDS = set(["and","the","for","with","that","this","from","your","have","will","you","are"])

def extract_section(text: str, header: str) -> str:
    pattern = rf"{header}:(.*?)(?:\n\w+:|$)"
    m = re.search(pattern, text, re.S | re.I)
    return m.group(1).strip() if m else ""

def get_keywords(text: str, top_n: int = 20) -> list:
    words = re.findall(r"\b\w+\b", text.lower())
    words = [w for w in words if len(w) > 4 and w not in STOPWORDS]
    freq = Counter(words)
    return [w for w, _ in freq.most_common(top_n)]

def compute_match_score(resume_text: str, jd_text: str) -> dict:
    # overall similarity
    r_vec = embeddings.embed_query(resume_text)
    j_vec = embeddings.embed_query(jd_text)
    overall = np.dot(r_vec, j_vec) / (np.linalg.norm(r_vec) * np.linalg.norm(j_vec))

    # section-level
    sections = {}
    resume_sections = {}
    jd_sections = {}
    for sec in ["Skills", "Experience", "Education"]:
        r_sec = extract_section(resume_text, sec)
        j_sec = extract_section(jd_text, sec)
        resume_sections[sec] = r_sec
        jd_sections[sec] = j_sec
        if r_sec and j_sec:
            rv = embeddings.embed_query(r_sec)
            jv = embeddings.embed_query(j_sec)
            score = np.dot(rv, jv) / (np.linalg.norm(rv) * np.linalg.norm(jv))
        else:
            score = 0.0
        sections[sec] = round(score * 100, 2)

    # keywords
    jd_keywords = get_keywords(jd_text)
    resume_lower = resume_text.lower()
    matched = [kw for kw in jd_keywords if kw in resume_lower]
    missing = [kw for kw in jd_keywords if kw not in resume_lower]

    return {
        "overall": round(overall * 100, 2),
        "sections": sections,
        "matched_keywords": matched,
        "missing_keywords": missing,
        "resume_sections": resume_sections,
        "jd_sections": jd_sections
    }