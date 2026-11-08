# Humaira: tumbesaran 0 hingga 18 bulan

Video montaj 1920×1080, 30 fps, kira-kira 73 saat, 120 BPM. Ia menggunakan 78 ilustrasi kartun berlatar telus daripada folder Drive `Humaira_Kartun_Tersusun`.

**Repo ini hanya menyimpan kod.** Gambar kartun, video siap dan fail audio tidak di-commit kerana ia gambar peribadi kanak-kanak. Semua fail itu tersenarai dalam `.gitignore`.

## Struktur video
| Bahagian | Isi |
|---|---|
| Pembukaan | Tajuk "Humaira", baru lahir hingga 1 tahun 6 bulan |
| Halaman umur | Satu halaman bagi setiap peringkat umur. Setiap gambar muncul tepat pada satu ketukan dengan not kotak muzik daripada kord semasa |
| Bawah 7 Bulan | Dipecah kepada 2 halaman, ditambah flipbook "Belajar meniarap di pantai" (7 gambar dimainkan ke depan dan ke belakang) |
| 1 Tahun | Konfeti |
| Bersama keluarga | Gambar 079 dan 080 (tiada label umur) |
| Penutup | "78 ilustrasi kartun · 18 bulan kenangan" |

Bar garis masa di bawah (Lahir hingga 18 bln) menunjuk umur halaman semasa. "Bawah 7 Bulan" dipaparkan sebagai julat 0–7 bulan, bukan satu titik, kerana tarikh tepat tidak diketahui.

## Kejujuran paparan
- Umur diambil **daripada nama fail sahaja** (lihat `BACA_SAYA.txt` dalam folder Drive). Gambar tanpa label umur diletakkan dalam "Bawah 7 Bulan" mengikut arahan asal, dan halaman itu ditanda "Urutan gambar anggaran".
- Penjuru kanan atas memaparkan tanda "ILUSTRASI KARTUN".
- Muzik dan bunyi dijana sepenuhnya dalam `audio.py`. Tiada sampel luar digunakan.

## Bina semula
1. Muat turun folder Drive `Humaira_Kartun_Tersusun` (zip), kemudian ekstrak ke mana-mana folder.
2. Jalankan:
```sh
cd src
python3 prepare.py /laluan/ke/Humaira_Kartun_Tersusun    # pelekat + assets/manifest.json
mkdir -p assets/fonts && cd assets/fonts \
  && npm pack @fontsource/fredoka@5.0.12 @fontsource/nunito@5.0.17 \
  && for f in *.tgz; do tar xzf "$f" && cp package/files/{fredoka,nunito}-latin-*-normal.woff2 . 2>/dev/null; rm -rf package "$f"; done && cd ../..
python3 -m http.server 8767 --bind 127.0.0.1 &
node render.js schedule              # schedule.json: masa setiap peristiwa
node render.js probe 5,20,41,68      # gambar pegun untuk semakan
node render.js full fr 0 2205        # semua bingkai (boleh dipecah kepada beberapa proses)
python3 audio.py                     # mix_raw.wav
ffmpeg -framerate 30 -i fr/f%05d.png -i mix_raw.wav \
  -c:v libx264 -crf 17 -preset slow -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 \
  -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:a aac -b:a 192k -shortest humaira-tumbesaran.mp4
```
Keperluan: Python (Pillow, numpy), Node + Playwright (Chromium) dan ffmpeg.

Untuk menukar susunan atau label, sunting nama fail di Drive (contoh `031_Humaira_8_Bulan_...png`), kemudian jalankan semula `prepare.py`. Halaman dibina secara automatik mengikut umur.
