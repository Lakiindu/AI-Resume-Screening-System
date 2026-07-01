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