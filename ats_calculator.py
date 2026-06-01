def calculate_ats(found_skills, required_skills):

    matched = set(found_skills) & set(required_skills)

    score = (len(matched) / len(required_skills)) * 100

    return round(score, 2)