from fastapi import APIRouter,HTTPException,BackgroundTasks
from ..schema.video import VideoDownloadRequest,VideoInfoRequest
from fastapi.responses import FileResponse
from ..services.video_downloader import download_video,get_video_info
from ..services.job_manager import update_job,get_job,create_job
import os
from pathlib import Path

router = APIRouter(prefix="/video",tags=["Video"])

@router.post("/download")
def video_download(request: VideoDownloadRequest,background_tasks:BackgroundTasks):
    job_id=create_job()
    background_tasks.add_task(download_video,request.url,request.quality,job_id)
    return {"job_id":job_id}
@router.get("/progress/{job_id}")
def video_progress(job_id:str):
    job=get_job(job_id)
    if not job:
        raise HTTPException(status_code=404,detail="Job not found")
    return job

@router.get("/download/{job_id}")
def download_complete_vid(job_id:str):
    job=get_job(job_id)
    if not job:
        raise HTTPException(status_code=404,detail="Job not found")
    if job["status"]!="completed":
        raise HTTPException(status_code=400,detail="Download is not completed yet")
    filename=job.get("filename")
    if not filename:
        raise HTTPException(status_code=500,detail="Download not found")
    path=Path(filename)
    if not path.exists():
        raise HTTPException(status_code=404,detail="Downloaded file no longer exists.")
    return FileResponse(path=path,media_type="video/mp4",filename=path.name)


@router.post("/info")
def vid_info(request:VideoInfoRequest):
    try:
        return get_video_info(request.url)
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))
