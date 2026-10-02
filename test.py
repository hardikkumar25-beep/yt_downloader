import yt_dlp

url = "https://youtu.be/CyiU-ITXVq0?si=_KVIuWoVg53Qob_P"

ydl_opts = {
    "format": "bestvideo+bestaudio/best",
    "merge_output_format": "mp4",
    "outtmpl": "downloads/%(title)s.%(ext)s",
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])