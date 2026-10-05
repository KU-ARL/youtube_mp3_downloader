from nicegui import ui
from controller import DownloadState, run_download
import os

state = DownloadState()

ui.label("🎵 YouTube to MP3 Downloader").classes('text-2xl font-bold text-center mt-4')
input_url = ui.input("YouTube URL").classes('w-full')
status_label = ui.label()
progress = ui.linear_progress().classes('w-full')

def update_ui():
    progress.set_value(state.percent)
    status_label.set_text(state.status)

ui.timer(interval=0.3, callback=update_ui)

async def start_download():
    url = input_url.value.strip()
    if not url:
        state.status = "❗ URL을 입력해주세요."
        return

    state.percent = 0.0
    state.status = "⏳ 다운로드 준비 중..."

    await run_download(url, state)

    if state.result_path and os.path.exists(state.result_path):
        ui.download(state.result_path, filename=state.filename)
    else:
        state.status = "❌ 다운로드된 파일을 찾을 수 없습니다."


ui.button("Download MP3 🎶", color='primary', on_click=start_download)

ui.run(title="YouTube MP3 추출기", reload=False, show=False)
