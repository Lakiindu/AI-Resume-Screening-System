from flask import Blueprint, render_template, request, redirect, url_for, flash
from modules.auth.decorators import login_required
from modules.jobs.services import (
    create_job,
    get_all_jobs,
    get_job_by_id,
    update_job,
    delete_job,
    search_jobs,
    get_job_statistics
)

jobs_bp = Blueprint("jobs", __name__, url_prefix="/jobs")


@jobs_bp.route("/")
@login_required
def index():
    """
    Displays all jobs with optional search and sorting.
    """
    keyword = request.args.get("keyword")
    sort = request.args.get("sort", "latest")

    if keyword:
        jobs = search_jobs(keyword, sort)
    else:
        jobs = get_all_jobs(sort)

    stats = get_job_statistics()

    return render_template(
        "jobs/index.html",
        jobs=jobs,
        keyword=keyword,
        sort=sort,
        stats=stats
    )


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


@jobs_bp.route("/<int:job_id>")
@login_required
def view(job_id):
    """
    Displays full details of one job.
    """
    job = get_job_by_id(job_id)

    if not job:
        flash("Job not found.", "danger")
        return redirect(url_for("jobs.index"))

    return render_template("jobs/view.html", job=job)


@jobs_bp.route("/<int:job_id>/edit", methods=["GET", "POST"])
@login_required
def edit(job_id):
    """
    Displays edit form and updates job data.
    """
    job = get_job_by_id(job_id)

    if not job:
        flash("Job not found.", "danger")
        return redirect(url_for("jobs.index"))

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

        update_job(job_id, data)

        flash("Job updated successfully.", "success")
        return redirect(url_for("jobs.view", job_id=job_id))

    return render_template("jobs/edit.html", job=job)


@jobs_bp.route("/<int:job_id>/delete", methods=["POST"])
@login_required
def delete(job_id):
    """
    Deletes selected job.
    """
    job = get_job_by_id(job_id)

    if not job:
        flash("Job not found.", "danger")
        return redirect(url_for("jobs.index"))

    delete_job(job_id)

    flash("Job deleted successfully.", "success")
    return redirect(url_for("jobs.index"))