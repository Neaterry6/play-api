
from flask import Blueprint, render_template, request
from scraper import get_video, get_audio, get_lyrics, download_video
from database.models import Favorite
from app import db

media_bp = Blueprint('media', __name__)

@media_bp.route('/play/audio')
def play_audio():
    query = request.args.get("query")
    if not query:
        return render_template("play_audio.html", error="No audio found.")
    audio_data = get_audio(query)
    return render_template("play_audio.html", audio=audio_data)

@media_bp.route('/play/video')
def play_video():
    query = request.args.get("query")
    if not query:
        return render_template("play_video.html", error="No video found.")
    video_data = get_video(query)
    return render_template("play_video.html", video=video_data)

@media_bp.route('/lyrics')
def lyrics():
    artist = request.args.get("artist")
    song = request.args.get("song")
    if not artist or not song:
        return render_template("lyrics.html", error="Please enter both artist name and song title.")
    lyrics_data = get_lyrics(f"{artist} - {song}")
    return render_template("lyrics.html", lyrics=lyrics_data)

@media_bp.route('/download', methods=["POST"])
def download():
    video_url = request.form.get("video_url")
    if not video_url:
        return render_template("download.html", error="Invalid video URL.")
    download_link = download_video(video_url)
    return render_template("download.html", link=download_link)

@media_bp.route('/favorites', methods=["GET", "POST"])
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
