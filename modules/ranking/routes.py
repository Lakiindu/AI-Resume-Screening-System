from flask import Blueprint, render_template
from modules.auth.decorators import login_required
from modules.ranking.services import get_candidate_rankings

ranking_bp = Blueprint(
    "ranking",
    __name__,
    url_prefix="/ranking"
)


@ranking_bp.route("/")
@login_required
def index():
    rankings = get_candidate_rankings()

    return render_template(
        "ranking/index.html",
        rankings=rankings
    )