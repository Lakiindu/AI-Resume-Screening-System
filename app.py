from flask import Flask, render_template, session, redirect, url_for
from config import Config
from modules.auth.routes import auth_bp

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(auth_bp)


@app.route("/")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    return render_template("dashboard/index.html")


if __name__ == "__main__":
    app.run(debug=True)