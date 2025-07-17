from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from resume_parser import parse_resume, parse_job_description
from scorer import compute_match_score
from tips_generator import generate_tips
from pdf_generator import generate_pdf_report

app = FastAPI()

@app.post("/analyze")
async def analyze(resume: UploadFile = File(...), jd: UploadFile = File(...)):
    resume_bytes = await resume.read()
    jd_bytes = await jd.read()
    resume_str = parse_resume(resume_bytes)
    jd_str = parse_job_description(jd_bytes)

    analysis = compute_match_score(resume_str, jd_str)
    tips = generate_tips(resume_str, jd_str).split("\n")
    analysis["tips"] = tips
    return analysis

@app.post("/export_pdf")
async def export_pdf(resume: UploadFile = File(...), jd: UploadFile = File(...)):
    resume_bytes = await resume.read()
    jd_bytes = await jd.read()
    resume_str = parse_resume(resume_bytes)
    jd_str = parse_job_description(jd_bytes)

    analysis = compute_match_score(resume_str, jd_str)
    tips = generate_tips(resume_str, jd_str).split("\n")
    analysis["tips"] = tips
    pdf_buffer = generate_pdf_report(resume_str, jd_str, analysis)
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment;filename=analysis_report.pdf"}
    )