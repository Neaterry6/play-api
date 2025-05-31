import requests
import yt_dlp
from urllib.parse import quote as url_quote  # ✅ Safe query encoding

COOKIES_PATH = "cookies.txt"
SEARCH_URL = "https://www.youtube.com/results?search_query="
LYRICS_API = "https://api.lyrics.ovh/v1/"

# ✅ Load Netscape cookies properly
def load_cookies():
    cookies = {}
    try:
        with open(COOKIES_PATH, "r") as file:
            for line in file:
                parts = line.strip().split("\t")
                if len(parts) >= 7:
                    cookies[parts[5]] = parts[6]
    except FileNotFoundError:
        print("⚠️ Cookies file missing! Some features may be limited.")
    return cookies

# 🔍 Improved YouTube search function
def search_songs(query):
    cookies = load_cookies()
    encoded_query = url_quote(query)
    response = requests.get(SEARCH_URL + encoded_query, cookies=cookies).text
    results = []  # TODO: Parse actual search results from YouTube
    return results if results else [{"title": "No results found", "video_url": "#"}]

# 🎥 Fetch video metadata (enhanced)
def get_video(query):
    ydl_opts = {"quiet": True, "format": "best"}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)
        if "entries" in info:
            video = info["entries"][0]  # First result
            return {"title": video["title"], "video_url": video["webpage_url"]}
    return {"title": "No video found", "video_url": "#"}

# 🔊 Fetch audio metadata
def get_audio(query):
    return get_video(query)  # Audio can be extracted from video

# 📜 Lyrics fetching (fixed)
def get_lyrics(query):
    try:
        artist, song = query.split(" - ")
        response = requests.get(f"{LYRICS_API}{artist}/{song}")
        return response.json().get("lyrics", "Lyrics not found.")
    except ValueError:
        return "Invalid format. Use 'Artist - Song' format."

# ⬇️ Universal video downloader (uses yt-dlp)
def download_video(video_url):
    ydl_opts = {"quiet": True, "format": "best", "outtmpl": "downloads/%(title)s.%(ext)s"}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(video_url, download=True)
            return info["url"]  # Return the direct video link
        except Exception as e:
            return f"❌ Error downloading video: {str(e)}"
