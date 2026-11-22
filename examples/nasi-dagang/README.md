# Nasi Dagang Tok Ma

Dua klip keluarga (10 s setiap satu) digabung menjadi satu cerita 28.8 s, 1920×1080, 24 fps. Tiada muzik; suara asal dikekalkan.

| Masa | Babak |
|---|---|
| 0.0 – 3.2 | Kad tajuk "Nasi Dagang Tok Ma" |
| 3.2 – 13.2 | Bab 01 "Khabar Gembira": cucu-cucu berborak tentang nasi dagang Tok Ma |
| 13.2 – 15.0 | Peralihan "Tak lama kemudian... Hidangan Tok Ma" |
| 15.0 – 25.0 | Bab 02 "Hidangan Tok Ma": makan bersama |
| 25.0 – 28.8 | Penutup "Tamat" |

- **Sari kata**: transkripsi Whisper large-v3 dan turbo (sherpa-onnx, luar talian), disemak secara manual. Teks disimpan dalam `src/subs.js` (tempatan, tidak di-commit kerana repo awam).
- **Tukar wajah**: insightface (buffalo_l) + inswapper_128, dijejak ikut embedding wajah. Gambar sumber di `work/sumber_wajah.png` (tidak di-commit).
- Media (video, gambar, SRT) tidak dimasukkan ke repo.

## Bina semula
```sh
# work/borak.mp4, work/makan.mp4, work/sumber_wajah.png, src/subs.js
python3 src/faceswap.py
cd work && mkdir -p borak_raw && ffmpeg -i borak.mp4 borak_raw/%04d.png
node ../src/render_overlay.js ov 0 691
for k in 0 1 2 3; do python3 ../src/compose.py chunk $k 4 & done; wait
../src/audio.sh
```
