from flask import Flask, render_template, request, jsonify
import requests
from scraper import search_songs, get_video, get_audio, get_lyrics, download_video
from dotenv import load_dotenv
import os
from urllib.parse import quote as url_quote  # ✅ Fully Fixed Werkzeug Issue

# Load environment variables
load_dotenv()

app = Flask(__name__)

# 🏠 Home Page
@app.route('/')
def index():
    latest_releases = search_songs("latest")  # ✅ Removed incorrect 'cookies' argument
    return render_template("index.html", latest_releases=latest_releases)

# ℹ️ About Page
@app.route('/about')
def about():
    return render_template("about.html")

# 🔍 Search Page
@app.route('/search', methods=["POST"])
def search():
    query = request.form.get("query")
    if not query:
        return render_template("search.html", error="Please enter a search term.")
    
    results = search_songs(query)  # ✅ Ensures correct argument passing
    return render_template("search.html", results=results)

# 🎵 Play Audio Page
@app.route('/play/audio')
def play_audio():
    query = request.args.get("query")
    if not query:
        return render_template("play_audio.html", error="No audio found.")
    
    audio_data = get_audio(query)
    return render_template("play_audio.html", audio=audio_data)

# 🎥 Play Video Page
@app.route('/play/video')
def play_video():
    query = request.args.get("query")
    if not query:
        return render_template("play_video.html", error="No video found.")
    
    video_data = get_video(query)
    return render_template("play_video.html", video=video_data)

# 📜 Lyrics Page (Using Lyrics.ovh API)
@app.route('/lyrics')
def lyrics():
    artist = request.args.get("artist")
    song = request.args.get("song")

    if not artist or not song:
        return render_template("lyrics.html", error="Please enter both artist name and song title.")

    api_url = f"https://api.lyrics.ovh/v1/{artist}/{song}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        lyrics_data = data.get("lyrics", "Lyrics not found.")
    else:
        lyrics_data = "Lyrics not found or API request failed."

    return render_template("lyrics.html", lyrics=lyrics_data)

# ⬇️ Universal Video Downloader Route
@app.route('/download', methods=["POST"])
def download():
    video_url = request.form.get("video_url")
    if not video_url:
        return render_template("download.html", error="Invalid video URL.")
    
    download_link = download_video(video_url)
    return render_template("download.html", link=download_link)

# 🚀 Run Flask App
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
