from flask import Flask, render_template, request, send_from_directory, jsonify
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename
import os
from utils.scraper import download_video, get_lyrics  # <-- fixed import, your scraper uses get_lyrics, not fetch_lyrics
from utils.ai_chat import get_ai_reply
from datetime import datetime

# App setup
app = Flask(__name__)
socketio = SocketIO(app)

# Upload folders
UPLOAD_FOLDER = 'static/uploads'
VIDEOS_FOLDER = 'static/videos'
AUDIOS_FOLDER = 'static/audios'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(VIDEOS_FOLDER):
    os.makedirs(VIDEOS_FOLDER)
if not os.path.exists(AUDIOS_FOLDER):
    os.makedirs(AUDIOS_FOLDER)

# Home route — list downloaded videos & audios
@app.route('/')
def home():
    video_files = os.listdir(VIDEOS_FOLDER)
    audio_files = os.listdir(AUDIOS_FOLDER)
    return render_template('index.html', videos=video_files, audios=audio_files)

# Video/Audio search page
@app.route('/search')
def search():
    return render_template('search.html')

# Download page (download video and save to static/videos)
@app.route('/download', methods=["GET", "POST"])
def download():
    video_url = ""
    filename = ""
    error = ""

    if request.method == "POST":
        video_url = request.form.get("video_url")
        if not video_url:
            error = "Please provide a video URL."
        else:
            try:
                # download_video() should save the file in static/videos folder
                # So override the output path inside download_video to VIDEOS_FOLDER
                filename = download_video(video_url, output_dir=VIDEOS_FOLDER)
            except Exception as e:
                error = str(e)

    return render_template("download.html", video_url=video_url, filename=filename, error=error)

# Serve downloaded videos
@app.route('/videos/<filename>')
def serve_video(filename):
    return send_from_directory(VIDEOS_FOLDER, filename)

# Serve downloaded audios
@app.route('/audios/<filename>')
def serve_audio(filename):
    return send_from_directory(AUDIOS_FOLDER, filename)

# Lyrics page — accepts "track" and "artist" from form and calls get_lyrics from scraper
@app.route('/lyrics', methods=["GET", "POST"])
def lyrics():
    lyrics_result = ""
    if request.method == "POST":
        track = request.form.get("track")
        artist = request.form.get("artist")
        if not track:
            lyrics_result = "Please enter the track name."
        else:
            query = f"{artist} - {track}" if artist else track
            lyrics_result = get_lyrics(query)
    return render_template("lyrics.html", lyrics=lyrics_result)

# Chatroom page
@app.route('/chatroom')
def chatroom():
    return render_template("chatroom.html")

# FAQ page
@app.route('/faq')
def faq():
    return render_template("faq.html")

# Contact page
@app.route('/contact')
def contact():
    return render_template("contact.html")

# AI Chat page
@app.route('/ai_chat', methods=["GET", "POST"])
def ai_chat():
    user_message = ""
    ai_response = ""

    if request.method == "POST":
        user_message = request.form.get("user_message")
        if user_message:
            ai_response = get_ai_reply(user_message)

    return render_template("ai_chat.html", user_message=user_message, ai_response=ai_response)

# Upload image or voice to chatroom
@app.route('/upload', methods=["POST"])
def upload():
    file = request.files.get('file')
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({'file_url': f"/static/uploads/{filename}"})
    return jsonify({'error': 'Upload failed'})

# SocketIO real-time messaging
@socketio.on('message')
def handle_message(msg):
    print(f"[{datetime.now()}] Message: {msg}")
    emit('message', msg, broadcast=True)

# AI auto reply in chatroom
@socketio.on('ai_message')
def handle_ai_message(data):
    user_text = data.get('text')
    ai_reply = get_ai_reply(user_text)
    emit('ai_message', {'text': ai_reply}, broadcast=True)

# Run the app
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)