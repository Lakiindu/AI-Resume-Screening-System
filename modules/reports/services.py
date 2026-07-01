from database.db_connection import get_db_connection


def get_candidate_report():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT candidate_name, email, phone, status, uploaded_at
        FROM resumes
        ORDER BY uploaded_at DESC
    """)

    data = cursor.fetchall()
    cursor.close()
    connection.close()

    return data


def get_job_report():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT job_title, department, location, status, created_at
        FROM jobs
        ORDER BY created_at DESC
    """)

    data = cursor.fetchall()
    cursor.close()
    connection.close()

    return data


def get_match_report():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            resumes.candidate_name,
            jobs.job_title,
            match_results.final_score,
            match_results.recommendation,
            match_results.matched_at
        FROM match_results
        JOIN resumes ON match_results.resume_id = resumes.id
        JOIN jobs ON match_results.job_id = jobs.id
        ORDER BY match_results.final_score DESC
    """)

    data = cursor.fetchall()
    cursor.close()
    connection.close()

    return data


def get_status_report():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT status, COUNT(*) AS total
        FROM resumes
        GROUP BY status
    """)

    data = cursor.fetchall()
    cursor.close()
    connection.close()

    return data

def get_ai_report_data(resume_id, job_id):
    """
    Gets complete AI match result data required for AI PDF report export.
    Includes candidate info, job info, AI scores, skills, and parsed resume details.
    """
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            r.id AS resume_id,
            r.candidate_name,
            r.email,
            r.phone,
            r.original_filename,
            r.status,

            j.id AS job_id,
            j.job_title,
            j.department,
            j.location,
            j.experience_required,
            j.required_skills,

            mr.similarity_score AS tfidf_score,
            mr.skill_score,
            mr.final_score,
            mr.recommendation,
            mr.matched_skills,
            mr.missing_skills,
            mr.matched_at,

            rd.education,
            rd.experience,
            rd.projects,
            rd.certificates,
            rd.languages

        FROM match_results mr

        JOIN resumes r
            ON mr.resume_id = r.id

        JOIN jobs j
            ON mr.job_id = j.id

        LEFT JOIN resume_details rd
            ON rd.resume_id = r.id

        WHERE mr.resume_id = %s
        AND mr.job_id = %s

        ORDER BY mr.matched_at DESC
        LIMIT 1
    """, (resume_id, job_id))

    data = cursor.fetchone()

    cursor.close()
    connection.close()

    return data