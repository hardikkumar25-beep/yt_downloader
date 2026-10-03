from fastapi import APIRouter,HTTPException
from ..schema.video import PlaylistDownloadRequest,PlaylistInfoRequest
from ..services.playlist_downloader import download_playlist,get_playlist_info

router = APIRouter(prefix="/video/playlist",tags=["Playlist"])

@router.post("/info")
def playlist_info(request: PlaylistInfoRequest):
    try:
        return get_playlist_info(request.url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/download")
def playlist_download(request: PlaylistDownloadRequest):
    try:
        return download_playlist(
            request.url,
            request.quality
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))