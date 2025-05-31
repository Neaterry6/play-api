import os
from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from dotenv import load_dotenv
from scraper import search_songs, get_video, get_audio, get_lyrics, download_video

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SECRET_KEY"] = os.getenv("SESSION_SECRET") or "supersecretkey"

db = SQLAlchemy(app)
socketio = SocketIO(app, async_mode="eventlet")

from database.models import Favorite

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

@app.route('/download', methods=["GET", "POST"])
def download():
    if request.method == "POST":
        video_url = request.form.get("video_url")
        if not video_url:
            return render_template("download.html", error="Please provide a valid video URL.")

        file_path = download_video(video_url)
        if not file_path:
            return render_template("download.html", error="Failed to download video.")
        
        # Send the file for download to user
        return send_file(file_path, as_attachment=True)

    return render_template("download.html")

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
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
