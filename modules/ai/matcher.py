from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from modules.ai.recommendation import get_recommendation


def calculate_similarity(job_text, resume_text):
    """
    Calculates TF-IDF cosine similarity between job description and resume text.
    Returns similarity percentage.
    """
    documents = [job_text, resume_text]

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

    return round(similarity * 100, 2)


def split_skills(skills_text):
    """
    Converts comma-separated skills text into clean skill list.
    """
    if not skills_text:
        return []

    return [
        skill.strip().lower()
        for skill in skills_text.split(",")
        if skill.strip()
    ]


def calculate_skill_match(job_skills, resume_skills):
    """
    Compares required job skills with resume skills.
    """
    required_skills = split_skills(job_skills)
    candidate_skills = split_skills(resume_skills)

    matched_skills = []
    missing_skills = []

    for skill in required_skills:
        if skill in candidate_skills:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    if required_skills:
        skill_score = (len(matched_skills) / len(required_skills)) * 100
    else:
        skill_score = 0

    return {
        "skill_score": round(skill_score, 2),
        "matched_skills": ", ".join(matched_skills),
        "missing_skills": ", ".join(missing_skills)
    }


def calculate_final_score(similarity_score, skill_score):
    """
    Combines similarity and skill score.
    """
    final_score = (similarity_score * 0.6) + (skill_score * 0.4)
    return round(final_score, 2)


def generate_match_result(job, resume_details):
    """
    Generates full AI match result for one job and one resume.
    """
    job_text = f"{job['job_title']} {job['required_skills']} {job['description']}"
    resume_text = f"{resume_details['extracted_text']} {resume_details['extracted_skills']}"

    similarity_score = calculate_similarity(job_text, resume_text)

    skill_result = calculate_skill_match(
        job["required_skills"],
        resume_details["extracted_skills"]
    )

    final_score = calculate_final_score(
        similarity_score,
        skill_result["skill_score"]
    )

    recommendation = get_recommendation(final_score)

    return {
        "similarity_score": similarity_score,
        "skill_score": skill_result["skill_score"],
        "final_score": final_score,
        "matched_skills": skill_result["matched_skills"],
        "missing_skills": skill_result["missing_skills"],
        "recommendation": recommendation
    }