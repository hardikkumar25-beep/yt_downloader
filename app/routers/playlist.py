from fastapi import APIRouter
from ..schema.video import PlaylistDownloadRequest,PlaylistInfoRequest
from ..services.playlist_downloader import download_playlist,get_playlist_info

router = APIRouter(prefix="/playlist",tags=["Playlist"])

@router.post("/info")
def playlist_info(request: PlaylistInfoRequest):
    return get_playlist_info(request.url)

@router.post("/download")
def playlist_download(request: PlaylistDownloadRequest):

    return download_playlist(request.url,request.quality)