from database.db_connection import get_db_connection


def get_candidate_rankings(keyword=None, recommendation=None):
    """
    Returns AI match results ordered by highest score.
    Supports search and recommendation filter.
    """
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            match_results.*,
            resumes.candidate_name,
            resumes.email,
            jobs.job_title
        FROM match_results
        JOIN resumes ON match_results.resume_id = resumes.id
        JOIN jobs ON match_results.job_id = jobs.id
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

    if recommendation:
        query += " AND match_results.recommendation = %s"
        values.append(recommendation)

    query += " ORDER BY match_results.final_score DESC"

    cursor.execute(query, values)
    rankings = cursor.fetchall()

    cursor.close()
    connection.close()

    return rankings


def get_ranking_statistics():
    """
    Returns summary statistics for ranking page.
    """
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total FROM match_results")
    total = cursor.fetchone()["total"]

    cursor.execute("SELECT MAX(final_score) AS top_score FROM match_results")
    top_score = cursor.fetchone()["top_score"] or 0

    cursor.execute("SELECT AVG(final_score) AS average_score FROM match_results")
    average_score = cursor.fetchone()["average_score"] or 0

    cursor.execute("""
        SELECT COUNT(*) AS highly_suitable
        FROM match_results
        WHERE recommendation = 'Highly Suitable'
    """)
    highly_suitable = cursor.fetchone()["highly_suitable"]

    cursor.close()
    connection.close()

    return {
        "total": total,
        "top_score": round(float(top_score), 2),
        "average_score": round(float(average_score), 2),
        "highly_suitable": highly_suitable
    }


def get_top_candidate():
    """
    Returns best ranked candidate.
    """
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            match_results.*,
            resumes.candidate_name,
            jobs.job_title
        FROM match_results
        JOIN resumes ON match_results.resume_id = resumes.id
        JOIN jobs ON match_results.job_id = jobs.id
        ORDER BY match_results.final_score DESC
        LIMIT 1
    """)

    top_candidate = cursor.fetchone()

    cursor.close()
    connection.close()

    return top_candidate