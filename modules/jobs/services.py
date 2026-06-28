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

def get_all_jobs(sort="latest"):
    """
    Gets all jobs from the database with sorting.
    """
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if sort == "oldest":
        query = "SELECT * FROM jobs ORDER BY created_at ASC"
    elif sort == "active":
        query = "SELECT * FROM jobs WHERE status='active' ORDER BY created_at DESC"
    elif sort == "closed":
        query = "SELECT * FROM jobs WHERE status='closed' ORDER BY created_at DESC"
    else:
        query = "SELECT * FROM jobs ORDER BY created_at DESC"

    cursor.execute(query)
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


def search_jobs(keyword, sort="latest"):
    """
    Searches jobs with optional sorting.
    """
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    search_value = f"%{keyword}%"

    base_query = """
        SELECT *
        FROM jobs
        WHERE job_title LIKE %s
           OR department LIKE %s
           OR location LIKE %s
           OR required_skills LIKE %s
           OR status LIKE %s
    """

    if sort == "oldest":
        base_query += " ORDER BY created_at ASC"
    elif sort == "active":
        base_query += " AND status='active' ORDER BY created_at DESC"
    elif sort == "closed":
        base_query += " AND status='closed' ORDER BY created_at DESC"
    else:
        base_query += " ORDER BY created_at DESC"

    cursor.execute(base_query, (
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

def get_job_statistics():
    """
    Returns job statistics for the Jobs dashboard.
    """
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total FROM jobs")
    total = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS active FROM jobs WHERE status='active'")
    active = cursor.fetchone()["active"]

    cursor.execute("SELECT COUNT(*) AS closed FROM jobs WHERE status='closed'")
    closed = cursor.fetchone()["closed"]

    cursor.close()
    connection.close()

    return {
        "total": total,
        "active": active,
        "closed": closed
    }