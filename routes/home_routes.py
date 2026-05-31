"""Home page routes."""
from flask import Blueprint, render_template

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def index():
    """Landing page with branding and feature overview."""
    return render_template("home.html")
