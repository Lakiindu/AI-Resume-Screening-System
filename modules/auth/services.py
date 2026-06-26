from werkzeug.security import check_password_hash, generate_password_hash
from database.db_connection import get_db_connection


def get_user_by_email(email):
    """
    Finds a user by email address.
    """
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    cursor.close()
    connection.close()

    return user


def get_user_by_id(user_id):
    """
    Finds a user by ID.
    """
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()

    cursor.close()
    connection.close()

    return user


def authenticate_user(email, password):
    """
    Checks email and password for login.
    """
    user = get_user_by_email(email)

    if user and check_password_hash(user["password"], password):
        return user

    return None


def update_profile(user_id, name, email):
    """
    Updates admin profile details.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE users
        SET name = %s, email = %s
        WHERE id = %s
        """,
        (name, email, user_id)
    )

    connection.commit()
    cursor.close()
    connection.close()


def update_password(user_id, new_password):
    """
    Updates admin password using secure hashing.
    """
    hashed_password = generate_password_hash(new_password)

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE users
        SET password = %s
        WHERE id = %s
        """,
        (hashed_password, user_id)
    )

    connection.commit()
    cursor.close()
    connection.close()