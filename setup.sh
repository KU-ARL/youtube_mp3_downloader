#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
BGUTIL_DIR="$HOME/bgutil-ytdlp-pot-provider"

echo "[1/4] Installing Python packages"
python -m pip install -r requirements.txt

echo "[2/4] Checking ffmpeg"
if ! command -v ffmpeg >/dev/null 2>&1; then
    echo "ffmpeg not found. Install with: sudo apt-get install -y ffmpeg" >&2
    exit 1
fi

echo "[3/4] Checking Node.js 22+"
if ! command -v node >/dev/null 2>&1; then
    echo "Node.js not found. Install Node.js 22 with nvm, then run this script again." >&2
    exit 1
fi
if [ "$(node -p 'process.versions.node.split(".")[0]')" -lt 22 ]; then
    echo "Node.js 22 or higher is required (current: $(node -v))." >&2
    exit 1
fi

echo "[4/4] Building bgutil PO Token script"
if [ ! -d "$BGUTIL_DIR" ]; then
    git clone --branch 2.0.0 --depth 1 https://github.com/Brainicism/bgutil-ytdlp-pot-provider.git "$BGUTIL_DIR"
fi
cd "$BGUTIL_DIR/server"
npm ci
npx tsc

echo "Setup complete. Run 'python app.py' to start."
