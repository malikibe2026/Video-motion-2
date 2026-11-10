"""Campur narasi suara ke atas muzik cerita.

Guna: python3 audio_narasi.py <fail_suara.(mp3|wav)> [cerita916_schedule.json]
- Suara dipotong ikut jeda kepada 12 baris (satu baris setiap bab).
- Setiap baris diletak pada masa mula bab + ofset (selepas tajuk/gambar pertama).
- Jika baris terlalu panjang untuk ruangnya, ia dipercepat sedikit (maks 1.15x).
- Muzik direndahkan (ducking) ketika suara bercakap.
Hasil: narasi_mix.wav (muzik + suara), narasi_suara.wav (suara sahaja).
"""
import json, subprocess, sys, wave
import numpy as np

SR = 48000
voice_file = sys.argv[1]
sched = json.load(open(sys.argv[2] if len(sys.argv) > 2 else 'cerita916_schedule.json'))
B = 60 / 96
OFF = {'buka': 1.3, 'lahir': 3 * B, 'polaroid': 2 * B, 'panel': 2 * B, 'karusel': 2 * B, 'odometer': 2 * B,
       'setahun': .6, 'laluan': 2 * B, 'kinetik': 2 * B, 'pantai': 2 * B, 'keluarga': 3 * B, 'penutup': 1.5}
scenes = sched['scenes']; total = sched['total'] + .3

def load(path):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', path, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, '<i2').astype(np.float32) / 32768

v = load(voice_file)
# tenaga per 10 ms untuk cari jeda
hop = SR // 100; n = len(v) // hop
e = np.sqrt((v[:n * hop].reshape(n, hop) ** 2).mean(1))
thr = max(1e-4, np.percentile(e, 95) * 0.06)
voiced = e > thr
# kumpulan senyap: (mula, tamat) dalam blok 10 ms
gaps, i = [], 0
while i < n:
    if not voiced[i]:
        j = i
        while j < n and not voiced[j]: j += 1
        if i > 0 and j < n: gaps.append((i, j))
        i = j
    else: i += 1
need = len(scenes) - 1
gaps = sorted(sorted(gaps, key=lambda g: g[1] - g[0], reverse=True)[:need])
if len(gaps) < need:
    sys.exit(f'Hanya {len(gaps)} jeda ditemui, perlu {need}. Semak fail suara.')
cuts = [0] + [((a + b) // 2) for a, b in gaps] + [n]
segs = []
for k in range(len(cuts) - 1):
    a, b = cuts[k], cuts[k + 1]
    idx = np.where(voiced[a:b])[0]
    s0, s1 = a + idx[0], a + idx[-1] + 1
    segs.append(v[max(0, s0 - 3) * hop:min(n, s1 + 6) * hop])

out = np.zeros(int(total * SR), np.float32)
starts = [t0 + OFF.get(name, 2 * B) for name, t0, t1 in scenes]
report = []
for k, seg in enumerate(segs):
    st = starts[k]
    room = (starts[k + 1] - .25 if k + 1 < len(starts) else total - 1.0) - st
    dur = len(seg) / SR
    if dur > room:
        tempo = min(1.15, dur / room)
        p = subprocess.run(['ffmpeg', '-loglevel', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', '-filter:a', f'atempo={tempo:.3f}', '-f', 'f32le', '-'],
                           input=seg.tobytes(), capture_output=True, check=True)
        seg = np.frombuffer(p.stdout, np.float32); dur = len(seg) / SR
        if dur > room: st = max(0, st - (dur - room))       # masih panjang: mula lebih awal
    i0 = int(st * SR); out[i0:i0 + len(seg)] += seg[:len(out) - i0]
    report.append(f'{k + 1:2d} {scenes[k][0]:9s} mula {st:6.2f}s  panjang {dur:4.2f}s  ruang {room:4.2f}s')

def save(path, mono_or_st):
    st = mono_or_st if mono_or_st.ndim == 2 else np.stack([mono_or_st, mono_or_st], 1)
    w = wave.open(path, 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(st, -1, 1) * 32767).astype('<i2').tobytes()); w.close()

out = out / max(1e-9, np.abs(out).max()) * 0.9
save('narasi_suara.wav', out)
# ducking: sampul suara dilicinkan
env = np.convolve(np.abs(out), np.ones(int(.12 * SR)) / int(.12 * SR), 'same')
env = np.clip(env / max(1e-9, np.percentile(env[env > 1e-4], 70)), 0, 1)
env = np.convolve(env, np.ones(int(.25 * SR)) / int(.25 * SR), 'same')
duck = 1 - 0.62 * np.clip(env, 0, 1)
w = wave.open('cerita_mix.wav'); m = np.frombuffer(w.readframes(w.getnframes()), '<i2').reshape(-1, 2).astype(np.float32) / 32768
L = min(len(m), len(out)); m = m[:L] * duck[:L, None]
mix = m + 1.0 * np.stack([out[:L], out[:L]], 1)
mix = mix / np.abs(mix).max() * 0.9
save('narasi_mix.wav', mix)
print('\n'.join(report))
