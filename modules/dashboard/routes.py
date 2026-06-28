from flask import Blueprint, render_template
from modules.auth.decorators import login_required
from modules.dashboard.services import get_dashboard_statistics

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
def index():
    stats = get_dashboard_statistics()
    return render_template("dashboard/index.html", stats=stats)