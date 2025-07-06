import os
import yt_dlp

OUTPUT_DIR = 'output_audio'

def download_mp3_with_progress(url: str, hook_fn=None):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(OUTPUT_DIR, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': True,
        'quiet': True,
        'progress_hooks': [hook_fn] if hook_fn else [],
        'outtmpl_na_placeholder': '_',  # 특수문자 대체
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url, download=True)
            filename_with_ext = ydl.prepare_filename(result)
            filename = os.path.splitext(os.path.basename(filename_with_ext))[0] + ".mp3"
            full_path = os.path.join(OUTPUT_DIR, filename)
            return filename, full_path
    except Exception as e:
        return None, str(e)
