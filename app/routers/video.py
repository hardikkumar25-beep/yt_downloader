from fastapi import APIRouter,HTTPException
from ..schema.video import VideoDownloadRequest,VideoInfoRequest
from fastapi.responses import FileResponse
from ..services.video_downloader import download_video,get_video_info
import os


router = APIRouter(prefix="/video",tags=["Video"])

@router.post("/download")
def download(request: VideoDownloadRequest):
    try:
        file_path = download_video(request.url,request.quality)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=500,details="Downloaded file was not found.")
        return FileResponse(path=file_path,media_Type="video/mp4",filename=os.path.basename(file_path))
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Download failed: {str(e)}")
    

@router.post("/info")
def vid_info(request:VideoInfoRequest):
    try:
        return get_video_info(request.url)
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))
