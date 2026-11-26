#!/bin/bash
# Check what Video Explainer needs and prepare it. Prints each missing tool with its install command and exits 1,
# so the agent can ask the user before installing.
# By default installs headless Chrome only (~390 MB) so Voice: none works right away.
# Pass --voice to also prepare Parakeet alignment + Kokoro-82M local TTS in the skill's isolated venv.
DIR="$(cd "$(dirname "$0")" && pwd)"
WITH_VOICE=0
for arg in "$@"; do
  case "$arg" in
    --voice) WITH_VOICE=1 ;;
    *) echo "usage: setup.sh [--voice]" >&2; exit 2 ;;
  esac
done

missing=0
if [ "$(uname)" = Darwin ]; then hint() { echo "brew install $1"; }; else hint() { echo "$2"; }; fi
need() { command -v "$1" >/dev/null || { echo "missing: $1  (install: $(hint "$2" "$3"))"; missing=1; }; }
need ffmpeg ffmpeg "sudo apt install ffmpeg"
need python3 python "sudo apt install python3 python3-venv"
need node node "Node 22+ from https://nodejs.org"
if command -v node >/dev/null && [ "$(node -p 'process.versions.node.split(".")[0]')" -lt 22 ]; then
  echo "too old: node $(node -v), needs 22 or newer  (install: $(hint node "Node 22+ from https://nodejs.org"))"; missing=1
fi
[ "$missing" = 1 ] && exit 1

"$DIR/py" -c "import numpy" || exit 1
VENV_PY="$("$DIR/py" -c 'import sys; print(sys.executable)')"

HF=hyperframes@0.9.79
LOG="$(mktemp)"
trap 'rm -f "$LOG"' EXIT
quiet() { "$@" >"$LOG" 2>&1 || { tail -c 1500 "$LOG"; return 1; }; }

quiet npx -y "$HF" browser ensure || { echo "HyperFrames could not download its Chrome"; exit 1; }

THREE_CACHE="$HOME/.cache/video-explainer/vendor/three.min.js"
if [ ! -f "$THREE_CACHE" ] && command -v curl >/dev/null; then
  mkdir -p "$(dirname "$THREE_CACHE")"
  curl -fsSL "https://cdn.jsdelivr.net/npm/three@0.149.0/build/three.min.js" -o "$THREE_CACHE" 2>/dev/null || rm -f "$THREE_CACHE"
fi

if [ "$WITH_VOICE" = 1 ]; then
  if ! "$VENV_PY" -c "import kokoro_onnx, soundfile" 2>/dev/null; then
    if command -v uv >/dev/null; then
      quiet uv pip install -q -p "$VENV_PY" kokoro-onnx soundfile || { echo "Could not install kokoro-onnx and soundfile"; exit 1; }
    else
      quiet "$VENV_PY" -m pip install -q --disable-pip-version-check kokoro-onnx soundfile || { echo "Could not install kokoro-onnx and soundfile"; exit 1; }
    fi
  fi
  quiet npx -y "$HF" models install parakeet || { echo "HyperFrames could not install the Parakeet speech model"; exit 1; }
  TMP_WAV="$(mktemp -u).wav"
  HYPERFRAMES_PYTHON="$VENV_PY" quiet npx -y "$HF" tts "Ready." -o "$TMP_WAV" --json || { rm -f "$TMP_WAV"; echo "HyperFrames could not initialize Kokoro TTS"; exit 1; }
  rm -f "$TMP_WAV"
  echo "ready: ffmpeg, Python, Node $(node -v), HyperFrames Chrome, Parakeet, and Kokoro TTS"
else
  echo "ready: ffmpeg, Python, Node $(node -v), HyperFrames Chrome (run 'setup.sh --voice' for local Kokoro + Parakeet voice)"
fi
