# Wira Cilik: dua pertukaran

Video 33.8 saat, 1920×1080, 30 fps. Dua video Gemini (10 s setiap satu) disambung menjadi satu filem:

| Masa | Babak |
|---|---|
| 0.0 – 3.0 | Tajuk "WIRA CILIK" dan nama tiga kanak-kanak |
| 3.0 | Peralihan 1: kilatan, zum-kabur, aberasi warna |
| 3.0 – 5.5 | Bingkai pegun Video 1 + tag nama setiap kanak-kanak, kad "Pertukaran Pertama" |
| 5.5 – 17.9 | Video 1: 1x, gerak perlahan 0.5x pada letupan pertukaran, kad nama wira (biru, magenta, emas) |
| 17.9 | Peralihan 2: kilatan + kad "Pertukaran Kedua" |
| 17.9 – 30.3 | Video 2: 1x, gerak perlahan 0.5x, kad nama wira (cahaya, merah jambu, hijau) |
| 30.3 – 33.8 | Penutup: tajuk dan nama, pudar ke hitam |

## Andaian
- Nama kanak-kanak (kiri ke kanan) diletak dalam `src/names.js`, fail tempatan yang tidak di-commit kerana repo ini awam:
  `window.NAMES=['Nama1','Nama2','Nama3'];`
- Gelaran wira ("Wira Biru", "Wira Cahaya" dll.) direka berdasarkan warna sut. Tukar dalam `src/overlay.html` (`HER1`, `HER2`).

## Bunyi
Muzik dan SFX disintesis dalam kod (`src/audio.py`), dicampur dengan audio asal video. Semasa gerak perlahan, audio asal diregang 0.5x dan ditapis. Penjanaan muzik ElevenLabs dicuba tetapi pelayan sibuk ketika itu.

## Bina semula
```sh
# letak video sumber sebagai work/v1.mp4 (Pertukaran 1) dan work/v2.mp4 (Pertukaran 2)
src/extract.sh                               # bingkai 30 fps + 60 fps (interpolasi minterpolate)
cd work
node ../src/render_overlay.js ov 0 1014      # lapisan grafik telus (boleh dipecah 3 proses)
for k in 0 1 2 3; do python3 ../src/compose.py chunk $k 4 & done; wait
python3 ../src/audio.py
../src/mux.sh                                # -> wira-cilik.mp4
```
Perlukan Playwright (Chromium), Python (numpy, Pillow, scipy) dan ffmpeg. Fon: Russo One dan Plus Jakarta Sans (OFL) dalam `src/fonts/`.
