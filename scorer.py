from langchain.embeddings import OpenAIEmbeddings
import pinecone
import os
import numpy as np

pinecone.init(api_key=os.getenv("PINECONE_API_KEY"), environment=os.getenv("PINECONE_ENV"))
index = pinecone.Index("resume-analyzer")
embeddings = OpenAIEmbeddings()

def compute_match_score(resume_text, jd_text):
    resume_vector = embeddings.embed_query(resume_text)
    jd_vector = embeddings.embed_query(jd_text)
    score = np.dot(resume_vector, jd_vector) / (np.linalg.norm(resume_vector) * np.linalg.norm(jd_vector))
    return round(score * 100, 2)