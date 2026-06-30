from flask import Flask, render_template

from config import Config

from modules.auth.routes import auth_bp
from modules.dashboard.routes import dashboard_bp
from modules.jobs.routes import jobs_bp
from modules.resumes.routes import resumes_bp
from modules.ranking.routes import ranking_bp

# Create Flask application
app = Flask(__name__)

# Load configuration
app.config.from_object(Config)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(jobs_bp)
app.register_blueprint(resumes_bp)
app.register_blueprint(ranking_bp)

# Custom 404 Error Page
@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404

# Custom 500 Error Page
@app.errorhandler(500)
def internal_server_error(error):
    return render_template("errors/500.html"), 500

# Run the application
if __name__ == "__main__":
    app.run(debug=True)