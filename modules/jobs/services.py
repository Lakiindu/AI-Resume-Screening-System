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


def get_job_by_id(job_id):
    """
    Gets one job by ID.
    """
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM jobs
        WHERE id = %s
    """, (job_id,))

    job = cursor.fetchone()

    cursor.close()
    connection.close()

    return job


def update_job(job_id, data):
    """
    Updates an existing job vacancy.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        UPDATE jobs
        SET job_title = %s,
            department = %s,
            location = %s,
            experience_required = %s,
            salary = %s,
            required_skills = %s,
            description = %s,
            status = %s
        WHERE id = %s
    """

    values = (
        data["job_title"],
        data["department"],
        data["location"],
        data["experience_required"],
        data["salary"],
        data["required_skills"],
        data["description"],
        data["status"],
        job_id
    )

    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()


def delete_job(job_id):
    """
    Deletes a job from the database.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM jobs
        WHERE id = %s
    """, (job_id,))

    connection.commit()

    cursor.close()
    connection.close()


def search_jobs(keyword):
    """
    Searches jobs by title, department, location, skills, or status.
    """
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    search_value = f"%{keyword}%"

    cursor.execute("""
        SELECT *
        FROM jobs
        WHERE job_title LIKE %s
           OR department LIKE %s
           OR location LIKE %s
           OR required_skills LIKE %s
           OR status LIKE %s
        ORDER BY created_at DESC
    """, (
        search_value,
        search_value,
        search_value,
        search_value,
        search_value
    ))

    jobs = cursor.fetchall()

    cursor.close()
    connection.close()

    return jobs