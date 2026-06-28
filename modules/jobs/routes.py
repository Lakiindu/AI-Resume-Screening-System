from flask import Blueprint, render_template, request, redirect, url_for, flash
from modules.auth.decorators import login_required
from modules.jobs.services import create_job, get_all_jobs

jobs_bp = Blueprint("jobs", __name__, url_prefix="/jobs")


@jobs_bp.route("/")
@login_required
def index():
    """
    Displays all jobs.
    """
    jobs = get_all_jobs()
    return render_template("jobs/index.html", jobs=jobs)


@jobs_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    """
    Displays add job form and saves job data.
    """
    if request.method == "POST":
        data = {
            "job_title": request.form.get("job_title"),
            "department": request.form.get("department"),
            "location": request.form.get("location"),
            "experience_required": request.form.get("experience_required"),
            "salary": request.form.get("salary"),
            "required_skills": request.form.get("required_skills"),
            "description": request.form.get("description"),
            "status": request.form.get("status")
        }

        create_job(data)

        flash("Job created successfully.", "success")
        return redirect(url_for("jobs.index"))

    return render_template("jobs/create.html")