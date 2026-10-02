from fastapi import APIRouter
from ..schema.video import VideoDownloadRequest,VideoInfoRequest
from ..services.video_downloader import download_video,get_video_info

router = APIRouter(prefix="/video",tags=["Video"])

@router.post("/download")
def download(request: VideoDownloadRequest):
    result = download_video(request.url,request.quality)
    return result

@router.post("/info")
def vid_info(request:VideoInfoRequest):
    return get_video_info(request.url)