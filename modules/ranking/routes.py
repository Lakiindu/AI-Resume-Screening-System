from flask import Blueprint, render_template, request
from modules.auth.decorators import login_required
from modules.ranking.services import (
    get_candidate_rankings,
    get_ranking_statistics,
    get_top_candidate
)

ranking_bp = Blueprint("ranking", __name__, url_prefix="/ranking")


@ranking_bp.route("/")
@login_required
def index():
    keyword = request.args.get("keyword")
    recommendation = request.args.get("recommendation")

    rankings = get_candidate_rankings(keyword, recommendation)
    stats = get_ranking_statistics()
    top_candidate = get_top_candidate()

    return render_template(
        "ranking/index.html",
        rankings=rankings,
        stats=stats,
        top_candidate=top_candidate,
        keyword=keyword,
        recommendation=recommendation
    )