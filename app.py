from flask import Flask

# Create the Flask application
app = Flask(__name__)

# Home page route
@app.route("/")
def home():
    return "AI Resume Screening System is running successfully!"

# Run the application
if __name__ == "__main__":
    app.run(debug=True)