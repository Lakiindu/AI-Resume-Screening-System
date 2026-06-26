from flask import Flask
from config import Config
from modules.auth.routes import auth_bp
from modules.dashboard.routes import dashboard_bp

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)


if __name__ == "__main__":
    app.run(debug=True)