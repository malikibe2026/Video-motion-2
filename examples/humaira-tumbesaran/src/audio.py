"""Muzik dan bunyi sintesis (tiada sampel luar, tiada isu lesen).

Guna: python3 audio.py   (perlukan schedule.json daripada `node render.js schedule`)
Hasil: mix_raw.wav (stereo 48 kHz). Normalkan dengan ffmpeg loudnorm selepas itu.

120 BPM, F major, kord F - Dm - Bb - C setiap bar. Setiap gambar yang muncul
dibunyikan sebagai satu not kotak muzik daripada kord semasa.
"""
import json, wave
import numpy as np

S = json.load(open('schedule.json'))
SR, BPM = 48000, 120
BEAT = 60 / BPM
T = S['total'] + 0.2
N = int(SR * T)
t = np.arange(N) / SR
rng = np.random.default_rng(20261108)

def hz(m): return 440 * 2 ** ((m - 69) / 12)
# kord (nota MIDI) setiap bar 4 ketukan
CHORDS = [[53, 57, 60], [50, 53, 57], [46, 50, 53], [48, 52, 55]]  # F Dm Bb C
def chord_at(x): return CHORDS[int(x / (4 * BEAT)) % 4]

def env_ramp(a, b, x0, x1):
    s = np.clip((t - x0) / (x1 - x0), 0, 1); s = s * s * (3 - 2 * s); return a + (b - a) * s

def note(buf, t0, f, dur, gain, kind='bell'):
    i0 = int(t0 * SR); n = min(int(dur * SR), N - i0)
    if n <= 0 or i0 < 0: return
    tt = np.arange(n) / SR
    att = 1 - np.exp(-tt * 600)
    if kind == 'bell':      # kotak muzik: asas + separa tak harmonik
        y = (np.sin(2 * np.pi * f * tt) * np.exp(-tt * 3.2) + 0.35 * np.sin(2 * np.pi * f * 2.0 * tt) * np.exp(-tt * 6)
             + 0.18 * np.sin(2 * np.pi * f * 3.01 * tt) * np.exp(-tt * 9) + 0.08 * np.sin(2 * np.pi * f * 4.2 * tt) * np.exp(-tt * 14))
    elif kind == 'pluck':   # bes lembut
        y = (np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(2 * np.pi * 2 * f * tt)) * np.exp(-tt * 4.5)
    elif kind == 'tick':    # ketukan kayu kecil
        y = np.sin(2 * np.pi * f * tt) * np.exp(-tt * 60)
    buf[i0:i0 + n] += gain * att * y

music = np.zeros(N); bells = np.zeros(N); sfx = np.zeros(N)

# pad: kord lembut, serangan perlahan
pad = np.zeros(N)
for b in range(int(T / (4 * BEAT)) + 1):
    t0 = b * 4 * BEAT; ch = CHORDS[b % 4]
    i0 = int(t0 * SR); i1 = min(N, int((t0 + 4 * BEAT + 0.4) * SR))
    if i0 >= N: break
    tt = np.arange(i1 - i0) / SR
    e = np.minimum(1, tt / 0.5) * np.minimum(1, np.maximum(0, (4 * BEAT + 0.4 - tt) / 0.5))
    for m in ch:
        for d in (-0.6, 0.6):
            pad[i0:i1] += e * np.sin(2 * np.pi * (hz(m + 12) + d) * tt + rng.uniform(0, 6.3)) * 0.18

# bes pada ketukan 1 dan 3, arpeggio not 1/8 selepas intro
for k in range(int(T / BEAT)):
    x = k * BEAT; ch = chord_at(x)
    if x > S['total'] - 3.2: break
    if k % 2 == 0: note(music, x, hz(ch[0] - 12), 1.2, 0.55, 'pluck')
    if x >= 2.5:
        for h in range(2):
            m = ch[(k * 2 + h) % 3] + 12
            note(music, x + h * BEAT / 2, hz(m), 0.6, 0.10, 'bell')

# not loceng untuk setiap gambar
cnt = 0
for e in S['events']:
    x = e['t']
    if e['type'] == 'pop':
        ch = chord_at(x); m = ch[cnt % 3] + 24 + (12 if cnt % 6 >= 3 else 0)
        m = min(m, 84); note(bells, x, hz(m), 1.6, 0.5, 'bell'); cnt += 1
    elif e['type'] == 'flip':
        note(sfx, x, 1600 + 200 * (cnt % 3), 0.15, 0.35, 'tick'); cnt += 1
    elif e['type'] == 'page' and x > 3.1:
        # desiran lembut sebelum halaman baru
        i0 = int((x - 0.32) * SR); n = int(0.55 * SR)
        if i0 + n < N:
            w = rng.standard_normal(n); w = np.convolve(w, np.ones(30) / 30, 'same')
            tt = np.arange(n) / n; sfx[i0:i0 + n] += 0.9 * w * np.sin(np.pi * tt) ** 2
    elif e['type'] == 'confetti':
        for j in range(26):
            note(sfx, x + j * 0.035 + rng.uniform(0, .02), hz(84 + [0, 4, 7, 12][j % 4]), 0.4, 0.16, 'bell')

# tajuk pembukaan dan penutup: arpeggio menaik
for j, m in enumerate([65, 69, 72, 77]):
    note(bells, 0.35 + j * 0.12, hz(m + 12), 2.0, 0.35, 'bell')
o = S['outro']
for j, m in enumerate([65, 69, 72, 77, 81]):
    note(bells, o + 0.4 + j * 0.14, hz(m + 12), 3.0, 0.38, 'bell')

def nrm(x): return x / max(1e-9, np.abs(x).max())
mix = 0.22 * nrm(pad) * env_ramp(0, 1, 0, 1.5) + 0.42 * nrm(music) + 0.55 * nrm(bells) + 0.18 * nrm(sfx)
mix *= env_ramp(1, 0, T - 2.5, T - 0.2)
mix = nrm(mix) * 0.85
st = np.stack([mix, np.roll(mix, 18)], 1)
w = wave.open('mix_raw.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((st * 32767).astype('<i2').tobytes()); w.close()
print('ok', round(T, 2), 's, gambar berbunyi:', cnt)
