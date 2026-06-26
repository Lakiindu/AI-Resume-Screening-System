from flask import Flask, render_template
from config import Config
from modules.auth.routes import auth_bp
from modules.dashboard.routes import dashboard_bp

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template("errors/500.html"), 500


if __name__ == "__main__":
    app.run(debug=True)