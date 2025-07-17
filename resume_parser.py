from pdfminer.high_level import extract_text
from docx import Document
import io

def parse_resume(content: bytes) -> str:
    try:
        return extract_text(io.BytesIO(content))
    except:
        doc = Document(io.BytesIO(content))
        return "\n".join([para.text for para in doc.paragraphs])

def parse_job_description(content: bytes) -> str:
    try:
        return extract_text(io.BytesIO(content))
    except:
        doc = Document(io.BytesIO(content))
        return "\n".join([para.text for para in doc.paragraphs])