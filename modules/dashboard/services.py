from database.db_connection import get_db_connection


def get_dashboard_statistics():
    """
    Gets dashboard statistics from MySQL.
    If tables do not exist yet, return default zero values.
    """

    stats = {
        "total_jobs": 0,
        "total_resumes": 0,
        "pending_candidates": 0,
        "shortlisted_candidates": 0,
        "rejected_candidates": 0,
        "average_match_score": 0,
        "total_skills_extracted": 0,
        "recent_uploads": 0
    }

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Later these queries will work after we create jobs/resumes tables

        cursor.close()
        connection.close()

    except Exception as error:
        print("Dashboard statistics error:", error)

    return stats