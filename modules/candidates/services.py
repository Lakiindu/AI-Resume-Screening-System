from database.db_connection import get_db_connection


def get_all_candidates(keyword=None, status=None):
    """
    Gets candidates with optional search and status filter.
    """
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            resumes.id,
            resumes.candidate_name,
            resumes.email,
            resumes.phone,
            resumes.status,
            jobs.id AS job_id,
            jobs.job_title,
            match_results.final_score,
            match_results.recommendation
        FROM resumes
        LEFT JOIN match_results ON resumes.id = match_results.resume_id
        LEFT JOIN jobs ON jobs.id = match_results.job_id
        WHERE 1=1
    """

    values = []

    if keyword:
        query += """
            AND (
                resumes.candidate_name LIKE %s
                OR resumes.email LIKE %s
                OR jobs.job_title LIKE %s
            )
        """
        search_value = f"%{keyword}%"
        values.extend([search_value, search_value, search_value])

    if status:
        query += " AND resumes.status = %s"
        values.append(status)

    query += " ORDER BY resumes.uploaded_at DESC"

    cursor.execute(query, values)
    candidates = cursor.fetchall()

    cursor.close()
    connection.close()

    return candidates


def get_candidate_statistics():
    """
    Gets candidate status statistics.
    """
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total FROM resumes")
    total = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS pending FROM resumes WHERE status='pending'")
    pending = cursor.fetchone()["pending"]

    cursor.execute("SELECT COUNT(*) AS shortlisted FROM resumes WHERE status='shortlisted'")
    shortlisted = cursor.fetchone()["shortlisted"]

    cursor.execute("SELECT COUNT(*) AS rejected FROM resumes WHERE status='rejected'")
    rejected = cursor.fetchone()["rejected"]

    cursor.close()
    connection.close()

    return {
        "total": total,
        "pending": pending,
        "shortlisted": shortlisted,
        "rejected": rejected
    }


def update_candidate_status(candidate_id, status):
    """
    Updates candidate status.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE resumes
        SET status = %s
        WHERE id = %s
    """, (status, candidate_id))

    connection.commit()

    cursor.close()
    connection.close()