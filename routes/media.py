from flask import Blueprint, request, render_template
from scraper import get_video, get_audio, download_video

media_bp = Blueprint("media", __name__)

@media_bp.route("/play/audio")
def play_audio():
    query = request.args.get("query")
    if not query:
        return render_template("play_audio.html", error="No audio found.")
    
    audio_data = get_audio(query)
    return render_template("play_audio.html", audio=audio_data)

@media_bp.route("/play/video")
def play_video():
    query = request.args.get("query")
    if not query:
        return render_template("play_video.html", error="No video found.")
    
    video_data = get_video(query)
    return render_template("play_video.html", video=video_data)

@media_bp.route("/download", methods=["POST"])
def download():
    video_url = request.form.get("video_url")
    if not video_url:
        return render_template("download.html", error="Please enter a valid video link.")
    
    # Calls scraper function to process download
    download_link = download_video(video_url)

    if not download_link:
        return render_template("download.html", error="Failed to download video. Try another link.")
    
    return render_template("download.html", link=download_link)
