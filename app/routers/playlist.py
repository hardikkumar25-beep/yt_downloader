from fastapi import APIRouter,HTTPException,BackgroundTasks
from fastapi.responses import FileResponse
from pathlib import Path
from ..schema.video import PlaylistDownloadRequest,PlaylistInfoRequest
from ..services.playlist_downloader import download_playlist,get_playlist_info
from ..services.job_manager import get_job,create_job

router = APIRouter(prefix="/video/playlist",tags=["Playlist"])

@router.post("/info")
def playlist_info(request: PlaylistInfoRequest):
    try:
        return get_playlist_info(request.url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/download")
def playlist_download(request: PlaylistDownloadRequest,background_tasks:BackgroundTasks):
    job_id=create_job()
    background_tasks.add_task(download_playlist,request.url,request.quality,job_id)
    return {"job_id":job_id}

@router.get("/progress/{job_id}")
def playlist_progress(job_id:str):
    job=get_job(job_id)
    if not job:
        raise HTTPException(status_code=404,detail="Job not found")
    return job

@router.get("/download/{job_id}")
def download_comp_playlist(job_id:str):
    job=get_job(job_id)
    if not job:
        raise HTTPException(status_code=404,detail="Job not found")
    if job["status"]!="completed":
        raise HTTPException(status_code=400,detail="Playlist Download is not completed yet")
    filename=job.get("filename")
    if not filename:
        raise HTTPException(status_code=500,detail="Playlist file not found")
    path=Path(filename)
    if not path.exists():
        raise HTTPException(status_code=404,detail="Playlist ZIP no longer exists.")
    return FileResponse(path=path,media_type="application/zip",filename=path.name)   

