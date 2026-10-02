from fastapi import FastAPI
from app.routers.video import router as video_router

app = FastAPI(title="Personal Video Downloader",version="1.0.0")
app.include_router(video_router)

@app.get("/")
def root():
    return {"message": "Video Downloader API is running"}