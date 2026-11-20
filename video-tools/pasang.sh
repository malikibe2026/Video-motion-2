#!/usr/bin/env bash
# Pasang semua alat video: FFmpeg (semak), Whisper, HyperFrames, Remotion, Three.js.
# Jalankan dari mana-mana: bash video-tools/pasang.sh
set -euo pipefail
cd "$(dirname "$0")"

echo "== FFmpeg"
if command -v ffmpeg >/dev/null; then ffmpeg -version | head -1
else echo "FFmpeg tiada. Pasang: sudo apt-get install -y ffmpeg (Linux) / winget install ffmpeg (Windows)"; exit 1; fi

echo "== HyperFrames, Remotion, Three.js (npm)"
# onnxruntime cuba muat turun binari GPU (CUDA) yang tidak diperlukan; langkau.
npm ci --no-audit --no-fund --onnxruntime-node-install-cuda=skip

echo "== Salin GSAP dan Three.js ke contoh HyperFrames (supaya tidak bergantung pada CDN)"
mkdir -p contoh/hyperframes-3d/vendor
cp node_modules/gsap/dist/gsap.min.js contoh/hyperframes-3d/vendor/
cp node_modules/three/build/three.module.js node_modules/three/build/three.core.js contoh/hyperframes-3d/vendor/

echo "== Whisper (Python)"
python3 -m pip install -r requirements.txt

echo "Siap. Uji: npm run ujian:hyperframes | npm run ujian:remotion | python3 transkrip.py VIDEO.mp4"
