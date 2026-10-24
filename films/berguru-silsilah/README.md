# Kepentingan Berguru & Silsilah (video penjelasan infografik)

Video 9:16 (1080×1920, 30 fps, ~2 min 24 s) yang menerangkan infografik
"Kepentingan Berguru & Silsilah: Memelihara Iktikad di Akhir Zaman", dengan
narasi Bahasa Melayu dan sarikata kecil yang menyala ikut perkataan.

## Fail

| Fail | Isi |
|---|---|
| `berguru-silsilah.mp4` | Video akhir (narasi + kesan bunyi lembut, tiada muzik) |
| `berguru-silsilah.ms.srt` | Sarikata berasingan (untuk YouTube/Facebook) |
| `narasi.md` | Skrip narasi |
| `index.html` | Enjin animasi, `window.seek(t)` (buka dalam pelayar: Space = main, ←/→ = lompat) |
| `timeline.js` | Masa setiap perkataan + cue babak (dijana oleh `tools/timeline.py`) |
| `render.py`, `audio.py` | Render bingkai demi bingkai (Playwright) dan campuran audio (-14 LUFS) |
| `tools/` | Potong ilustrasi dari infografik, muat turun fon, jana sarikata |

## Bina semula

```bash
python tools/crops.py . && python tools/prep.py && python tools/fonts.py
python tools/timeline.py && python tools/srt.py
python audio.py
python render.py probe 14.5 22 69 110      # semak gambar pegun -> probe/sheet.png
python render.py all 30 4                  # 4 bahagian selari -> out/video.mp4
ffmpeg -i out/video.mp4 -i out/audio.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart berguru-silsilah.mp4
```

Suara: ElevenLabs `eleven_v4`, suara "Zulfikar – Expressive Narrator" (take 2 daripada 2).
Masa perkataan: ElevenLabs Scribe. Ilustrasi: dipotong daripada infografik asal.
