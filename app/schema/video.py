from pydantic import BaseModel

class VideoDownloadRequest(BaseModel):
    url: str
    quality: str = "1080p"
    format: str = "mp4"

class VideoInfoRequest(BaseModel):
    url: str

class PlaylistInfoRequest(BaseModel):
    url: str

class PlaylistDownloadRequest(BaseModel):
    url: str
    quality: str = "1080p"
    format: str = "mp4"