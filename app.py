import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from dotenv import load_dotenv
from http.cookiejar import MozillaCookieJar
import requests

from scraper import (
    search_songs, get_video, get_audio, get_lyrics, download_video
)

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SECRET_KEY"] = os.getenv("SESSION_SECRET") or "supersecretkey"

db = SQLAlchemy(app)
socketio = SocketIO(app, async_mode="eventlet")

# Load cookies from cookies.txt in Netscape format
cookies_file = "cookies.txt"
cookie_jar = MozillaCookieJar(cookies_file)
try:
    cookie_jar.load(ignore_discard=True, ignore_expires=True)
    print("Cookies loaded successfully from cookies.txt")
except FileNotFoundError:
    print("cookies.txt file not found! Continuing without cookies.")
except Exception as e:
    print(f"Error loading cookies: {e}")

# Create requests session with loaded cookies
session = requests.Session()
session.cookies = cookie_jar

from database.models import Favorite  # Import models after db initialization


@app.route('/')
def index():
    latest_releases = search_songs("latest", session=session)
    return render_template("index.html", latest_releases=latest_releases)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/search', methods=["POST"])
def search():
    query = request.form.get("query")
    if not query:
        return render_template("search.html", error="Please enter a search term.")
    results = search_songs(query, session=session)
    return render_template("search.html", results=results)


@app.route('/play/audio')
def play_audio():
    query = request.args.get("query")
    if not query:
        return render_template("play_audio.html", error="No audio found.")
    audio_data = get_audio(query, session=session)
    return render_template("play_audio.html", audio=audio_data)


@app.route('/play/video')
def play_video():
    query = request.args.get("query")
    if not query:
        return render_template("play_video.html", error="No video found.")
    video_data = get_video(query, session=session)
    return render_template("play_video.html", video=video_data)


@app.route('/lyrics')
def lyrics():
    artist = request.args.get("artist")
    song = request.args.get("song")
    if not artist or not song:
        return render_template("lyrics.html", error="Please enter both artist name and song title.")
    lyrics_data = get_lyrics(f"{artist} - {song}", session=session)
    return render_template("lyrics.html", lyrics=lyrics_data)


@app.route('/download', methods=["POST"])
def download():
    video_url = request.form.get("video_url")
    if not video_url:
        return render_template("download.html", error="Invalid video URL.")
    download_link = download_video(video_url, session=session)
    return render_template("download.html", link=download_link)


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


# SocketIO events

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
