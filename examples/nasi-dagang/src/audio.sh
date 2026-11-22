#!/bin/bash
# Audio asal sahaja (tiada muzik): Borak pada 3.2 s, Makan pada 15.0 s; dinormalkan untuk pertuturan.
set -e; cd "$(dirname "$0")/../work"
ffmpeg -v error -y -i borak.mp4 -i makan.mp4 -filter_complex "\
[0:a]aresample=48000,afade=t=in:d=0.15,afade=t=out:st=9.8:d=0.22,adelay=3200|3200[a];\
[1:a]aresample=48000,afade=t=in:d=0.15,afade=t=out:st=9.8:d=0.22,adelay=15000|15000[b];\
[a][b]amix=inputs=2:normalize=0,apad=whole_dur=28.8,atrim=0:28.8,\
acompressor=threshold=-22dB:ratio=2.5:attack=10:release=200:makeup=2,loudnorm=I=-16:TP=-1.5:LRA=11:linear=true" -ar 48000 out/audio.wav
