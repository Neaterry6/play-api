from flask import Flask, jsonify, request, render_template
from scraper import search_songs, get_video, get_audio, get_lyrics, download_video

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/search', methods=["GET", "POST"])
def search():
    if request.method == "POST":
        query = request.form.get("query")
        results = search_songs(query)
        return render_template("search.html", results=results)
    return render_template("search.html")

@app.route('/play/audio')
def play_audio():
    query = request.args.get("query")
    audio_data = get_audio(query)
    return render_template("play_audio.html", audio=audio_data)

@app.route('/play/video')
def play_video():
    query = request.args.get("query")
    video_data = get_video(query)
    return render_template("play_video.html", video=video_data)

@app.route('/lyrics')
def lyrics():
    query = request.args.get("query")
    lyrics_data = get_lyrics(query)
    return render_template("lyrics.html", lyrics=lyrics_data)

@app.route('/download', methods=["GET", "POST"])
def download():
    if request.method == "POST":
        video_url = request.form.get("video_url")
        download_link = download_video(video_url)
        return render_template("download.html", link=download_link)
    return render_template("download.html")

if __name__ == '__main__':
    app.run(debug=True)
