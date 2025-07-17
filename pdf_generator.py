from fpdf import FPDF
from wordcloud import WordCloud
from io import BytesIO

def generate_pdf_report(resume_text: str, jd_text: str, analysis: dict) -> BytesIO:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "SmartResume Analyzer Report", 0, 1, "C")
    pdf.ln(5)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"Overall Match Score: {analysis['overall']}%", 0, 1)
    pdf.ln(3)
    for sec, sc in analysis["sections"].items():
        pdf.cell(0, 6, f"{sec}: {sc}%", 0, 1)
    pdf.ln(5)
    # missing keywords word cloud
    if analysis.get("missing_keywords"):
        wc = WordCloud(width=200, height=100).generate(" ".join(analysis["missing_keywords"]))
        buf = BytesIO()
        wc.to_image().save(buf, format="PNG")
        buf.seek(0)
        pdf.image(buf, x=10, w=90)
    # matched keywords word cloud
    if analysis.get("matched_keywords"):
        wc2 = WordCloud(width=200, height=100).generate(" ".join(analysis["matched_keywords"]))
        buf2 = BytesIO()
        wc2.to_image().save(buf2, format="PNG")
        buf2.seek(0)
        pdf.image(buf2, x=110, w=90)
    pdf.ln(60)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Suggested Improvements", 0, 1)
    pdf.set_font("Arial", "", 12)
    for tip in analysis.get("tips", []):
        pdf.multi_cell(0, 6, f"- {tip}", 0, 1)
    output = BytesIO()
    pdf.output(output)
    output.seek(0)
    return output