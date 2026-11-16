# Adni Humaira (9:16), video untuk anak

`adni-humaira-9x16.mp4` (66 s, dengan bunyi ambien) dan `adni-humaira-9x16-senyap.mp4` (tanpa audio).
Sumber: `src/adni.html`, bunyi `src/audio_adni.py`, render `PAGE=adni.html node render.js chunk ...` (3 × 660 bingkai).

| Masa | Babak | Isi | Rujukan |
|---|---|---|---|
| 0-6 s | Nama | عَدْنِي حُمَيْرَاء, "Sebuah nama, sebuah doa" | |
| 5.6-12.6 | Adni | 'Adn: syurga tempat menetap yang kekal; taman 'Adn | Ar-Ra'd 13:23 (terjemahan ringkas, perlu disemak) |
| 12.2-18.6 | Humaira | "yang kemerah-merahan" | Makna bahasa |
| 18.2-25.2 | Sempena | Gelaran mesra Rasulullah ﷺ untuk Saidatina 'Aisyah r.a. | |
| 24.8-49.2 | Empat doa | dikasihi, membesar riang, cintakan ilmu, pemurah | Bukhari 3662, Abi Dawud 2578, adh-Dhahabi, Ibn Sa'd |
| 48.8-55.2 | Doa | dalam peliharaan Allah | An-Nur 24:11-20 |
| 54.8-66 | Penutup | Semoga menjadi penghuni syurga 'Adn bersama kami; اللَّهُمَّ بَارِكْ فِيهَا | |

Nota: makna "Adni" di sini diambil daripada kata 'Adn (عدن). Ejaan Arab عَدْنِي ialah andaian; sahkan ejaan yang digunakan keluarga.

---

# Humaira: kisah Saidatina Aisyah r.a. (9:16)

Video 70 saat, 1080×1920, 30 fps. Tiada suara naratif; cerita dibawa oleh teks kinetik dan animasi.
Pencerita senyap ialah **Pelita**, sebuah tanglung comel berpipi merah (merujuk gelaran *Humaira*).

- `humaira-9x16.mp4`: dengan runut bunyi ambien sintesis (pad dan loceng, tiada vokal, tiada sampel luar).
- `humaira-9x16-senyap.mp4`: tanpa audio langsung.

## Prinsip paparan
- **Tiada gambaran wajah atau tubuh** Rasulullah ﷺ, Saidatina Aisyah r.a. atau mana-mana sahabat. Semua tokoh diwakili simbol (bintang, hati, jejak kaki, cawan, pelita).
- Isu sensitif (umur semasa perkahwinan, butiran peristiwa *ifk*) tidak dipaparkan. Peristiwa *ifk* disebut sebagai "difitnah" sahaja beserta rujukan ayat.

## Babak dan sumber (`facts`)
| Masa | Babak | Fakta di skrin | Rujukan |
|---|---|---|---|
| 0-5.8 s | Cangkuk | الحُمَيْرَاء, "Al-Humaira" | Gelaran masyhur. Kebanyakan riwayat yang memuatkan lafaz *al-Humaira* dinilai lemah oleh ulama hadis; sebahagian (cth. riwayat an-Nasa'i dalam *as-Sunan al-Kubra*) dinilai sahih oleh sebahagian ulama. |
| 5.4-11.8 | Makna | "yang kemerah-merahan", merujuk wajah cerah kemerahan | Makna bahasa *humaira'* (bentuk tasghir *hamra'*). |
| 11.4-18.8 | Siapa dia | Aisyah binti Abu Bakar as-Siddiq, ibu Ummu Ruman, lahir di Makkah | Sirah; adh-Dhahabi, *Siyar A'lam an-Nubala'*. |
| 18.4-24.8 | Hijrah | Berhijrah ke Madinah | Sirah. Laluan pada peta ialah ilustrasi, bukan laluan sebenar. |
| 24.4-30.8 | Kasih | Amr bin al-As bertanya siapa yang paling dicintai; jawapan: "Aisyah" | Sahih al-Bukhari 3662; Sahih Muslim 2384. |
| 30.4-37.8 | Berlumba | Berlumba lari dua kali; "Ini untuk yang dulu" (*hadhihi bi tilka*) | Sunan Abi Dawud 2578. |
| 37.4-41.8 | Cawan | Baginda minum di tempat bibirnya menyentuh bekas | Sahih Muslim 300. |
| 41.4-45.8 | Salam | "Wahai Aisy, ini Jibril, dia menyampaikan salam kepadamu" | Sahih al-Bukhari 3217. |
| 45.4-50.3 | Ilmu | 2,210 hadis; sahabat besar merujuk kepadanya | adh-Dhahabi, *Siyar A'lam an-Nubala'* (bilangan 2,210 ialah kiraan masyhur, angka lain wujud); Sunan at-Tirmizi 3883 (kata-kata Abu Musa al-Asy'ari). |
| 49.9-54.3 | Kalung | Kalung tercicir, lalu turun ayat tayammum | Sahih al-Bukhari 334. |
| 53.9-58.3 | Dibela | Allah membersihkan namanya | Surah An-Nur 24:11-20; Sahih al-Bukhari 4750. |
| 57.9-62.3 | Dermawan | 100,000 dirham disedekahkan sehari ketika berpuasa | Ibn Sa'd, *at-Tabaqat al-Kubra* (diriwayatkan oleh pembantunya; juga dalam *Hilyat al-Auliya'*). |
| 61.9-70 | Penutup | Ummul Mukminin; wafat 58 H di Madinah | Al-Ahzab 33:6. Tahun wafat: pendapat masyhur 58 H (ada yang menyebut 57 H); dimakamkan di Baqi'. |

**Sila semak** semua teks Arab, nombor hadis dan terjemahan dengan rujukan asal atau ustaz/ustazah sebelum disiarkan. Teks ditulis daripada ingatan dan tidak disemak secara dalam talian.

## Bina semula
```sh
cd src
npm i @fontsource/fraunces @fontsource/plus-jakarta-sans @fontsource/amiri @fontsource/aref-ruqaa @fontsource/fredoka   # fon sudah disalin ke src/fonts
python3 -m http.server 8777 --bind 127.0.0.1 &
node render.js probe probe/sheet.png 1,8,27,43,63      # lembaran still
node render.js chunk out/part0.mp4 0 700 &              # 3 bahagian selari
node render.js chunk out/part1.mp4 700 1400 &
node render.js chunk out/part2.mp4 1400 2100
python3 audio.py                                        # out/audio.wav, -16 LUFS
```
Pratonton: buka `humaira.html` dalam pelayar (Space main/jeda, ←/→ bingkai, R ulang, `?t=27` lompat ke saat 27).

Fon: Fraunces, Plus Jakarta Sans, Amiri, Aref Ruqaa, Fredoka (semua lesen SIL OFL).
