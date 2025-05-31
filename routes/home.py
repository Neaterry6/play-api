from flask import Blueprint, render_template
from scraper import search_songs

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def index():
    """Homepage displaying latest music and videos."""
    latest_releases = search_songs("latest")  # Fetch latest songs/videos
    return render_template("index.html", latest_releases=latest_releases)

@home_bp.route("/about")
def about():
    """About StreamMe page."""
    return render_template("about.html")

@home_bp.route("/contact")
def contact():
    """Contact page (Optional for user feedback)."""
    return render_template("contact.html")

@home_bp.route("/faq")
def faq():
    """Frequently Asked Questions (Optional section)."""
    return render_template("faq.html"
