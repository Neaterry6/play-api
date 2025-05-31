import yt_dlp
import os
import re
import requests

COOKIES_PATH = "cookies.txt"  # Your YouTube cookies file, keep private
DOWNLOAD_FOLDER = "downloads"

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def get_yt_info(url):
    ydl_opts = {
        'cookiefile': COOKIES_PATH,
        'format': 'bestvideo+bestaudio/best',
        'quiet': True,
        'skip_download': True,
        'noplaylist': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
    return info

def search_youtube(query, max_results=5):
    ydl_opts = {
        'cookiefile': COOKIES_PATH,
        'quiet': True,
        'skip_download': True,
        'default_search': 'ytsearch',
        'max_downloads': max_results,
        'noplaylist': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(query, download=False)
    return result.get('entries', [])

def download_any_video_no_watermark(url):
    """
    Downloads video from URL (YouTube, TikTok, FB, Instagram, etc) and attempts no watermark for TikTok.
    Returns path to downloaded file.
    """
    if "tiktok.com" in url:
        # For TikTok, try no watermark via external service or API
        return download_tiktok_no_watermark(url)
    else:
        # General download using yt-dlp
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'quiet': True,
            'nocheckcertificate': True,
            'noplaylist': True,
            'cookiefile': COOKIES_PATH,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        return filename

def download_tiktok_no_watermark(url):
    """
    Uses the free TikTok no watermark downloader API to fetch no watermark video.
    This method downloads video manually and saves it.
    """
    # Here is a free API example — you can change if it breaks:
    API_URL = "https://api.tikmate.app/api/lookup"
    params = {"url": url}
    r = requests.get(API_URL, params=params)
    if r.status_code != 200:
        raise Exception("TikTok API lookup failed")

    data = r.json()
    # Get highest quality no watermark video URL
    no_wm_url = None
    for video in data.get("video", []):
        if video.get("watermark") is False:
            no_wm_url = video.get("url")
            break

    if not no_wm_url:
        # fallback to any available video URL
        no_wm_url = data.get("video")[0].get("url")

    # Download video manually
    local_filename = os.path.join(DOWNLOAD_FOLDER, "tiktok_no_wm.mp4")
    with requests.get(no_wm_url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    return local_filenam
