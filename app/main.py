from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers.playlist import router as playlist_router
from app.routers.video import router as video_router

app = FastAPI(title="Video Downloader",version="1.0.0")

app.mount("/static",StaticFiles(directory="app/static"),name="static")

templates = Jinja2Templates(directory="app/templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request=request,name="index.html",context={"request": request})

app.include_router(video_router)
app.include_router(playlist_router)