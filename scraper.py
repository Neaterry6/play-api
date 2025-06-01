import os
import requests
from yt_dlp import YoutubeDL

COOKIES_FILE = 'cookies.txt'  # Your YouTube cookies file (if needed)

# YT-DLP Options for Searching & Downloading
YDL_OPTS = {
    'format': 'best',
    'outtmpl': 'static/videos/%(title)s.%(ext)s',
    'nocheckcertificate': True,
    'quiet': True,
    'no_warnings': True,
    'cookiefile': COOKIES_FILE,
    'merge_output_format': 'mp4',
}

def search_songs(query, max_results=10):
    """Search YouTube for videos matching query"""
    search_query = f"ytsearch{max_results}:{query}"
    with YoutubeDL({'quiet': True, 'cookiefile': COOKIES_FILE}) as ydl:
        try:
            results = ydl.extract_info(search_query, download=False)
            videos = results.get('entries', [])
            return [{
                'id': video.get('id'),
                'title': video.get('title'),
                'url': video.get('webpage_url'),
                'duration': video.get('duration'),
                'thumbnail': video.get('thumbnail')
            } for video in videos]
        except Exception as e:
            print(f"Error searching songs: {e}")
            return []

def get_video(url):
    """Get video info without downloading"""
    with YoutubeDL({'quiet': True, 'cookiefile': COOKIES_FILE}) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return {
                'title': info.get('title'),
                'url': info.get('webpage_url'),
                'duration': info.get('duration'),
                'thumbnail': info.get('thumbnail'),
                'formats': info.get('formats'),
            }
        except Exception as e:
            print(f"Error getting video info: {e}")
            return None

def get_audio(url):
    """Get best audio info without downloading"""
    opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'cookiefile': COOKIES_FILE,
    }
    with YoutubeDL(opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            audio_formats = [f for f in info.get('formats', []) if f.get('acodec') != 'none']
            best_audio = max(audio_formats, key=lambda f: f.get('abr', 0)) if audio_formats else None
            return {
                'title': info.get('title'),
                'url': info.get('webpage_url'),
                'duration': info.get('duration'),
                'thumbnail': info.get('thumbnail'),
                'audio_url': best_audio.get('url') if best_audio else None,
            }
        except Exception as e:
            print(f"Error getting audio info: {e}")
            return None

def download_video(url):
    """Download video and return local path"""
    os.makedirs('static/videos', exist_ok=True)
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': 'static/videos/%(title)s.%(ext)s',
        'cookiefile': COOKIES_FILE,
        'nocheckcertificate': True,
        'quiet': True,
        'no_warnings': True,
        'merge_output_format': 'mp4',
    }
    with YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            filepath = ydl.prepare_filename(info)
            return os.path.basename(filepath)
        except Exception as e:
            print(f"Error downloading video: {e}")
            return None

def get_lyrics(song_query):
    """
    Get lyrics using the Lyrics.ovh API
    """
    try:
        artist, title = song_query.split(" - ")  # Extract artist & song title
        response = requests.get(f"https://api.lyrics.ovh/v1/{artist}/{title}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("lyrics"):
                return f"🎶 {title} by {artist}\n\n{data.get('lyrics')}"
            else:
                return "❌ No lyrics found for this track."
        else:
            return "❌ Failed to fetch lyrics."
    except Exception as e:
        print(f"Error fetching lyrics: {e}")
        return "❌ Error fetching lyrics."

if __name__ == "__main__":
    print("Search results for 'Imagine Dragons':")
    results = search_songs("Imagine Dragons")
    for r in results[:3]:
        print(r['title'], r['url'])
