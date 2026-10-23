# Video 30 saat (9:16): Peringatan Khutbah Jumaat, gaya video-shotcraft

`khutbah-shotcraft-30s-9x16.mp4`: 1080×1920, 30 fps, 30 saat, 6.6 MB, dengan kesan bunyi (tanpa muzik).

## Apa yang diambil daripada `Vincentwei1021/video-shotcraft` (Apache-2.0)
Resipi syot dan parameter (dialih ke enjin kanvas `seek(t)`, tanpa Remotion):
- `effects/spotlight-sweep-moves`: pembuka, lampu sorot menyapu tajuk.
- `typography/marker-underline-title`: garis bawah penanda 10 bingkai di bawah kata kunci, kiri rendah kanan tinggi, lebar 0.12em.
- `camera/depth-layer-moves`: tiga lapisan paralaks 0.35/0.7/1.4, landasan `cubic-bezier(.45,0,.18,1)`, ilustrasi terangkat 1.035x selepas mendarat.
- `transition/card-flip-reveal`: kad zakat, faraid, wasiat, hibah diterbalikkan (4f persediaan, 16f ke 194°, spring ke 180°, selang 12f, cahaya sisi memuncak pada 90°).
- `outro/grain-dissolve`: baris "{ Usia singkat. Harta amanah. }" menjadi butiran dan memadat menjadi "Akhirat kekal." (feTurbulence + feDisplacementMap, skala puncak 52).
Kesan bunyi daripada `assets/audio/sfx` repo itu, semuanya Mixkit dengan URL tercatat: transition-soft, whoosh-fast, pen-write-paper, paper-page-turn, sand-swish, sparkle-touch.

## Apa yang diambil daripada infografik
Ilustrasi sahaja (`src/img/`): jam pasir, mushaf, neraca, periuk duit, ikon zakat/faraid/wasiat/hibah, masjid, pintu syurga dan jahim.
Tidak digunakan: gambaran sahabat, ular dan siluet manusia berapi, teks yang salah eja, tanda air.
Semua teks ditaip semula dengan ejaan dan fakta yang betul.

## Rujukan pada skrin
Hadis riwayat at-Tirmidzi & Ibn Majah · At-Taghabun 64:15 · Al-Munafiqun 63:9 · maksud hadis riwayat al-Bukhari · An-Nazi'at 79:40-41.
