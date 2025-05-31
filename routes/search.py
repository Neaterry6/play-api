from flask import Blueprint, request, render_template
from scraper import search_songs

search_bp = Blueprint("search", __name__)

@search_bp.route("/search", methods=["POST"])
def search():
    query = request.form.get("query")
    if not query:
        return render_template("search.html", error="Please enter a search term.")
    
    results = search_songs(query)
    return render_template("search.html", results=results
