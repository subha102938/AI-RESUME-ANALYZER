from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File

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
async def analyze(file: UploadFile = File(...)):


    temp_file = "uploaded_resume.pdf"

    with open(temp_file, "wb") as f:
        f.write(await file.read())

    # Extract text from PDF
    resume_text = extract_text(temp_file)

   
    emails = extract_email(resume_text)
    phones = extract_phone(resume_text)
    skills = extract_skills(resume_text)

   
    required_skills = [
        "Python",
        "SQL",
        "Machine Learning",
        "JavaScript"
    ]

  
    score = calculate_ats(skills, required_skills)
    matched = list(set(skills) & set(required_skills))
    missing = list(set(required_skills) - set(skills))

    return {
    "email": emails,
    "phone": phones,
    "skills": skills,
    "ats_score": score,
    "matched_skills": matched,
    "missing_skills": missing
}