from fastapi import FastAPI
from app.routers.video import router as video_router
from app.routers.playlist import router as playlist_router

app = FastAPI(title="Personal Video Downloader",version="1.0.0")
app.include_router(video_router)
app.include_router(playlist_router)

@app.get("/")
def root():
    return {"message": "Video Downloader API is running"}