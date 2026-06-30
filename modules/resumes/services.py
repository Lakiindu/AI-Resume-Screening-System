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

def save_resume_details(resume_id, parsed_data):
    """
    Saves parsed resume details into resume_details table.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM resume_details
        WHERE resume_id = %s
    """, (resume_id,))

    query = """
        INSERT INTO resume_details
        (
            resume_id,
            extracted_text,
            extracted_email,
            extracted_phone,
            extracted_skills,
            education,
            experience,
            projects,
            certificates,
            languages
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        resume_id,
        parsed_data["extracted_text"],
        parsed_data["extracted_email"],
        parsed_data["extracted_phone"],
        parsed_data["extracted_skills"],
        parsed_data["education"],
        parsed_data["experience"],
        parsed_data["projects"],
        parsed_data["certificates"],
        parsed_data["languages"]
    )

    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()

def get_resume_details_by_resume_id(resume_id):
    """
    Gets parsed details of a resume.
    """
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM resume_details
        WHERE resume_id = %s
        ORDER BY parsed_at DESC
        LIMIT 1
    """, (resume_id,))

    details = cursor.fetchone()

    cursor.close()
    connection.close()

    return details


def save_match_result(resume_id, job_id, match_data):
    """
    Saves AI match result into match_results table.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM match_results
        WHERE resume_id = %s AND job_id = %s
    """, (resume_id, job_id))

    cursor.execute("""
        INSERT INTO match_results
        (
            resume_id,
            job_id,
            similarity_score,
            skill_score,
            final_score,
            matched_skills,
            missing_skills,
            recommendation
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        resume_id,
        job_id,
        match_data["similarity_score"],
        match_data["skill_score"],
        match_data["final_score"],
        match_data["matched_skills"],
        match_data["missing_skills"],
        match_data["recommendation"]
    ))

    connection.commit()

    cursor.close()
    connection.close()

def get_match_result_by_resume_and_job(resume_id, job_id):
    """
    Gets AI match result with resume and job details.
    """
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            mr.*,
            r.candidate_name,
            r.email,
            r.phone,
            r.original_filename,
            j.job_title,
            j.department,
            j.location
        FROM match_results mr
        JOIN resumes r ON mr.resume_id = r.id
        JOIN jobs j ON mr.job_id = j.id
        WHERE mr.resume_id = %s AND mr.job_id = %s
        ORDER BY mr.matched_at DESC
        LIMIT 1
    """, (resume_id, job_id))

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result