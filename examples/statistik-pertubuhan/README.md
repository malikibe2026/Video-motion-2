# Video: Dashboard Statistik Utama Pertubuhan (48 s, 9:16)

`statistik-pertubuhan-9x16.mp4`: 1080×1920, 30 fps, 48 saat, 11.6 MB, dengan muzik dan kesan bunyi.

## Sumber
- Aplikasi: folder `dashboard-mko/` dalam repo `malikibe2026/WARGAWP` (cabang `main`, commit `bf55f51`), iaitu sumber tapak Netlify `statistik-pertubuhan-be`.
- UI yang dipaparkan ialah **tangkapan skrin dashboard sebenar** yang dijalankan secara setempat.
- **Semua data dalam video ialah REKAAN** (`src/gen_data.py`, 780 pertubuhan fiksyen, "Pertubuhan Contoh 0001 Sdn. Bhd.", "Pegawai A (Tetap)"). Panggilan Supabase dipintas dan diganti data rekaan; tiada data sebenar dimuat atau dipaparkan. Video menanda "DATA REKAAN · DEMO".
- Pautan tapak tidak dipaparkan kerana README aplikasi menyatakan pautan untuk kegunaan dalaman sahaja.

## Struktur (setiap potongan tepat pada bar muzik, 130 BPM)
Pembuka (logo + tajuk) · Muat naik Excel · Klimaks: kad Pencapaian Selesai + 5 KPI · 4 sektor (kad diterbalikkan) · Status pencapaian + Penemuan utama (paralaks) · Trend harian + donut status respon · Peta 11 parlimen KL + kedudukan · Kad skor pegawai kerja luar · Analisis nilai (serakan + kes perlu semakan) · Penutup (lockup logo).
Resipi gerakan dipinjam daripada `video-shotcraft` (depth-layer-moves, card-flip-reveal, deck-deal-flyin, marker-underline-title).

## Audio
- Muzik: "Cat Walk", Arulo (Mixkit Stock Music Free License), https://assets.mixkit.co/music/371/371.mp3, bermula 7.391 s supaya klimaks lagu (14.77 s) jatuh pada babak KPI.
- Kesan bunyi Mixkit daripada `video-shotcraft/assets/audio` (whoosh-fast, swoosh-quick, impact-transition, data-scan, sparkle-touch, power-up-electronic).

## Bina semula
`src/gen_data.py` (data rekaan) → `src/cap2.js` (tangkap kad dashboard, perlu salinan `dashboard-mko` dengan pustaka setempat) → `src/film.html` + `src/fdrive.js` (render bingkai).
