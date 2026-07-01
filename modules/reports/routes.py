from flask import Blueprint, render_template, flash, redirect, url_for, send_file
from modules.auth.decorators import login_required

from modules.reports.services import (
    get_candidate_report,
    get_job_report,
    get_match_report,
    get_status_report,
    get_ai_report_data
)

from modules.reports.pdf_export import generate_candidate_report
from modules.reports.pdf_ai_report import generate_ai_report

reports_bp = Blueprint("reports", __name__, url_prefix="/reports")


@reports_bp.route("/")
@login_required
def index():
    candidate_report = get_candidate_report()
    job_report = get_job_report()
    match_report = get_match_report()
    status_report = get_status_report()

    return render_template(
        "reports/index.html",
        candidate_report=candidate_report,
        job_report=job_report,
        match_report=match_report,
        status_report=status_report
    )


@reports_bp.route("/candidate/pdf")
@login_required
def export_candidate_pdf():
    candidate_report = get_candidate_report()

    return generate_candidate_report(candidate_report)


@reports_bp.route("/export-ai-report/<int:resume_id>/<int:job_id>")
@login_required
def export_ai_report(resume_id, job_id):
    data = get_ai_report_data(resume_id, job_id)

    if not data:
        flash("AI report data not found.", "warning")
        return redirect(url_for("reports.index"))

    pdf_buffer = generate_ai_report(data)

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name="ai_candidate_evaluation_report.pdf",
        mimetype="application/pdf"
    )