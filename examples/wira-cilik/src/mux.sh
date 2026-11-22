#!/bin/bash
# Sambung bahagian video + audio (mampat, had puncak, ~ -14 LUFS) -> ../wira-cilik.mp4
set -e
cd "$(dirname "$0")/../work"
printf "file 'chunk_%d.mp4'\n" 0 1 2 3 > out/list.txt
ffmpeg -v error -y -f concat -safe 0 -i out/list.txt -c copy out/video.mp4
ffmpeg -v error -y -i out/video.mp4 -i out/audio.wav -map 0:v -map 1:a -c:v copy \
  -af "acompressor=threshold=-20dB:ratio=3:attack=8:release=250:makeup=2,volume=2.6dB,alimiter=limit=0.84:level=false" \
  -c:a aac -b:a 256k -ar 48000 -movflags +faststart ../wira-cilik.mp4
ffprobe -v error -show_entries format=duration -of default=nw=1 ../wira-cilik.mp4
ffmpeg -v info -i ../wira-cilik.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|Peak):"
