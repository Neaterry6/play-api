import requests
from youtube_search import YoutubeSearch
import yt_dlp
import re

def search_songs(query, max_results=10):
    """
    Search YouTube for songs/videos matching the query.
    Returns a list of dicts with title, url, duration, and thumbnail.
    """
    results = []
    try:
        yt_results = YoutubeSearch(query, max_results=max_results).to_dict()
        for video in yt_results:
            results.append({
                "title": video.get("title"),
                "url": f"https://www.youtube.com{video.get('url_suffix')}",
                "duration": video.get("duration"),
                "thumbnail": video.get("thumbnails")[0] if video.get("thumbnails") else None
            })
    except Exception as e:
        print(f"Error searching songs: {e}")
    return results

def get_video(query):
    """
    Get video info for the first YouTube result for the query.
    """
    try:
        results = search_songs(query, max_results=1)
        if not results:
            return None
        url = results[0]['url']
        info = get_video_info(url)
        return info
    except Exception as e:
        print(f"Error getting video: {e}")
        return None

def get_audio(query):
    """
    Get audio info for the first YouTube result for the query.
    """
    try:
        results = search_songs(query, max_results=1)
        if not results:
            return None
        url = results[0]['url']
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'forceurl': True,
            'forcejson': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = None
            for f in info.get('formats', []):
                if f.get('acodec') != 'none' and f.get('vcodec') == 'none':
                    audio_url = f.get('url')
                    break
            return {
                'title': info.get('title'),
                'audio_url': audio_url,
                'thumbnail': info.get('thumbnail')
            }
    except Exception as e:
        print(f"Error getting audio: {e}")
        return None

def get_video_info(url):
    """
    Extract detailed video info using yt_dlp.
    """
    try:
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                'title': info.get('title'),
                'url': url,
                'duration': info.get('duration'),
                'thumbnail': info.get('thumbnail'),
                'description': info.get('description'),
                'view_count': info.get('view_count'),
                'upload_date': info.get('upload_date')
            }
    except Exception as e:
        print(f"Error extracting video info: {e}")
        return None

def get_lyrics(query):
    """
    Fetch lyrics using Lyrics.ovh free API.
    Expects query format: "artist - song"
    """
    try:
        if '-' not in query:
            return "Invalid format. Use 'Artist - Song Title'."
        artist, song = map(str.strip, query.split('-', 1))
        url = f"https://api.lyrics.ovh/v1/{artist}/{song}"
        response = requests.get(url)
        data = response.json()

        if 'lyrics' in data and data['lyrics']:
            return data['lyrics']
        else:
            return "Lyrics not found."
    except Exception as e:
        return f"Error fetching lyrics: {str(e)}"

def download_video(url):
    """
    Download video from URL (supports YouTube, TikTok, Instagram, Facebook).
    Attempts to download without watermark where possible.
    Returns path or direct download link.
    """
    try:
        # Use yt_dlp for supported URLs
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
            'noplaylist': True
        }

        # For TikTok, Instagram, Facebook, try no watermark options (if supported)
        if 'tiktok.com' in url:
            ydl_opts['format'] = 'mp4'  # Best mp4 format
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegMetadata',
            }]
            # yt-dlp supports no watermark by default sometimes
        elif 'instagram.com' in url or 'facebook.com' in url:
            # Same options, yt-dlp handles these URLs
            pass

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return filename  # Return saved file path

    except Exception as e:
        print(f"Error downloading video: {e}")
        return None
