from flask import Blueprint, render_template, request, redirect, url_for, flash
from modules.auth.decorators import login_required
from modules.candidates.services import (
    get_all_candidates,
    get_candidate_statistics,
    update_candidate_status
)

candidates_bp = Blueprint("candidates", __name__, url_prefix="/candidates")


@candidates_bp.route("/")
@login_required
def index():
    keyword = request.args.get("keyword")
    status = request.args.get("status")

    candidates = get_all_candidates(keyword, status)
    stats = get_candidate_statistics()

    return render_template(
        "candidates/index.html",
        candidates=candidates,
        stats=stats,
        keyword=keyword,
        status=status
    )


@candidates_bp.route("/<int:candidate_id>/status", methods=["POST"])
@login_required
def update_status(candidate_id):
    status = request.form.get("status")

    if status not in ["pending", "shortlisted", "rejected"]:
        flash("Invalid candidate status.", "danger")
        return redirect(url_for("candidates.index"))

    update_candidate_status(candidate_id, status)

    flash("Candidate status updated successfully.", "success")
    return redirect(url_for("candidates.index"))