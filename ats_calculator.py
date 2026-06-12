def calculate_ats(found_skills, required_skills):

    if not required_skills:
        return 0.0
    matched = set(found_skills) & set(required_skills)

    score = (len(matched) / len(required_skills)) * 100

    return round(score, 2)