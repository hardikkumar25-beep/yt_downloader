import yt_dlp
from pathlib import Path
from yt_dlp.utils import DownloadError

DOWNLOAD_DIR = Path("downloads")
DOWNLOAD_DIR.mkdir(exist_ok=True)

def download_video(url: str, quality: str = "1080p"):
    ydl_opts = {
        "format": f"bestvideo[height<={quality.replace('p', '')}]+bestaudio/best",
        "merge_output_format": "mp4",
        "outtmpl": str(DOWNLOAD_DIR / "%(title)s.%(ext)s"),
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

    return {
        "title": info.get("title"),
        "filename": ydl.prepare_filename(info),
    }

def get_video_info(url: str):

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
    except DownloadError as e:
        raise ValueError(str(e))

    qualities = set()

    for f in info.get("formats", []):
        height = f.get("height")
        if (f.get("vcodec") != "none"and height):
            qualities.add(height)
        
    return {
        "title": info.get("title"),
        "thumbnail": info.get("thumbnail"),
        "duration": info.get("duration"),
        "uploader": info.get("uploader"),
        "qualities": sorted(qualities)
    }