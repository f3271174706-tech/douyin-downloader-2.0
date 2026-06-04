from pathlib import Path
from urllib.parse import unquote

import httpx
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from downloader import MOBILE_UA, apply_quality, cleanup_old_files, download_video_for_stream, extract_video_info, download_video

app = FastAPI(title="抖音/X 无水印下载器")

@app.on_event("startup")
async def startup_cleanup():
    cleanup_old_files()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


class ParseRequest(BaseModel):
    url: str


class DownloadRequest(BaseModel):
    url: str
    quality: str = "1080p"
    type: str = "video"
    image_index: int = 0


@app.get("/")
async def index():
    from fastapi.responses import HTMLResponse
    html_path = static_dir / "index.html"
    if html_path.exists():
        return HTMLResponse(html_path.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>index.html not found</h1>", status_code=404)


@app.post("/api/parse")
async def parse_video(req: ParseRequest):
    url = req.url.strip()
    if not url:
        raise HTTPException(status_code=400, detail="请输入视频链接")

    try:
        info = extract_video_info(url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"解析失败: {str(e)}")

    media_type = info.get("type", "video")
    result = {
        "success": True,
        "title": info["title"],
        "thumbnail": info["thumbnail"],
        "duration": info.get("duration", 0),
        "platform": info["platform"],
        "type": media_type,
    }
    if media_type == "photo":
        result["images"] = info.get("images", [])
        result["video_url"] = ""
        result["music_url"] = info.get("music_url", "")
    else:
        result["video_url"] = info.get("video_url", "")
    return result


@app.get("/api/stream")
async def stream_video(
    video_url: str = Query(..., description="Douyin video URL"),
    quality: str = Query("1080p", description="Quality: 720p, 1080p, hd"),
):
    """Download video to disk, serve with FileResponse (native Range support)."""
    video_url = unquote(video_url)
    if "douyin" in video_url or "snssdk" in video_url:
        video_url = apply_quality(video_url, quality)

    file_path, filename = download_video_for_stream(video_url)
    return FileResponse(
        path=file_path,
        media_type="video/mp4",
        filename=filename,
    )


@app.post("/api/download")
async def download_video_api(req: DownloadRequest):
    url = req.url.strip()
    if not url:
        raise HTTPException(status_code=400, detail="请输入视频链接")

    try:
        file_path, filename = download_video(
            url, quality=req.quality, media_type=req.type, image_index=req.image_index
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"下载失败: {str(e)}")

    if filename.endswith(".mp3"):
        media_type = "audio/mpeg"
    elif filename.endswith(".zip"):
        media_type = "application/zip"
    elif filename.endswith(".webp") or filename.endswith(".jpg") or filename.endswith(".png"):
        media_type = "image/" + filename.rsplit(".", 1)[-1]
    else:
        media_type = "video/mp4"
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type=media_type,
    )
