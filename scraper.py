import os
from yt_dlp import YoutubeDL
from youtube_search import YoutubeSearch
import requests
from bs4 import BeautifulSoup

# YouTube Search using youtube_search package
def search_songs(query, max_results=10):
    results = YoutubeSearch(query, max_results=max_results).to_dict()
    songs = []
    for item in results:
        songs.append({
            "title": item.get("title"),
            "url_suffix": item.get("url_suffix"),
            "duration": item.get("duration"),
            "thumbnails": item.get("thumbnails"),
            "channel": item.get("channel")
        })
    return songs

# Get video info + streaming url
def get_video(query):
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "format": "bestvideo+bestaudio/best",
    }
    with YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
            return {
                "title": info.get("title"),
                "url": info.get("webpage_url"),
                "thumbnail": info.get("thumbnail"),
                "duration": info.get("duration"),
                "formats": info.get("formats")
            }
        except Exception as e:
            print(f"Error fetching video info: {e}")
            return None

# Get audio info + streaming url
def get_audio(query):
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "format": "bestaudio/best",
    }
    with YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
            return {
                "title": info.get("title"),
                "url": info.get("webpage_url"),
                "thumbnail": info.get("thumbnail"),
                "duration": info.get("duration"),
                "audio_url": info.get("url"),
            }
        except Exception as e:
            print(f"Error fetching audio info: {e}")
            return None

# Get lyrics by scraping lyrics.com (as example)
def get_lyrics(query):
    try:
        # Replace spaces with + for URL search
        search_url = f"https://www.lyrics.com/serp.php?st={query.replace(' ', '+')}&qtype=2"
        res = requests.get(search_url)
        soup = BeautifulSoup(res.text, "html.parser")
        # Find first lyrics link
        link = soup.select_one("td.tal.qx a")
        if link:
            lyrics_page = requests.get(f"https://www.lyrics.com{link['href']}")
            lyrics_soup = BeautifulSoup(lyrics_page.text, "html.parser")
            lyrics_div = lyrics_soup.find("pre", id="lyric-body-text")
            if lyrics_div:
                return lyrics_div.get_text()
        return "Lyrics not found."
    except Exception as e:
        print(f"Error fetching lyrics: {e}")
        return "Lyrics not found."

# Download video from URL (no watermark for TikTok/Facebook/Instagram using yt-dlp)
def download_video(video_url, download_path="downloads"):
    os.makedirs(download_path, exist_ok=True)
    ydl_opts = {
        "outtmpl": f"{download_path}/%(title)s.%(ext)s",
        "format": "best",
        "quiet": True,
        "noplaylist": True,
        # Remove watermark for TikTok and others if possible:
        "postprocessors": [{
            "key": "FFmpegVideoConvertor",
            "preferedformat": "mp4",
        }],
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url)
            filename = ydl.prepare_filename(info)
            return filename  # return path to downloaded file
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None
