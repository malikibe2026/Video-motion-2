# video-tools

Lima alat untuk menghasilkan video dengan kod.

| Alat | Kegunaan |
|---|---|
| **FFmpeg** | Potong, cantum dan gabung video; letak caption atas video |
| **Whisper** (faster-whisper) | Dengar percakapan dalam video → caption dan masa setiap perkataan |
| **HyperFrames** | HTML → video |
| **Remotion** | React → video |
| **Three.js** | Adegan 3D dalam video (melalui HyperFrames atau Remotion) |

## Pasang

Perlu: Node.js 22+, Python 3.10+, FFmpeg.

```bash
bash video-tools/pasang.sh
```

## Uji

```bash
cd video-tools
npm run ujian:hyperframes        # contoh/hyperframes-3d/out.mp4 (kiub 3D + tajuk)
npm run ujian:remotion           # contoh/remotion/out.mp4 (tajuk melantun)
python3 transkrip.py VIDEO.mp4   # VIDEO.srt + VIDEO.words.json
```

Kalau Remotion gagal memuat turun pelayarnya sendiri, tetapkan pelayar tempatan:

```bash
REMOTION_BROWSER=/laluan/ke/chrome npm run ujian:remotion
```

## Resipi FFmpeg

```bash
# Potong 10 saat bermula pada minit 1
ffmpeg -ss 00:01:00 -i masuk.mp4 -t 10 -c:v libx264 -c:a aac potong.mp4

# Cantum dua klip dengan peralihan pudar 0.5 saat (klip pertama 5 saat)
ffmpeg -i a.mp4 -i b.mp4 -filter_complex "[0][1]xfade=transition=fade:duration=0.5:offset=4.5,format=yuv420p" gabung.mp4

# Letak caption daripada Whisper
ffmpeg -i video.mp4 -vf "subtitles=video.srt:force_style='FontSize=28'" -c:a copy bercaption.mp4

# Tukar audio dengan suara latar
ffmpeg -i video.mp4 -i suara.mp3 -map 0:v -map 1:a -c:v copy -shortest akhir.mp4
```

## Whisper: perkara yang perlu tahu

- Model `small` ialah lalai. Guna `--model medium` untuk lebih tepat (lebih lambat).
- Semak nama khas dan istilah jabatan; Whisper boleh tersalah eja.
- Whisper boleh **mereka-reka ayat** (contoh: "Assalamualaikum...") bila audio terlalu pendek atau terpotong. Sentiasa semak caption.
- Kali pertama, model dimuat turun dari huggingface.co.

## Peraturan HyperFrames + Three.js

- Setiap bingkai mesti dikira daripada masa `t` sahaja: lukis dalam pendengar `hf-seek`, bukan `requestAnimationFrame`.
- Fail GSAP dan Three.js disalin ke `contoh/hyperframes-3d/vendor/` oleh `pasang.sh`, jadi render tidak bergantung pada CDN.
