from database.db_connection import get_db_connection


def get_candidate_rankings():
    """
    Returns all AI match results ordered by highest score.
    """

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            match_results.*,
            resumes.candidate_name,
            resumes.email,
            jobs.job_title
        FROM match_results

        JOIN resumes
            ON match_results.resume_id = resumes.id

        JOIN jobs
            ON match_results.job_id = jobs.id

        ORDER BY match_results.final_score DESC
    """)

    rankings = cursor.fetchall()

    cursor.close()
    connection.close()

    return rankings