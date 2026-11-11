"""Campur lagu sebenar (disediakan pengguna) dengan kesan bunyi halus untuk cerita916.html.

Guna: python3 audio_lagu.py   (perlukan cerita916_schedule.json dan assets/lagu/*.mp3)
- assets/lagu/latar.mp3    : lagu latar keseluruhan video
- assets/lagu/birthday.mp3 : lagu hari jadi, hanya sepanjang bab 'setahun'
Selepas bab 'setahun', lagu latar disambung semula. Titik sambung dipilih supaya
korus lagu latar (KORUS saat dalam lagu) jatuh tepat pada permulaan bab 'pantai'.
Fail lagu tidak di-commit (hak cipta pemiliknya). Hasil: cerita916_lagu.wav
"""
import json, subprocess, wave
import numpy as np

SR = 48000
LATAR_MULA = 0.8      # saat dalam lagu latar tempat bunyi bermula
KORUS = 80.0          # saat dalam lagu latar tempat korus pertama bermula
BDAY_MULA = 2.9       # saat dalam lagu hari jadi; muziknya bermula 3.2 s, jatuh pada puncak kilat
XF = .45              # tempoh silang pudar (s)
S = json.load(open('cerita916_schedule.json'))
T = S['total']; N = int(T * SR); t = np.arange(N) / SR
sc = {n: (a, b) for n, a, b in S['scenes']}
rng = np.random.default_rng(7)


def load(p):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', p, '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2)


def seg(x, a, dur):
    i0 = int(a * SR); y = x[i0:i0 + int(dur * SR)]
    return np.pad(y, ((0, int(dur * SR) - len(y)), (0, 0)))


def place(y, at):                     # letak segmen y pada masa video `at`
    z = np.zeros((N, 2), np.float32); i0 = int(at * SR)
    a, b = max(0, -i0), min(len(y), N - i0); z[i0 + a:i0 + b] = y[a:b]; return z


def fade(a, b, x0, x1):               # sampul licin a->b antara x0..x1 (masa video)
    s = np.clip((t - x0) / max(1e-6, x1 - x0), 0, 1); s = s * s * (3 - 2 * s); return a + (b - a) * s


rms = lambda y: float(np.sqrt((y ** 2).mean())) + 1e-9

latar, bday = load('assets/lagu/latar.mp3'), load('assets/lagu/birthday.mp3')
s0, s1 = sc['setahun']; p0 = sc['pantai'][0]
resume = KORUS - (p0 - s1)

A = place(seg(latar, LATAR_MULA, s0 + XF), 0)                          # awal -> setahun
Bd = place(seg(bday, BDAY_MULA - .1, s1 - s0 + .1 + XF), s0 - .1)      # hari jadi
C = place(seg(latar, resume - XF, T - s1 + XF), s1 - XF)               # latar disambung

gB = rms(latar[int(20 * SR):int(54 * SR)]) / rms(bday[int(3.2 * SR):int(11 * SR)]) * 1.45   # hari jadi sedikit lebih kuat daripada verse
eA = fade(1, 0, s0 - .15, s0 + XF - .1)
eB = fade(0, 1, s0 - .1, s0 + .05) * fade(1, 0, s1 - .2, s1 + XF)
eC = fade(0, 1, s1 - .25, s1 + XF) * fade(1, 0, T - 3.6, T - .15)
music = A * eA[:, None] + Bd * (eB * gB)[:, None] + C * eC[:, None]

# ---- kesan bunyi halus tanpa nada (tidak bertembung dengan kunci lagu) ----
fx = np.zeros(N, np.float32)


def add(y, at, g):
    i = int(at * SR)
    if i >= N or i + len(y) <= 0: return
    a, b = max(0, -i), min(len(y), N - i); fx[i + a:i + b] += g * y[a:b]


def sweep(dur, f0, f1):
    n = int(dur * SR); w = rng.standard_normal(n); k = np.linspace(0, 1, n); y = np.zeros(n)
    for j in range(16):
        a, b = j * n // 16, (j + 1) * n // 16; L = max(2, int(SR / (f0 * (f1 / f0) ** (j / 15)) / 2))
        y[a:b] = np.convolve(w, np.ones(L) / L, 'same')[a:b]
    return y * np.sin(np.pi * k) ** 2


def tick(f, dur=.08):
    tt = np.arange(int(dur * SR)) / SR; return np.sin(2 * np.pi * f * tt) * np.exp(-tt * 70)


def pop():                            # "pop" lembut: sapuan turun pantas, tiada nada tetap
    tt = np.arange(int(.09 * SR)) / SR; f = 900 * np.exp(-tt * 28) + 180
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 40) * (1 - np.exp(-tt * 2000))


for e in S['events']:
    x, ty = e['t'], e['type']
    if ty == 'pop': add(pop(), x, .35)
    elif ty == 'tick': add(pop(), x, .18)
    elif ty == 'flip': add(tick(1600), x, .25)
    elif ty == 'roll':
        for j in range(6): add(tick(1200 + j * 120), x - .1 + j * .045, .2)
    elif ty == 'whip': add(sweep(.5, 300, 2600), x - .22, .8)
    elif ty == 'trans' and e.get('kind') in ('pushUp', 'pushLeft', 'whip', 'zoom', 'wipe', 'flood'):
        d = .5 if e['kind'] == 'whip' else .8
        add(sweep(d, 300, 900 if e['kind'] == 'zoom' else 2400), x - d * .4, .7)
    elif ty == 'waves':
        a, b = x, e['t1']; n = int((b - a) * SR); tt = np.arange(n) / SR
        w = np.convolve(rng.standard_normal(n), np.ones(40) / 40, 'same')
        add(w * (.55 + .45 * np.sin(2 * np.pi * tt / 4.2 - 1.5)) * np.minimum(1, tt / .8) * np.clip((b - a - tt) / .8, 0, 1), a, 1.6)

fx = fx / max(1e-9, np.abs(fx).max()) * rms(music) * 2.2
mix = music + np.stack([fx, fx * .96], 1)
mix = mix / max(1e-9, np.abs(mix).max()) * .92
w = wave.open('cerita916_lagu.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((np.clip(mix, -1, 1) * 32767).astype('<i2').tobytes()); w.close()
print(f'ok {T:.2f}s | latar {LATAR_MULA}-{LATAR_MULA + s0:.1f}s | hari jadi {BDAY_MULA}-{BDAY_MULA + s1 - s0:.1f}s '
      f'pada video {s0:.2f}-{s1:.2f}s | latar disambung dari {resume:.2f}s, korus pada video {p0:.2f}s')
