import shutil
from pathlib import Path
import yt_dlp
from .job_manager import update_job

DOWNLOAD_DIR = Path("downloads")
DOWNLOAD_DIR.mkdir(exist_ok=True)

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

def download_playlist(url: str,quality: str = "1080p",job_id:str | None =None):
    height = quality.replace("p", "")
    current_vids=0
    total_vids=0
    def progress_hook(data):
        nonlocal current_vids,total_vids
        if not job_id:
            return
        if data["status"]=="downloading":
            downloaded=data.get("downloaded_bytes",0)
            total=(data.get("total_bytes")or data.get("total_bytes_estimate"))
            if total:
                current_prog=(downloaded/total)*100
            else:
                current_prog=0
            if total_vids>0:
                overall_prog=((current_vids-1+current_prog/100)/total_vids)*100
            else:
                overall_prog=current_prog
            update_job(job_id,status="downloading",progress=overall_prog,message=(f"Downloading video" f"{current_vids} of"f"{total_vids}"),current_video=current_vids,total_videos=total_vids)
        elif data["status"]=="finished":
            current_vids+=1
            if total_vids>0:
                overall_prog=(current_vids/total_vids)*100
            else:
                overall_prog=100
            update_job(job_id,status="downloading",progress=overall_prog,message=(f"Finished video" f"{current_vids} of"f"{total_vids}"),current_video=current_vids,total_videos=total_vids)
    ydl_opts = {
        "format": f"bestvideo[height<={height}]+bestaudio/best",
        "merge_output_format": "mp4",
        "outtmpl": "downloads/%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s",
        "noplaylist": False,
        "progress_hooks":[progress_hook]}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            entries=[entry for entry in info.get("entries") or [] if entry]
            total_vids=len(entries)
            if job_id:
                update_job(job_id,status="downloading",progress=0,message=(f"Starting playlist" f"{total_vids} videos"),current_video=0,total_video=total_vids)
            ydl.download([url])
        playlist_title=info.get("title")or"playlist"
        playlist_dir=(DOWNLOAD_DIR/playlist_title)
        zip_base=(DOWNLOAD_DIR/playlist_title)
        zip_path=Path(shutil.make_archive(str(zip_base),"zip",root_dir=playlist_dir))
        if job_id:
            update_job(job_id,status="completed",progress=100,message="Playlist download complete",current_video=current_vids,total_videos=total_vids,filename=str(zip_path))
        return{"playlist_title":playlist_title,"status":"completed","filename":str(zip_path)}
    except Exception as e:
        if job_id:
            update_job(job_id,status="failed",error=str(e),message="Playlist download failed",)
            raise