import yt_dlp
from pathlib import Path

def get_playlist_info(url: str):
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": "in_playlist",
        "skip_download": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
    videos = []
    for index, entry in enumerate(info.get("entries") or [], start=1):
        if not entry:
            continue
        videos.append({
            "index": index,
            "id": entry.get("id"),
            "title": entry.get("title"),
            "url": entry.get("url"),
        })
    return {
        "playlist_title": info.get("title"),
        "playlist_id": info.get("id"),
        "video_count": len(videos),
        "videos": videos,
    }

def download_playlist(url: str,quality: str = "1080p"):
    height = quality.replace("p", "")
    ydl_opts = {
        "format": f"bestvideo[height<={height}]+bestaudio/best",
        "merge_output_format": "mp4",
        "outtmpl": "downloads/%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s",
        "noplaylist": False,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
    return {
        "playlist_title": info.get("title"),
        "status": "completed"
    }