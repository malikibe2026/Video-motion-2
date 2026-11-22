#!/bin/bash
# Ekstrak bingkai: a = 30 fps penuh, s = gerak perlahan (60 fps interpolasi, dimainkan pada 30 fps = 0.5x)
set -e
cd "$(dirname "$0")/../work"
MI="mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1"
for v in v1 v2; do mkdir -p ${v}a ${v}s; done
ffmpeg -v error -y -i v1.mp4 -vf "minterpolate=fps=30:$MI" -q:v 2 v1a/%04d.jpg &
ffmpeg -v error -y -i v2.mp4 -vf "minterpolate=fps=30:$MI" -q:v 2 v2a/%04d.jpg &
ffmpeg -v error -y -ss 2.0 -t 2.8 -i v1.mp4 -vf "minterpolate=fps=60:$MI" -q:v 2 v1s/%04d.jpg &
ffmpeg -v error -y -ss 2.2 -t 2.8 -i v2.mp4 -vf "minterpolate=fps=60:$MI" -q:v 2 v2s/%04d.jpg &
wait
for d in v1a v2a v1s v2s; do echo $d $(ls $d | wc -l); done
