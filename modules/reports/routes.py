from flask import Blueprint, render_template
from modules.auth.decorators import login_required
from modules.reports.services import (
    get_candidate_report,
    get_job_report,
    get_match_report,
    get_status_report
)

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