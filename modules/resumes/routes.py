import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from config import Config
from modules.auth.decorators import login_required

from modules.resumes.parser import parse_resume

from modules.resumes.services import (
    save_resume,
    get_all_resumes,
    get_resume_by_id,
    delete_resume_record,
    search_resumes,
    is_duplicate_resume,
    save_resume_details
)

from modules.resumes.utils import (
    allowed_file,
    generate_unique_filename,
    ensure_upload_folder_exists
)

resumes_bp = Blueprint("resumes", __name__, url_prefix="/resumes")


@resumes_bp.route("/")
@login_required
def index():
    keyword = request.args.get("keyword")

    if keyword:
        resumes = search_resumes(keyword)
    else:
        resumes = get_all_resumes()

    return render_template("resumes/index.html", resumes=resumes, keyword=keyword)


@resumes_bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    """
    Uploads PDF resume and saves file data.
    """
    if request.method == "POST":
        candidate_name = request.form.get("candidate_name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        file = request.files.get("resume_file")

        if not file or file.filename == "":
            flash("Please select a resume file.", "warning")
            return redirect(url_for("resumes.upload"))

        if not allowed_file(file.filename):
            flash("Only PDF files are allowed.", "danger")
            return redirect(url_for("resumes.upload"))

        if is_duplicate_resume(file.filename):
            flash("This resume has already been uploaded.", "warning")
            return redirect(url_for("resumes.upload"))

        ensure_upload_folder_exists()

        stored_filename = generate_unique_filename(file.filename)
        file_path = os.path.join(Config.UPLOAD_FOLDER, stored_filename)

        file.save(file_path)

        file_size = os.path.getsize(file_path)

        data = {
            "candidate_name": candidate_name,
            "email": email,
            "phone": phone,
            "original_filename": file.filename,
            "stored_filename": stored_filename,
            "file_path": file_path,
            "file_size": file_size
        }

        save_resume(data)

        flash("Resume uploaded successfully.", "success")
        return redirect(url_for("resumes.index"))

    return render_template("resumes/upload.html")


@resumes_bp.route("/<int:resume_id>/parse", methods=["POST"])
@login_required
def parse(resume_id):
    """
    Parses selected resume PDF and saves extracted data.
    """
    resume = get_resume_by_id(resume_id)

    if not resume:
        flash("Resume not found.", "danger")
        return redirect(url_for("resumes.index"))

    parsed_data = parse_resume(resume["file_path"])

    save_resume_details(resume_id, parsed_data)

    flash("Resume parsed successfully.", "success")
    return redirect(url_for("resumes.index"))


@resumes_bp.route("/<int:resume_id>/preview")
@login_required
def preview(resume_id):
    resume = get_resume_by_id(resume_id)

    if not resume:
        flash("Resume not found.", "danger")
        return redirect(url_for("resumes.index"))

    return send_file(resume["file_path"], as_attachment=False)


@resumes_bp.route("/<int:resume_id>/download")
@login_required
def download(resume_id):
    resume = get_resume_by_id(resume_id)

    if not resume:
        flash("Resume not found.", "danger")
        return redirect(url_for("resumes.index"))

    return send_file(
        resume["file_path"],
        as_attachment=True,
        download_name=resume["original_filename"]
    )


@resumes_bp.route("/<int:resume_id>/delete", methods=["POST"])
@login_required
def delete(resume_id):
    resume = get_resume_by_id(resume_id)

    if not resume:
        flash("Resume not found.", "danger")
        return redirect(url_for("resumes.index"))

    if os.path.exists(resume["file_path"]):
        os.remove(resume["file_path"])

    delete_resume_record(resume_id)

    flash("Resume deleted successfully.", "success")
    return redirect(url_for("resumes.index"))