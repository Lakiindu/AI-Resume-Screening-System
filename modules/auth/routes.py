from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from modules.auth.decorators import login_required
from modules.auth.services import (
    authenticate_user,
    get_user_by_id,
    update_profile,
    update_password
)

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Handles admin login.
    """
    if "user_id" in session:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = authenticate_user(email, password)

        if user:
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            session["user_email"] = user["email"]

            flash("Login successful.", "success")
            return redirect(url_for("dashboard.index"))

        flash("Invalid email or password.", "danger")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    """
    Logs out admin by clearing session.
    """
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """
    Displays and updates admin profile.
    """
    user = get_user_by_id(session["user_id"])

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")

        update_profile(session["user_id"], name, email)

        session["user_name"] = name
        session["user_email"] = email

        flash("Profile updated successfully.", "success")
        return redirect(url_for("auth.profile"))

    return render_template("auth/profile.html", user=user)


@auth_bp.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    """
    Allows admin to change password.
    """
    user = get_user_by_id(session["user_id"])

    if request.method == "POST":
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        if not check_password_hash(user["password"], current_password):
            flash("Current password is incorrect.", "danger")
            return redirect(url_for("auth.change_password"))

        if new_password != confirm_password:
            flash("New password and confirm password do not match.", "danger")
            return redirect(url_for("auth.change_password"))

        if len(new_password) < 6:
            flash("Password must be at least 6 characters long.", "warning")
            return redirect(url_for("auth.change_password"))

        update_password(session["user_id"], new_password)

        flash("Password changed successfully. Please login again.", "success")
        session.clear()
        return redirect(url_for("auth.login"))

    return render_template("auth/change_password.html")