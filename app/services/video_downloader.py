import yt_dlp
from pathlib import Path
from yt_dlp.utils import DownloadError
from .job_manager import update_job

DOWNLOAD_DIR = Path("downloads")
DOWNLOAD_DIR.mkdir(exist_ok=True)

def download_video(url: str, quality: str = "1080p",job_id: str | None = None):
    height = quality.replace("p", "")
    def progress_hook(data):
        if not job_id:
            return
        if data["status"]=="downloading":
            downloaded=data.get("downloaded_bytes",0)
            total=(data.get("total_bytes")or data.get("total_bytes_estimate"))
            if total:
                progress=downloaded/total*100
            else:
                progress=0
            update_job(job_id,status="downloading",progress=progress,message="Downloading video...")
        elif data["status"]=="finished":
            update_job(job_id,status="processing",progress=100,message="Processing video...")
    ydl_opts = {
        "format": f"bestvideo[height<={quality.replace('p', '')}]+bestaudio/best",
        "merge_output_format": "mp4",
        "outtmpl": str(DOWNLOAD_DIR / "%(title)s.%(ext)s"),
        "progress_hooks": [progress_hook],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename=ydl.prepare_filename(info)
            final_filename=Path(filename)
            if final_filename.suffix != ".mp4":
                final_filename = final_filename.with_suffix(".mp4")
        if job_id:
            update_job(
                job_id,
                status="completed",
                progress=100,
                message="Download complete.",
                filename=str(final_filename))
        return {"title":info.get("title"),"filename":str(final_filename)}
    except DownloadError as e:

        if job_id:
            update_job(
                job_id,
                status="failed",
                error=str(e),
                message="Download failed."
            )

        raise

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