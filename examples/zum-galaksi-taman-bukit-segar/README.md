# Zum: galaksi ke Taman Bukit Segar

Video 24 saat, 1920×1080, 30 fps, dengan bunyi sintesis (pad, whoosh dan bunyi label, dijana dalam kod).
Perjalanan: Alam Galaksi, Bumi, Asia, Malaysia, Kuala Lumpur, Cheras, Taman Bukit Segar.

## Sumber dan kejujuran paparan
- **Galaksi**: ilustrasi prosedur (benih tetap), bukan imej sebenar. Ditanda "Ilustrasi" pada skrin.
- **Bumi hingga jalan**: imej satelit Esri World Imagery (Esri, Maxar, Earthstar Geographics dan komuniti pengguna GIS). Tertakluk pada terma Esri.
- **Taman Bukit Segar**: koordinat anggaran 3.0926°U, 101.7496°T, diambil daripada kedudukan jalan "Jalan Bukit Segar" pada peta jalan Esri. Ia bukan titik rasmi.
- **Kuala Lumpur** (3.1390°U, 101.6869°T) ialah pusat bandar. Pin **Cheras** diletakkan pada kedudukan label peta Esri.

## Bina semula
```sh
cd src
python3 fetch_base.py          # lapisan Bumi z4, z5, z6 ke tex/
node drive.js collect          # senarai jubin peta ke needed.json
python3 fetch_tiles.py         # muat turun jubin ke tiles/
python3 -m http.server 8766 --bind 127.0.0.1 &
node drive.js full fr/a 0 720  # render bingkai (boleh dipecah kepada 3 proses)
python3 audio.py               # bunyi sintesis
```
Perlukan Playwright (Chromium), Python (Pillow, numpy), ffmpeg, dan `@fontsource/plus-jakarta-sans` serta `@fontsource/dm-mono` dalam `node_modules`.
