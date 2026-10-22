# Narasi: contoh video dashboard REPORT-BORANG (16 s)

Bahasa Malaysia, nada tenang dan jelas. Kadar baca kira-kira 12 aksara sesaat, jadi
setiap baris muat dalam tetingkapnya. Semua angka dalam video ialah **data demo**.

| Masa (s) | Babak | Baris narasi |
|---|---|---|
| 0.3 – 2.8 | Kad tajuk | Laporan BE2026, Unit Harga-Harga. |
| 2.95 – 4.6 | KPI utama | KPI utama sekali pandang. |
| 4.7 – 6.3 | Penapis fasa dan survei | Tapis ikut fasa dan survei. |
| 6.5 – 9.0 | Carta komposisi | Komposisi respon dalam carta. |
| 9.5 – 12.0 | Jadual daerah | Ringkasan setiap daerah. |
| 12.3 – 14.2 | Jadual penyelia | Prestasi mengikut penyelia. |
| 14.9 – 16.0 | Kad penutup | Ini data demo. |

## Cara guna dengan VoiceStudio
1. Pilih **Voice cloning** atau **Voice design**, tampal setiap baris, dan jana satu fail audio
   bagi setiap baris (atau satu fail, dengan jeda mengikut jadual di atas).
2. Jika perlu, letakkan setiap klip pada masa mula dalam jadual, kemudian eksport `narasi.wav`.
3. Gabungkan ke video:

```sh
ffmpeg -i contoh-report-borang-sarikata.mp4 -i narasi.wav \
  -filter_complex "[1:a]loudnorm=I=-14:TP=-1.3:LRA=11,apad[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 256k -t 16 -movflags +faststart \
  contoh-report-borang-suara.mp4
```

Nota: VoiceStudio berlesen AGPL-3.0. Menggunakannya sebagai alat untuk menjana audio tidak
mengikat video anda dengan lesen itu.
