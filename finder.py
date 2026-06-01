import re

def extract_email(resume_text):
    emails = re.findall(
        r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',
        resume_text
    )
    return emails

def extract_phone(resume_text):
    phones = re.findall(r'\b\d{10}\b', resume_text)
    return phones

def extract_skills(resume_text):
    skills_db = [
        "Python", "C", "C++", "Java",
        "SQL", "Machine Learning",
        "HTML", "CSS", "JavaScript"
    ]

    found_skills = []

    for skill in skills_db:
        if re.search(re.escape(skill), resume_text, re.IGNORECASE):
            found_skills.append(skill)

    return found_skills