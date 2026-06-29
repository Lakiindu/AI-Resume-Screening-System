from database.db_connection import get_db_connection

def save_resume(data):
    """
    Saves uploaded resume file details into MySQL.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO resumes
        (candidate_name, email, phone, original_filename, stored_filename, file_path, file_size, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        data["candidate_name"],
        data["email"],
        data["phone"],
        data["original_filename"],
        data["stored_filename"],
        data["file_path"],
        data["file_size"],
        "pending"
    )

    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()

def get_all_resumes():
    """
    Gets all uploaded resumes.
    """
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM resumes
        ORDER BY uploaded_at DESC
    """)

    resumes = cursor.fetchall()

    cursor.close()
    connection.close()

    return resumes

def get_resume_by_id(resume_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM resumes WHERE id = %s", (resume_id,))
    resume = cursor.fetchone()

    cursor.close()
    connection.close()

    return resume

def delete_resume_record(resume_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM resumes WHERE id = %s", (resume_id,))
    connection.commit()

    cursor.close()
    connection.close()

def search_resumes(keyword):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    search_value = f"%{keyword}%"

    cursor.execute("""
        SELECT *
        FROM resumes
        WHERE candidate_name LIKE %s
           OR email LIKE %s
           OR phone LIKE %s
           OR original_filename LIKE %s
           OR status LIKE %s
        ORDER BY uploaded_at DESC
    """, (
        search_value,
        search_value,
        search_value,
        search_value,
        search_value
    ))

    resumes = cursor.fetchall()

    cursor.close()
    connection.close()

    return resumes

def is_duplicate_resume(original_filename):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT id
        FROM resumes
        WHERE original_filename = %s
    """, (original_filename,))

    resume = cursor.fetchone()

    cursor.close()
    connection.close()

    return resume is not None