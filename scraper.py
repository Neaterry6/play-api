import os
from yt_dlp import YoutubeDL
import requests

COOKIES_FILE = 'cookies.txt'  # Your cookies file in Netscape format

# YT-DLP options with cookie support
YDL_OPTS = {
    'format': 'best',
    'outtmpl': 'downloads/%(title)s.%(ext)s',
    'nocheckcertificate': True,
    'quiet': True,
    'no_warnings': True,
    'cookiefile': COOKIES_FILE,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

def search_songs(query, max_results=10):
    """Search YouTube for videos matching query and return basic info list"""
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
            # Choose best audio format info
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
    os.makedirs('downloads', exist_ok=True)
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'cookiefile': COOKIES_FILE,
        'nocheckcertificate': True,
        'quiet': True,
        'no_warnings': True,
        # Add postprocessors here if you want to merge audio+video
    }
    with YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            filepath = ydl.prepare_filename(info)
            return filepath
        except Exception as e:
            print(f"Error downloading video: {e}")
            return None

def get_lyrics(song_query):
    """
    Get lyrics from free API: lyrics.ovh or fallback to Genius scraping
    song_query: 'artist - song title' or just 'song title'
    """
    # Try lyrics.ovh first
    try:
        artist, song = None, None
        if " - " in song_query:
            artist, song = song_query.split(" - ", 1)
        else:
            song = song_query

        if artist:
            url = f"https://api.lyrics.ovh/v1/{artist.strip()}/{song.strip()}"
        else:
            url = f"https://api.lyrics.ovh/v1//{song.strip()}"

        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get("lyrics", "Lyrics not found.")
    except Exception as e:
        print(f"Error fetching lyrics.ovh API: {e}")

    # Fallback: Simple Genius scraping (basic)
    try:
        import lyricsgenius
        GENIUS_ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")
        if not GENIUS_ACCESS_TOKEN:
            return "No Genius API token set."
        genius = lyricsgenius.Genius(GENIUS_ACCESS_TOKEN, skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"], remove_section_headers=True)
        song = genius.search_song(song_query)
        if song:
            return song.lyrics
        else:
            return "Lyrics not found."
    except Exception as e:
        print(f"Error fetching lyrics from Genius: {e}")
        return "Lyrics not found."

if __name__ == "__main__":
    # quick test
    print("Search results for 'Imagine Dragons':")
    results = search_songs("Imagine Dragons")
    for r in results[:3]:
        print(r['title'], r['url'])
