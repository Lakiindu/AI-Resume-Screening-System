from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from modules.ai.recommendation import get_recommendation


def calculate_similarity(job_text, resume_text):
    documents = [job_text, resume_text]

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

    return round(similarity * 100, 2)


def split_skills(skills_text):
    if not skills_text:
        return []

    return [
        skill.strip().lower()
        for skill in skills_text.split(",")
        if skill.strip()
    ]


def calculate_skill_match(job_skills, resume_skills):
    required_skills = split_skills(job_skills)
    candidate_skills = split_skills(resume_skills)

    matched_skills = []
    missing_skills = []

    for skill in required_skills:
        if skill in candidate_skills:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    skill_score = 0

    if required_skills:
        skill_score = (len(matched_skills) / len(required_skills)) * 100

    return {
        "skill_score": round(skill_score, 2),
        "matched_skills": ", ".join(matched_skills),
        "missing_skills": ", ".join(missing_skills)
    }


def keyword_score(job_text, resume_section):
    """
    Gives score if resume section contains words related to the job.
    """
    if not resume_section:
        return 0

    job_words = set(job_text.lower().split())
    section_words = set(resume_section.lower().split())

    common_words = job_words.intersection(section_words)

    if len(common_words) >= 5:
        return 100
    elif len(common_words) >= 3:
        return 70
    elif len(common_words) >= 1:
        return 40
    else:
        return 0


def calculate_final_score(
    similarity_score,
    skill_score,
    education_score,
    experience_score,
    project_score
):
    final_score = (
        similarity_score * 0.40 +
        skill_score * 0.35 +
        education_score * 0.10 +
        experience_score * 0.10 +
        project_score * 0.05
    )

    return round(final_score, 2)


def generate_match_result(job, resume_details):
    job_text = f"""
        {job['job_title']}
        {job['required_skills']}
        {job['description']}
        {job['experience_required']}
    """

    resume_text = f"""
        {resume_details['extracted_text']}
        {resume_details['extracted_skills']}
        {resume_details['education']}
        {resume_details['experience']}
        {resume_details['projects']}
    """

    similarity_score = calculate_similarity(job_text, resume_text)

    skill_result = calculate_skill_match(
        job["required_skills"],
        resume_details["extracted_skills"]
    )

    education_score = keyword_score(job_text, resume_details["education"])
    experience_score = keyword_score(job_text, resume_details["experience"])
    project_score = keyword_score(job_text, resume_details["projects"])

    final_score = calculate_final_score(
        similarity_score,
        skill_result["skill_score"],
        education_score,
        experience_score,
        project_score
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