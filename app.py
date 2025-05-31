from flask import Flask, render_template, request, jsonify, url_for
from scraper import search_songs, get_video, get_audio, get_lyrics, download_video

app = Flask(__name__, static_url_path='/static')

# 🏠 Home Page
@app.route('/')
def index():
    return render_template("index.html")

# ℹ️ About Page
@app.route('/about')
def about():
    return render_template("about.html")

# 🔍 Search Page (Fetch Multiple Results)
@app.route('/search', methods=["GET", "POST"])
def search():
    if request.method == "POST":
        query = request.form.get("query")
        results = search_songs(query)
        return render_template("search.html", results=results)
    return render_template("search.html")

# 🎵 Play Audio Page
@app.route('/play/audio')
def play_audio():
    query = request.args.get("query")
    audio_data = get_audio(query)
    return render_template("play_audio.html", audio=audio_data)

# 🎥 Play Video Page
@app.route('/play/video')
def play_video():
    query = request.args.get("query")
    video_data = get_video(query)
    return render_template("play_video.html", video=video_data)

# 📜 Lyrics Page
@app.route('/lyrics')
def lyrics():
    query = request.args.get("query")
    lyrics_data = get_lyrics(query)
    return render_template("lyrics.html", lyrics=lyrics_data)

# ⬇️ Download Page
@app.route('/download', methods=["GET", "POST"])
def download():
    if request.method == "POST":
        video_url = request.form.get("video_url")
        download_link = download_video(video_url)
        return render_template("download.html", link=download_link)
    return render_template("download.html")

# 🔧 Ensure Static Files Load Properly
@app.route('/static/<path:filename>')
def static_files(filename):
    return url_for('static', filename=filename)

# 🚀 Run Flask App
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000, debug=True)
