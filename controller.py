import asyncio
from downloader import download_mp3_with_progress
import os

class DownloadState:
    def __init__(self):
        self.percent = 0.0
        self.status = "대기 중"
        self.filename = None
        self.result_path = None

    def hook(self, p):
        if p['status'] == 'downloading':
            total = float(p.get('total_bytes', 1))
            downloaded = float(p.get('downloaded_bytes', 0))
            self.percent = downloaded / total
            self.status = f"📥 {self.percent * 100:.1f}% 다운로드 중"
        elif p['status'] == 'finished':
            self.percent = 1.0
            self.status = "🎧 변환 중..."

async def run_download(url: str, state: DownloadState):
    state.status = "⏳ 다운로드 시작..."
    filename, path = await asyncio.to_thread(download_mp3_with_progress, url, state.hook)

    if filename and os.path.exists(path):
        state.filename = filename
        state.result_path = path
        state.status = f"✅ 완료: {filename}"
    else:
        state.status = "❌ 오류 발생 또는 파일 없음"
