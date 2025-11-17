import requests
import urllib.parse
import subprocess
import time
import urllib.request

SERVER_URL = "http://127.0.0.1:8000"

def list_videos():
    try:
        res = requests.get(f"{SERVER_URL}/list")
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print("取得影片列表失敗:", e)
        return []

def generate_hls(filename):
    try:
        res = requests.get(f"{SERVER_URL}/play", params={"file": filename})
        res.raise_for_status()
        data = res.json()
        playlist_url = SERVER_URL + data["playlist"]
        return playlist_url
    except Exception as e:
        print("生成 HLS 失敗:", e)
        return None

def wait_for_playlist(playlist_url, timeout=15):
    """等待 playlist 可用"""
    print("等待 HLS playlist 生成中...")
    start = time.time()
    while True:
        try:
            with urllib.request.urlopen(playlist_url) as resp:
                if resp.status == 200:
                    return True
        except:
            pass
        if time.time() - start > timeout:
            print("等待 HLS playlist 超時")
            return False
        time.sleep(0.5)

def play_hls_ffplay(playlist_url):
    if not wait_for_playlist(playlist_url):
        return
    print("啟動 ffplay 播放 HLS，按 q 或 ESC 關閉")
    subprocess.run(["ffplay", "-autoexit", "-loglevel", "quiet", playlist_url])

# ------------------------------
if __name__ == "__main__":
    files = list_videos()
    if not files:
        print("沒有影片")
        exit(0)

    print("可播放影片列表：")
    for i, f in enumerate(files):
        print(f"{i}: {f}")

    idx = input("請選影片編號: ")
    try:
        idx = int(idx)
        filename = files[idx]
    except:
        print("輸入錯誤")
        exit(1)

    playlist_url = generate_hls(filename)
    if playlist_url:
        play_hls_ffplay(playlist_url)
