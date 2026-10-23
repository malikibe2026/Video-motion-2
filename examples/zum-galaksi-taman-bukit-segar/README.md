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

## Versi 2: `zum-galaksi-ke-alam-barzakh.mp4` (51 s)
Sambungan hingga tanah perkuburan, liang lahad dan alam barzakh. Menggantikan versi 1 (`zum-galaksi-taman-bukit-segar.mp4`), yang lokasi Taman Bukit Segarnya kurang tepat.
- **Taman Bukit Segar**: kini 3.0913°U, 101.7538°T (kedudukan label peta Esri).
- **Tanah Perkuburan Islam Taman Permai, Cheras**: 3.1083778°U, 101.7536773°T. Koordinat diberi pengguna. Imej satelit mengesahkan barisan kubur dengan sebuah masjid di sebelahnya.
- **Liang lahad** dan **alam barzakh**: ilustrasi abstrak buatan kod, tanpa memaparkan jenazah. Ditanda "Ilustrasi".
- **Ayat** (Arab dan terjemahan): An-Nisa' 4:78, Ali 'Imran 3:185, Al-Mu'minun 23:100 (potongan). Teks ditaip daripada ingatan dan perlu disemak dengan mushaf sebelum disiarkan.
- Fail versi 2: `src/zoom2.html`, `drive2.js`, `fetch_tiles2.py`, `audio2.py` (jalankan seperti langkah di atas, dengan `drive2.js` dan `needed2.json`). Fon Arab: `@fontsource/amiri`.

## Versi WhatsApp
- `zum-galaksi-ke-alam-barzakh-wa.mp4`: 1280×720 (landskap), 12.8 MB.
- `zum-galaksi-ke-alam-barzakh-wa-9x16.mp4`: 720×1280 (menegak 9:16, untuk Status), 12.7 MB. Susun atur disusun semula untuk potret (bukan dipotong): `src/zoom3.html?p=1`, `drive3.js`, `fetch_tiles3.py`.
Had klip Status WhatsApp berbeza mengikut versi aplikasi (secara tradisi 30 saat), jadi semak sebelum memuat naik video 51 saat.
