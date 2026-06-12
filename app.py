from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, Form

from extractor import extract_text
from finder import extract_email, extract_phone, extract_skills
from ats_calculator import calculate_ats

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Resume Analyzer API is working"}

@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    job_description: str = Form("")
):

    temp_file = "uploaded_resume.pdf"

    with open(temp_file, "wb") as f:
        f.write(await file.read())

    # Extract text from PDF
    resume_text = extract_text(temp_file)

    emails = extract_email(resume_text)
    phones = extract_phone(resume_text)
    resume_skills = extract_skills(resume_text)

    # Use extracted job description skills if provided; fall back if empty
    job_required_skills = []
    if job_description and job_description.strip():
        job_required_skills = extract_skills(job_description)

    if not job_required_skills:
        job_required_skills = [
            "Python",
            "SQL",
            "Machine Learning",
            "JavaScript"
        ]

    score = calculate_ats(resume_skills, job_required_skills)
    matched = list(set(resume_skills) & set(job_required_skills))
    missing = list(set(job_required_skills) - set(resume_skills))

    return {
        "email": emails,
        "phone": phones,
        "resume_skills": resume_skills,
        "skills": resume_skills,  # for backward compatibility
        "job_required_skills": job_required_skills,
        "matched_skills": matched,
        "missing_skills": missing,
        "ats_score": score
    }