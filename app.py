from flask import Flask
from config import Config
from database.db_connection import get_db_connection

app = Flask(__name__)
app.config.from_object(Config)


@app.route("/")
def home():
    connection = get_db_connection()

    if connection:
        connection.close()
        return "AI Resume Screening System connected to MySQL successfully!"

    return "Database connection failed. Please check your MySQL settings."


if __name__ == "__main__":
    app.run(debug=True)