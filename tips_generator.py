import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_tips(resume_text, jd_text):
    prompt = f"""
    Job Description:
    {jd_text}

    Resume:
    {resume_text}

    Suggest 3 concrete improvements the resume can make to better match the job description.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful career coach."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
