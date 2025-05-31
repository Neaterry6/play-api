from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
import requests
from scraper import search_songs, get_video, get_audio, get_lyrics, download_video
from dotenv import load_dotenv
import os

# ✅ Load environment variables
load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SECRET_KEY"] = os.getenv("SESSION_SECRET")
db = SQLAlchemy(app)
socketio = SocketIO(app)

# 🏠 Home Page
@app.route('/')
def index():
    latest_releases = search_songs("latest")
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
    
    results = search_songs(query)
    return render_template("search.html", results=results)

# 🎵 Play Audio Page (With Effects & Speed Control)
@app.route('/play/audio')
def play_audio():
    query = request.args.get("query")
    if not query:
        return render_template("play_audio.html", error="No audio found.")
    
    audio_data = get_audio(query)
    return render_template("play_audio.html", audio=audio_data)

# 🎥 Play Video Page (With Speed Control)
@app.route('/play/video')
def play_video():
    query = request.args.get("query")
    if not query:
        return render_template("play_video.html", error="No video found.")
    
    video_data = get_video(query)
    return render_template("play_video.html", video=video_data)

# 📜 Lyrics Page
@app.route('/lyrics')
def lyrics():
    artist = request.args.get("artist")
    song = request.args.get("song")

    if not artist or not song:
        return render_template("lyrics.html", error="Please enter both artist name and song title.")

    lyrics_data = get_lyrics(f"{artist} - {song}")
    return render_template("lyrics.html", lyrics=lyrics_data)

# ⬇️ Video Downloader Route
@app.route('/download', methods=["POST"])
def download():
    video_url = request.form.get("video_url")
    if not video_url:
        return render_template("download.html", error="Invalid video URL.")
    
    download_link = download_video(video_url)
    return render_template("download.html", link=download_link)

# ❤️ Favorites Page
@app.route('/favorites', methods=["GET", "POST"])
def favorites():
    from models import Favorite

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

# 💬 Chatroom Functionality
users = {}

@socketio.on("join")
def handle_join(nickname):
    users[request.sid] = nickname
    socketio.emit("message", {"nickname": "System", "text": f"{nickname} joined the chat!"})

@socketio.on("message")
def handle_message(data):
    socketio.emit("message", data)

@socketio.on("disconnect")
def handle_disconnect():
    nickname = users.pop(request.sid, "Unknown")
    socketio.emit("message", {"nickname": "System", "text": f"{nickname} left the chat."})

# 🚀 Run Flask App
if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
