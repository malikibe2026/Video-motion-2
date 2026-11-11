# Humaira: kisah tumbesaran

## Versi 2 (utama): `src/cerita.html`, video bercerita kira-kira 112 saat
Video 1920×1080, 30 fps, 96 BPM. Ada 12 bab, setiap bab dengan gaya visual dan peralihan berbeza, serta sarikata cerita:

| Bab | Gaya visual | Peralihan masuk |
|---|---|---|
| Pembukaan | Langit subuh, matahari terbit, bokeh, sapuan cahaya, tajuk huruf demi huruf | – |
| Hari pertama | Ken Burns, halo, kerlipan bintang, cap tarikh | Pudar |
| Bulan-bulan awal | Polaroid jatuh ke meja, kamera pan, pita washi | Tolak ke atas |
| 7 bulan | Panel belah 4 gaya majalah | Sapuan |
| 8 bulan | Karusel 3D berputar dengan kedalaman | Iris bulat |
| 9–11 bulan | Odometer nombor; buih, kad terbalik 3D, kipas kad | Whip pan |
| Genap setahun | Angka "1" dilukis, sinar berputar, belon, konfeti | Kilat |
| 1 thn 1–3 bln | Laluan tapak kaki, papan tanda, bukit parallax | Tolak ke kiri |
| 1 thn 4–6 bln | Tipografi kinetik warna terang, whip pan antara bulan | Whip pan |
| 1 thn 7 bln | Pantai beranimasi (ombak, awan, burung), flipbook stop-motion | Zum tembus |
| Keluarga | Sinar keemasan berputar, hati terapung | Pudar |
| Penutup | Mozek 78 gambar, nama penuh dan tarikh lahir | Pudar |

Cip umur (kiri atas) dan garis masa 0–19 bulan (bawah) dipaparkan sepanjang cerita.

```sh
FILM=cerita.html node render.js schedule        # cerita_schedule.json
FILM=cerita.html node render.js full fr2 0 3375 # bingkai
python3 audio_cerita.py                         # cerita_mix.wav
ffmpeg -framerate 30 -i fr2/f%05d.png -i cerita_mix.wav -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p \
  -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:a aac -b:a 192k -shortest cerita.mp4
```

**Pembetulan umur:** siri "Meniarap Di Pantai" (018–024) ialah **1 tahun 7 bulan**, bukan bawah 7 bulan seperti pada nama fail. Pembetulan ini dibuat dalam `AGE_OVERRIDES` (`prepare.py`). Fail Drive asal tidak diubah.

`info.json` untuk versi 2 juga memerlukan `nama_penuh`, `lahir` dan `setahun` (cth. `"setahun": "1 Januari 2026"`).

### Versi tegak 9:16 (paling terkini): `src/cerita916.html`
Versi 1080×1920 untuk telefon dan WhatsApp Status, dengan 12 bab dan masa yang sama seperti versi melintang. Ia versi yang paling digilap:

- **Motion blur sebenar:** bingkai dalam tetingkap peralihan dirender sebagai 4 subbingkai (pengatup 180°) dan digabung oleh `blend.py`.
- **Pembukaan:** 12 gambar kecil muncul mengelilingi tajuk.
- **Hari pertama:** mainan gantung berayun dan cap tarikh bulat.
- **8 bulan:** setiap gambar tampil besar, kemudian terbang ke jalur filem di bawah.
- **Genap setahun:** angka "1" menjadi lilin dengan api berkelip.
- **Laluan tapak kaki:** kamera menjejak ke bawah, papan tanda bagi setiap bulan, bunga di tepi laluan.
- **Pantai:** sinar matahari berputar, kilauan laut, daun kelapa berayun, bola terapung.
- **Keluarga:** kartun dan foto sebenar dalam bingkai (`foto_keluarga` dalam `info.json`).
- **Sarikata:** kata bertanda `*` diserlah dengan penanda kuning. Sarikata boleh ditukar melalui `cap_<nama bab>` dalam `info.json`.
- **Muzik (`audio916.py`):** dram lembut dan susunan ikut bab.

```sh
export FILM=cerita916.html VW=1080 VH=1920 SUB=4
node render.js schedule                 # cerita916_schedule.json
node render.js full fr3 0 3375          # bingkai; yang bermotion blur ke fr3_sub/
python3 blend.py fr3                    # gabung subbingkai
python3 audio916.py                     # cerita916_mix.wav
ffmpeg -framerate 30 -i fr3/f%05d.png -i cerita916_mix.wav -c:v libx264 -crf 19 -preset slow -pix_fmt yuv420p \
  -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:a aac -b:a 192k -shortest cerita916.mp4
```
**Muzik daripada lagu sebenar (`audio_lagu.py`):** letak `assets/lagu/latar.mp3` dan `assets/lagu/birthday.mp3` (tidak di-commit, hak cipta pemiliknya), kemudian jalankan `python3 audio_lagu.py` untuk menghasilkan `cerita916_lagu.wav`.
- Lagu latar dimainkan dari awal hingga bab "Genap setahun".
- Lagu hari jadi dimainkan sepanjang bab itu sahaja.
- Lagu latar kemudian disambung semula, dengan titik sambung dipilih supaya korus (`KORUS`) jatuh tepat pada bab pantai.
- Kesan bunyi bernada tidak digunakan supaya tidak bertembung dengan kunci lagu.

`info.json` juga menerima `buang` (senarai nombor gambar yang tidak dipaparkan). Untuk WhatsApp Status (maksimum 60 s), video dipecah kepada dua bahagian pada sempadan bab "Genap setahun" (53.1 s).

## Versi 1: `src/film.html`, montaj 73 saat
Versi pertama dibuat sebelum pembetulan umur. Selepas `prepare.py` dikemas kini, versi ini tidak lagi memaparkan flipbook pantai di bahagian "Bawah 7 Bulan".

Video montaj 1920×1080, 30 fps, kira-kira 73 saat, 120 BPM. Ia menggunakan 78 ilustrasi kartun berlatar telus daripada folder Drive `Humaira_Kartun_Tersusun`.

**Repo ini hanya menyimpan kod.** Gambar kartun, video siap, fail audio serta nama penuh dan tarikh lahir (`assets/info.json`) tidak di-commit kerana ia maklumat peribadi kanak-kanak. Semua fail itu tersenarai dalam `.gitignore`. Tanpa `info.json`, tajuk memaparkan "Humaira" sahaja.

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
# pilihan: nama & tarikh lahir untuk tajuk (fail ini tidak di-commit)
cat > assets/info.json <<'EOF'
{"nama": "Nama Panggilan", "intro_sub": "Lahir 1 Januari 2025",
 "outro_sub1": "Nama penuh", "outro_sub2": "Lahir 1 Januari 2025 · 78 ilustrasi kartun · 18 bulan kenangan"}
EOF
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
