# Runut bunyi ambien sintesis (tiada vokal, tiada sampel luar): pad lembut,
# loceng kotak muzik pada setiap pendedahan, desir peralihan babak.
import numpy as np, wave, subprocess, os
SR, T = 48000, 70.0
N = int(SR * T); t = np.arange(N) / SR
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(7)
def hz(m): return 440 * 2 ** ((m - 69) / 12)
def add(sig, at, pan=0.0, g=1.0):
    i = int(at * SR); j = min(N, i + len(sig))
    if i >= N: return
    s = sig[:j - i] * g
    L[i:j] += s * np.sqrt((1 - pan) / 2) * 1.414; R[i:j] += s * np.sqrt((1 + pan) / 2) * 1.414
def lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); acc = 0.0
    for k in range(len(x)): acc = (1 - a) * x[k] + a * acc; y[k] = acc
    return y
# ---- pad: kord berubah pada setiap babak ----
chords = [(0, [50, 57, 62, 66, 69, 76]), (5.4, [47, 54, 59, 62, 66, 73]), (11.4, [43, 50, 55, 59, 62, 69]), (18.4, [45, 52, 57, 61, 64, 71]),
          (24.4, [50, 57, 62, 66, 69, 74]), (30.4, [47, 54, 59, 62, 66, 71]), (37.4, [43, 50, 55, 59, 64, 71]), (41.4, [45, 52, 57, 62, 64, 69]),
          (45.4, [50, 57, 62, 64, 66, 73]), (49.9, [47, 54, 59, 62, 64, 71]), (53.9, [40, 47, 52, 55, 59, 66]), (56.0, [43, 50, 55, 59, 62, 69]),
          (57.9, [45, 52, 57, 61, 64, 69]), (61.9, [50, 57, 62, 66, 69, 74])]
pad = np.zeros(N)
for k, (a, notes) in enumerate(chords):
    b = chords[k + 1][0] if k + 1 < len(chords) else T
    i0 = max(0, int((a - 1.0) * SR)); i1 = min(N, int((b + 1.2) * SR)); tt = t[i0:i1]
    env = np.clip((tt - (a - 1.0)) / 1.6, 0, 1) * np.clip(((b + 1.2) - tt) / 1.6, 0, 1)
    env = np.sin(env * np.pi / 2) ** 2
    s = np.zeros_like(tt)
    for n in notes:
        f = hz(n)
        for d in (-0.07, 0.07):
            s += np.sin(2 * np.pi * f * (1 + d / 100) * tt + rng.random() * 6) * (0.5 if n < 52 else 0.32)
            s += 0.12 * np.sin(2 * np.pi * 2 * f * tt + rng.random() * 6)
    pad[i0:i1] += s * env
pad *= 0.6 + 0.4 * np.sin(2 * np.pi * 0.11 * t)
pad = lp(pad, 1400)
L += pad * 0.05; R += pad * 0.05
# ---- bunyi ----
def chime(m, dur=2.2, g=1.0):
    n = int(dur * SR); x = np.arange(n) / SR; f = hz(m)
    s = (np.sin(2 * np.pi * f * x) + .35 * np.sin(2 * np.pi * 2 * f * x) * np.exp(-x * 6) + .12 * np.sin(2 * np.pi * 3.01 * f * x) * np.exp(-x * 9))
    return s * np.exp(-x * 2.6) * np.minimum(1, x * 400) * g
def whoosh(dur=1.0, g=1.0, up=True):
    n = int(dur * SR); x = np.arange(n) / SR; w = rng.standard_normal(n)
    w = lp(w, 1800 if up else 900); e = np.sin(np.pi * x / dur) ** 2
    return w * e * g
def thump(f0=110, dur=.35, g=1.0):
    n = int(dur * SR); x = np.arange(n) / SR; f = f0 * (1 + 1.5 * np.exp(-x * 30))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x * 11) * g
def pop(f0=600, g=1.0):
    n = int(.12 * SR); x = np.arange(n) / SR; f = f0 * (1 + 2 * x * 8)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x * 40) * g
def shimmer(dur=2.5, g=1.0, base=84):
    out = np.zeros(int((dur + 2.5) * SR))
    for k in range(14):
        m = base + [0, 2, 4, 7, 9][k % 5] + 12 * (k // 10)
        c = chime(m, 2.0, .5); i = int(k / 14 * dur * SR); out[i:i + len(c)] += c
    return out * g
PENTA = [74, 76, 78, 81, 83, 86, 88, 90]
def arp(at, notes, gap=.11, g=.5):
    for i, m in enumerate(notes): add(chime(m, 2.4, g), at + i * gap, pan=(i % 3 - 1) * .4)
for a in [5.4, 11.4, 18.4, 24.4, 30.4, 37.4, 41.4, 45.4, 49.9, 53.9, 57.9, 61.9]: add(whoosh(1.1, 1.0), a - .55, g=.045)
arp(1.0, [74, 78, 81, 86, 90], .16, .55)       # kaligrafi Humaira
add(thump(90, .5), 1.05, g=.35)                 # pelita mendarat
arp(6.0, [81, 83, 86, 90], .12, .45)
arp(12.0, [78, 81, 85, 90], .14, .45)
arp(19.2, [74, 76, 78, 81], .2, .35)
add(chime(93, 2.5, .5), 23.3)                   # tiba di Madinah
for k in range(5): add(thump(70, .4), 26.6 + k * .82, g=.35); add(thump(70, .3), 26.85 + k * .82, g=.22)  # degup jantung
arp(27.0, [86, 90, 93], .12, .5)
add(chime(88, 2, .5), 32.4); add(chime(81, 2, .5), 35.7); arp(35.75, [86, 88], .1, .35)
add(pop(700, .4), 38.8); arp(39.6, [90, 93], .1, .4)
add(shimmer(2.2, .5, 86), 41.9); add(whoosh(1.4, .8, False), 41.6, g=.05)
for i in range(5): add(pop(420 + i * 70, .55), 46.0 + i * .22)
for i in range(14): add(pop(900 + (i % 5) * 120, .25), 50.95 + i * .03 + .55, pan=(i / 7 - 1) * .7)
add(shimmer(2.0, .35, 81), 52.0)
rum = lp(rng.standard_normal(int(2.4 * SR)), 140); x = np.arange(len(rum)) / SR
add(rum * np.sin(np.pi * x / 2.4) ** 2 * 4, 54.0, g=.4)
arp(56.1, [74, 78, 81, 86, 90, 93], .13, .5)
for i in range(18): add(pop(1200 + (i % 4) * 150, .18), 58.9 + i * .17, pan=np.sin(i) * .7)
arp(62.5, [74, 78, 81, 86], .18, .45)
add(shimmer(1.5, .4, 86), 67.2)
arp(66.0, [86, 85, 81, 78, 74], .2, .45)
# ---- tamat ----
fade = np.clip((70 - t) / 1.2, 0, 1); L *= fade; R *= fade
st = np.stack([L, R], 1); st /= np.max(np.abs(st)) * 1.05
os.makedirs('out', exist_ok=True)
with wave.open('out/raw.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype('<i2').tobytes())
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', 'out/raw.wav', '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-ar', '48000', 'out/audio.wav'], check=True)
print('ok')
