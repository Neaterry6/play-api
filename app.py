import os
from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from dotenv import load_dotenv

from scraper import search_songs, get_video, get_audio, get_lyrics
from yt_utils import search_youtube, get_yt_info, download_any_video_no_watermark

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SECRET_KEY"] = os.getenv("SESSION_SECRET") or "supersecretkey"

db = SQLAlchemy(app)
socketio = SocketIO(app, async_mode="eventlet")

from database.models import Favorite

# Routes...

@app.route('/')
def index():
    latest_releases = search_songs("latest")
    return render_template("index.html", latest_releases=latest_releases)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/search', methods=["POST"])
def search():
    query = request.form.get("query")
    if not query:
        return render_template("search.html", error="Please enter a search term.")
    results = search_songs(query)
    return render_template("search.html", results=results)

@app.route('/play/audio')
def play_audio():
    query = request.args.get("query")
    if not query:
        return render_template("play_audio.html", error="No audio found.")
    audio_data = get_audio(query)
    return render_template("play_audio.html", audio=audio_data)

@app.route('/play/video')
def play_video():
    query = request.args.get("query")
    if not query:
        return render_template("play_video.html", error="No video found.")
    video_data = get_video(query)
    return render_template("play_video.html", video=video_data)

@app.route('/lyrics')
def lyrics():
    artist = request.args.get("artist")
    song = request.args.get("song")
    if not artist or not song:
        return render_template("lyrics.html", error="Please enter both artist name and song title.")
    lyrics_data = get_lyrics(f"{artist} - {song}")
    return render_template("lyrics.html", lyrics=lyrics_data)

@app.route('/favorites', methods=["GET", "POST"])
def favorites():
    if request.method == "POST":
        user_id = request.form.get("user_id")
        song_title = request.form.get("song_title")
        song_url = request.form.get("song_url")

        if user_id and song_title and song_url:
            favorite = Favorite(user_id=user_id, song_title=song_title, song_url=song_url)
            db.session.add(favorite)
            db.session.commit()

    user_favorites = Favorite.query.all()
    return render_template("favorites.html", favorites=user_favorites)

# YouTube search & playback routes

@app.route('/yt/search', methods=["GET", "POST"])
def yt_search():
    query = request.args.get("query") or request.form.get("query")
    if not query:
        return render_template("search.html", error="Please enter a search term for YouTube.")
    results = search_youtube(query)
    return render_template("search.html", results=results, source="youtube")

@app.route('/yt/video')
def yt_video():
    video_url = request.args.get("url")
    if not video_url:
        return render_template("play_video.html", error="No video URL provided.")
    video_info = get_yt_info(video_url)
    return render_template("play_video.html", video=video_info)

@app.route('/yt/audio')
def yt_audio():
    audio_url = request.args.get("url")
    if not audio_url:
        return render_template("play_audio.html", error="No audio URL provided.")
    audio_info = get_yt_info(audio_url)
    return render_template("play_audio.html", audio=audio_info)

# Download route for any video (YouTube, TikTok, Instagram, Facebook, etc)

@app.route('/download', methods=["GET", "POST"])
def download():
    if request.method == "POST":
        video_url = request.form.get("video_url")
        if not video_url:
            return render_template("download.html", error="Invalid video URL.")
        try:
            filepath = download_any_video_no_watermark(video_url)
            return send_file(filepath, as_attachment=True)
        except Exception as e:
            return render_template("download.html", error=f"Download failed: {str(e)}")
    else:
        return render_template("download.html")

# SocketIO events (same as before)...

users = {}

@socketio.on("join")
def handle_join(nickname):
    users[request.sid] = nickname
    socketio.emit("message", {"nickname": "System", "text": f"{nickname} joined the chat!"})

@socketio.on("message")
def handle_message(data):
    socketio.emit("message", data)

@socketio.on("image")
def handle_image(data):
    socketio.emit("image", data)

@socketio.on("voice")
def handle_voice(data):
    socketio.emit("voice", data)

@socketio.on("disconnect")
def handle_disconnect():
    nickname = users.pop(request.sid, "Unknown")
    socketio.emit("message", {"nickname": "System", "text": f"{nickname} left the chat."})

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True
