
# HLS Server & Reader

本專案支援：

- 本地 MP4 即時轉 HLS 串流  
- 中文檔名支援  
- 低延遲播放大影片  
- Reader 使用 `ffplay` 即時播放 HLS  

---

## 專案結構

```
HLS-server/
├─ videos/       # 放置 MP4 影片
│   ├─ 內部.mp4
│   └─ 外部.mp4
├─ llhls/        # ffmpeg 生成的 HLS playlist 與 TS 段
├─ Server.py
├─ reader.py
└─ README.md
```

---

## 安裝依賴

請先安裝 Python 3.10+ 與 pip，然後在專案根目錄執行：

```bash
pip install aiohttp aiohttp-cors requests
```

安裝 ffmpeg / ffplay：

- Windows：[https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/)  
- macOS：

```bash
brew install ffmpeg
```

---

## Server.py 使用說明

1. 放置 MP4 影片到 `videos/` 資料夾  
2. 啟動 Server：

```bash
python Server.py
```

3. 會在終端看到：

```
🚀 Server running at http://127.0.0.1:8000
```

4. Server 提供 API：

| 路徑             | 功能                       |
|-----------------|---------------------------|
| `/list`          | 列出 videos 下 MP4 清單    |
| `/play?file=xxx` | 生成 HLS playlist           |
| `/hls/{file}`    | 提供 HLS playlist 與 TS     |

---

## Reader.py 使用說明

1. 啟動 Reader：

```bash
python reader.py
```

2. 選擇影片編號，例如：

```
可播放影片列表：
0: 內部.mp4
1: 外部.mp4
請選影片編號: 0
```

3. Reader 將自動：

- 呼叫 Server 生成 HLS playlist  
- 等待 playlist 可用  
- 使用 `ffplay` 即時播放影片  

4. 播放視窗中按 **q** 或 **ESC** 可退出  

---

## 注意事項

- 對於大影片，Reader.py 會 **即時播放 HLS**，不需等整個影片轉完  
- HLS segment 時長默認 1 秒，可調整 `Server.py` 內 `-hls_time` 參數  
- 中文檔名已支援  
- Server 可同時處理多個播放請求  
