from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from dotenv import load_dotenv
from urllib.parse import quote as url_quote  # Werkzeug-safe URL quoting
import os

# Local module imports
from scraper import search_songs, get_video, get_audio, get_lyrics, download_video

# Load environment variables
load_dotenv()

# Flask App Setup
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SECRET_KEY"] = os.getenv("SESSION_SECRET")

# Database & SocketIO
db = SQLAlchemy(app)
socketio = SocketIO(app, async_mode="eventlet")

# ------------------- Routes ----------------------

# 🏠 Home Page
@app.route('/')
def index():
    latest_videos = search_songs("latest_videos")
    latest_audios = search_songs("latest_audios")
    return render_template("index.html", latest_videos=latest_videos, latest_audios=latest_audios)

# ℹ️ About Page
@app.route('/about')
def about():
    return render_template("about.html")

# ❔ FAQ Page
@app.route('/faq')
def faq():
    return render_template("faq.html")

# 📩 Contact Page
@app.route('/contact')
def contact():
    return render_template("contact.html")

# 🤖 AI Chat Feature (if implemented)
@app.route('/ai_chat')
def ai_chat():
    return render_template("ai_chat.html")

# 🔍 Search Songs Page
@app.route('/search', methods=["GET", "POST"])
def search():
    if request.method == "POST":
        query = request.form.get("query")
        if not query:
            return render_template("search.html", error="Please enter a search term.")
        results = search_songs(query)
        return render_template("search.html", results=results)
    return render_template("search.html")

# 🎵 Dedicated Audio Page
@app.route('/audio')
def audio():
    latest_audios = search_songs("latest_audios")
    return render_template("audio.html", latest_audios=latest_audios)

# 🎥 Dedicated Video Page
@app.route('/video')
def video():
    latest_videos = search_songs("latest_videos")
    return render_template("video.html", latest_videos=latest_videos)

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

# 📜 Lyrics Page
@app.route('/lyrics')
def lyrics():
    artist = request.args.get("artist")
    song = request.args.get("song")
    if not artist or not song:
        return render_template("lyrics.html", error="Please enter both artist and song.")
    lyrics_data = get_lyrics(f"{artist} - {song}")
    return render_template("lyrics.html", lyrics=lyrics_data)

# ⬇️ Video Downloader
@app.route('/download', methods=["GET", "POST"])
def download():
    if request.method == "POST":
        video_url = request.form.get("video_url")
        if not video_url:
            return render_template("download.html", error="Please enter a video URL.")
        download_link = download_video(video_url)
        return render_template("download.html", link=download_link)
    return render_template("download.html")

# ❤️ Favorites Page
@app.route('/favorites', methods=["GET", "POST"])
def favorites():
    from models import Favorite  # Local import to avoid circular dependency

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

# 💬 Real-Time Chatroom
users = {}

@app.route('/chatroom')
def chatroom():
    return render_template("chatroom.html")

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

# ----------------- Run Flask App -----------------

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)