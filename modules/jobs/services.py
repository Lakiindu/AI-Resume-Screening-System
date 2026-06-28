from database.db_connection import get_db_connection


def create_job(data):
    """
    Saves a new job vacancy into the jobs table.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO jobs
        (
            job_title,
            department,
            location,
            experience_required,
            salary,
            required_skills,
            description,
            status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        data["job_title"],
        data["department"],
        data["location"],
        data["experience_required"],
        data["salary"],
        data["required_skills"],
        data["description"],
        data["status"]
    )

    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()


def get_all_jobs():
    """
    Gets all jobs from the database.
    """
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM jobs
        ORDER BY created_at DESC
    """)

    jobs = cursor.fetchall()

    cursor.close()
    connection.close()

    return jobs