import mysql.connector
from config import Config


def get_db_connection():
    """
    Creates and returns a MySQL database connection.
    This function will be reused in controllers/modules.
    """
    try:
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )

        return connection

    except mysql.connector.Error as error:
        print("Database connection failed:", error)
        return None