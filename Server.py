import os
import subprocess
import urllib.parse
from aiohttp import web
from aiohttp_cors import setup as cors_setup, ResourceOptions

VIDEO_DIR = "./videos"
HLS_DIR = "./llhls"

os.makedirs(VIDEO_DIR, exist_ok=True)
os.makedirs(HLS_DIR, exist_ok=True)

# -----------------------
# 路由
# -----------------------

async def list_videos(request):
    files = [f for f in os.listdir(VIDEO_DIR) if f.endswith(".mp4")]
    return web.json_response(files)

async def play_video(request):
    raw_filename = request.query.get("file", "")
    filename = urllib.parse.unquote(raw_filename)
    input_file = os.path.join(VIDEO_DIR, filename)

    if not os.path.exists(input_file):
        return web.json_response({"error": "影片不存在"}, status=404)

    playlist_file = os.path.join(HLS_DIR, "stream.m3u8")

    # ffmpeg 邊轉邊輸出 TS HLS
    cmd = [
        "ffmpeg", "-y", "-i", input_file,
        "-preset", "veryfast",
        "-g", "48",
        "-sc_threshold", "0",
        "-hls_time", "1",
        "-hls_list_size", "5",  # 最多保留 5 個 segment
        "-hls_flags", "delete_segments+append_list",
        "-hls_segment_type", "mpegts",
        playlist_file
    ]
    subprocess.Popen(cmd)  # 非阻塞

    return web.json_response({"playlist": "/hls/stream.m3u8"})

async def serve_hls(request):
    filename = request.match_info['filename']
    path = os.path.join(HLS_DIR, filename)
    if not os.path.exists(path):
        return web.Response(status=404)
    return web.FileResponse(path)

# -----------------------
# App + CORS
# -----------------------
app = web.Application()
cors = cors_setup(app, defaults={
    "*": ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*",
    )
})
routes = [
    app.router.add_get("/list", list_videos),
    app.router.add_get("/play", play_video),
    app.router.add_get("/hls/{filename}", serve_hls),
]
for route in routes:
    cors.add(route)

if __name__ == "__main__":
    print("🚀 Server running at http://127.0.0.1:8000")
    web.run_app(app, host="0.0.0.0", port=8000)
