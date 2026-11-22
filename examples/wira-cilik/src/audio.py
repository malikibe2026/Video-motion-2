"""Bunyi: muzik wira disintesis dalam kod + SFX pada garis masa + audio asal video.
python3 audio.py  -> out/audio.wav (belum dinormalkan; ffmpeg loudnorm dibuat semasa mux)
"""
import os, subprocess
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve

SR = 48000
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, '..', 'work')
T = dict(ch1=3.0, play1=5.5, slow1=7.5, norm1=12.3, ch2=17.9, slow2=20.1, norm2=24.9, outro=30.3, end=33.8)
N = int(T['end'] * SR) + SR
rng = np.random.default_rng(11)
music = np.zeros((N, 2))
sfx = np.zeros((N, 2))


def lp(x, f, o=2):
    return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x, axis=0)


def hp(x, f, o=2):
    return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x, axis=0)


def bp(x, a, b, o=2):
    return sosfilt(butter(o, [a, b], 'band', fs=SR, output='sos'), x, axis=0)


def put(buf, t, sig, g=1.0, pan=0.0):
    i = int(t * SR)
    if sig.ndim == 1:
        sig = np.stack([sig * (1 - max(0, pan)), sig * (1 + min(0, pan))], 1)
    j = min(N, i + len(sig))
    if j > i >= 0:
        buf[i:j] += sig[:j - i] * g


def tt(d):
    return np.arange(int(d * SR)) / SR


def hz(m):
    return 440 * 2 ** ((m - 69) / 12)


def saw(f, d, det=0.0):
    t = tt(d)
    return 2 * ((t * f * (1 + det)) % 1) - 1


# ---------- instruments ----------
def kick(g=1):
    t = tt(.45)
    f = 45 + 95 * np.exp(-t / .045)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t / .16) * g + .3 * np.exp(-t / .004) * rng.standard_normal(len(t)) * g * .3


def snare():
    t = tt(.3)
    n = bp(rng.standard_normal(len(t)), 1200, 7000) * np.exp(-t / .09)
    return .7 * n + .5 * np.sin(2 * np.pi * 190 * t) * np.exp(-t / .05)


def hat(open_=False):
    t = tt(.25 if open_ else .06)
    return hp(rng.standard_normal(len(t)), 7000) * np.exp(-t / (.08 if open_ else .015)) * .5


def boom(d=3.0):
    t = tt(d)
    f = 32 + 60 * np.exp(-t / .12)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .9)
    n = lp(rng.standard_normal(len(t)), 400) * np.exp(-t / .5) * .6
    return s + n


def impact():
    t = tt(2.5)
    crash = hp(rng.standard_normal(len(t)), 3000) * np.exp(-t / .7) * .35
    return boom(2.5) * .9 + crash + np.pad(kick(), (0, len(t) - len(kick())))


def riser(d):
    t = tt(d)
    n = rng.standard_normal(len(t))
    out = np.zeros(len(t))
    seg = 2400
    for k in range(0, len(t), seg):
        fc = 300 + 9000 * (k / len(t)) ** 2
        out[k:k + seg] = bp(n[max(0, k - 2000):k + seg], fc * .6, min(fc * 1.6, 20000))[-len(n[k:k + seg]):]
    tone = np.sin(2 * np.pi * np.cumsum(200 + 900 * (t / d) ** 2) / SR) * .25
    return (out * .6 + tone) * (t / d) ** 2


def whoosh(d=.7, rev=False):
    t = tt(d)
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2
    s = bp(rng.standard_normal(len(t)), 500, 4000) * env
    return s[::-1] if rev else s


def pop(f0=700):
    t = tt(.18)
    return np.sin(2 * np.pi * np.cumsum(f0 + 1400 * t / .18) / SR) * np.exp(-t / .05) * .6


def shimmer(d, density=10, seed=3):
    r = np.random.default_rng(seed)
    out = np.zeros((int(d * SR) + SR, 2))
    notes = [74, 77, 81, 84, 86, 89, 93]
    for k in range(int(d * density)):
        t0 = r.uniform(0, d)
        tn = tt(.9)
        s = np.sin(2 * np.pi * hz(r.choice(notes)) * tn) * np.exp(-tn / .3) * .12
        pan = r.uniform(-.8, .8)
        i = int(t0 * SR)
        out[i:i + len(s), 0] += s * (1 - max(0, pan))
        out[i:i + len(s), 1] += s * (1 + min(0, pan))
    return out


# D minor epic: Dm - Bb - F - C
CHORDS = [[50, 53, 57], [46, 50, 53], [53, 57, 60], [48, 52, 55]]
BEAT = .5  # 120 BPM


def pad(t0, d, g=.12, att=1.0):
    total = np.zeros((int(d * SR) + 1, 2))
    bar = 4 * BEAT
    nb = int(np.ceil(d / bar))
    for b in range(nb):
        ch = CHORDS[b % 4]
        seg = min(bar, d - b * bar)
        if seg <= 0:
            break
        s = np.zeros(int(seg * SR))
        for m in ch + [ch[0] + 12]:
            for det in (-.004, .004):
                s += saw(hz(m), seg, det)[:len(s)]
        s = lp(s, 1600) / 8
        i = int(b * bar * SR)
        n = len(s)
        fade = np.minimum(1, np.minimum(np.arange(n) / (.04 * SR), (n - np.arange(n)) / (.04 * SR)))
        total[i:i + n, 0] += s * fade
        total[i:i + n, 1] += np.roll(s, 300) * fade
    env = np.minimum(1, np.arange(len(total)) / (att * SR))[:, None]
    put(music, t0, total * env, g)


def groove(t0, d, full=True, g=1.0):
    nb = int(d / BEAT)
    for k in range(nb):
        t = t0 + k * BEAT
        bar_beat = k % 4
        put(music, t, kick(), .9 * g)
        if full and bar_beat in (1, 3):
            put(music, t, snare(), .45 * g)
        if full:
            put(music, t + BEAT / 2, kick(.6), .35 * g) if bar_beat == 3 else None
        for h in range(2 if full else 1):
            put(music, t + h * BEAT / 2, hat(open_=(h == 1 and full)), .35 * g, pan=.3)
        # bass eighths
        root = CHORDS[(k // 4) % 4][0] - 12
        for h in range(2):
            b = lp(saw(hz(root), BEAT / 2 * .9), 500) * np.exp(-tt(BEAT / 2 * .9) / .2)
            put(music, t + h * BEAT / 2, b, .32 * g)
        # brass stabs
        if full and bar_beat in (0, 2):
            ch = CHORDS[(k // 4) % 4]
            s = sum(saw(hz(m + 12), .35, det) for m in ch for det in (-.003, .003))
            s = lp(s, 2800) / 6 * np.exp(-tt(.35) / .14)
            put(music, t, s, .22 * g, pan=-.15)


def snare_roll(t0, d):
    n = 16
    for k in range(n):
        p = k / n
        put(music, t0 + d * (1 - (1 - p) ** 1.6), snare(), .1 + .35 * p)


def drone(t0, d, g=.25):
    t = tt(d)
    s = (np.sin(2 * np.pi * hz(38) * t) + .5 * np.sin(2 * np.pi * hz(50) * t)) * np.sin(np.pi * t / d) ** .5
    put(music, t0, np.stack([s, s], 1), g)


# ---------- score ----------
pad(0, 3.0, .10, att=2.2)
put(music, 0, shimmer(3.0, 7), 1.0)
put(sfx, 1.6, riser(1.4), .55)
put(sfx, 3.0, impact(), .5)
put(sfx, 2.75, whoosh(.5), .5)
pad(3.0, T['play1'] - 3.0 + .2, .08, att=.3)
for i in range(3):
    put(sfx, T['ch1'] + 1.15 + i * .18, pop(650 + 120 * i), .35, pan=(-.5, 0, .5)[i])
for k in range(4):  # pulse tension
    put(music, 3.5 + k * .5, kick(.5), .45)
groove(T['play1'], T['slow1'] - T['play1'], full=False, g=.8)
snare_roll(T['slow1'] - 1.0, 1.0)
put(sfx, T['slow1'] - .35, whoosh(.4, rev=True), .5)
# gerak perlahan 1
put(sfx, T['slow1'], boom(4.0), .5)
drone(T['slow1'], T['norm1'] - T['slow1'], .22)
put(music, T['slow1'] + .5, shimmer(4.0, 5, seed=5), 1.0)
put(sfx, T['norm1'] - 1.3, riser(1.3), .5)
# wira terserlah 1
put(sfx, T['norm1'], impact(), .5)
pad(T['norm1'], T['ch2'] - T['norm1'], .08, att=.2)
groove(T['norm1'], T['ch2'] - T['norm1'] - .5, full=True)
for i in range(3):
    put(sfx, T['norm1'] + .6 + i * .28, whoosh(.35), .3, pan=(-.6, 0, .6)[i])
# peralihan 2
put(sfx, T['ch2'] - 1.2, riser(1.2), .6)
put(sfx, T['ch2'] - .25, whoosh(.5), .55)
put(sfx, T['ch2'], impact(), .5)
groove(T['ch2'], T['slow2'] - T['ch2'], full=False, g=.8)
snare_roll(T['slow2'] - 1.0, 1.0)
put(sfx, T['slow2'] - .35, whoosh(.4, rev=True), .5)
# gerak perlahan 2
put(sfx, T['slow2'], boom(4.0), .5)
drone(T['slow2'], T['norm2'] - T['slow2'], .22)
put(music, T['slow2'] + .5, shimmer(4.0, 5, seed=9), 1.0)
put(sfx, T['norm2'] - 1.3, riser(1.3), .5)
# wira terserlah 2
put(sfx, T['norm2'], impact(), .5)
pad(T['norm2'], T['outro'] - T['norm2'], .08, att=.2)
groove(T['norm2'], T['outro'] - T['norm2'], full=True)
for i in range(3):
    put(sfx, T['norm2'] + .4 + i * .28, whoosh(.35), .3, pan=(-.6, 0, .6)[i])
# penutup
put(sfx, T['outro'], impact(), .5)
pad(T['outro'], T['end'] - T['outro'], .11, att=.1)
put(music, T['outro'] + .3, shimmer(3.0, 6, seed=13), 1.0)

# reverb ringkas
ir_t = tt(1.4)
ir = rng.standard_normal((len(ir_t), 2)) * np.exp(-ir_t / .35)[:, None]
ir /= np.abs(ir).sum(0) ** .5 * 6
wet = np.stack([fftconvolve(music[:, c], ir[:, c])[:N] for c in range(2)], 1)
music = music + wet * .5

# ---------- audio asal video ----------
def orig(name, ss, d, tempo=1.0):
    cmd = ['ffmpeg', '-v', 'error', '-ss', str(ss), '-t', str(d), '-i', os.path.join(WORK, name), '-vn',
           '-af', ('atempo=%g,' % tempo if tempo != 1 else '') + 'aresample=48000', '-ac', '2', '-f', 'f32le', '-']
    a = np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32).reshape(-1, 2).astype(np.float64)
    n = len(a)
    f = int(.03 * SR)
    env = np.ones(n)
    env[:f] = np.linspace(0, 1, f)
    env[-f:] = np.linspace(1, 0, f)
    return a * env[:, None]


vo = np.zeros((N, 2))
put(vo, T['play1'], orig('v1.mp4', 0, 2.0), 1.0)
put(vo, T['slow1'], lp(orig('v1.mp4', 2.0, 2.4, .5), 2500), .7)
put(vo, T['norm1'], orig('v1.mp4', 4.4, 5.6), 1.0)
put(vo, T['ch2'], orig('v2.mp4', 0, 2.2), 1.0)
put(vo, T['slow2'], lp(orig('v2.mp4', 2.2, 2.4, .5), 2500), .7)
put(vo, T['norm2'], orig('v2.mp4', 4.6, 5.4), 1.0)

# duck muzik bila audio asal kuat
lvl = np.sqrt(np.clip(lp(vo.mean(1) ** 2, 4), 0, None))
duck = 1 - .45 * np.clip(lvl / (lvl.max() + 1e-9) * 3, 0, 1)
mix = music * .55 * duck[:, None] + sfx * .7 + vo * .9
# pudar keluar
tail = int(.9 * SR)
e = int(T['end'] * SR)
mix[e - tail:e] *= np.linspace(1, 0, tail)[:, None]
mix[e:] = 0
mix = mix[:e]
print("nan music", np.isnan(music).sum(), "sfx", np.isnan(sfx).sum(), "vo", np.isnan(vo).sum())
mix = np.nan_to_num(mix)
mix /= np.abs(mix).max() / .89
os.makedirs(os.path.join(WORK, 'out'), exist_ok=True)
import wave
with wave.open(os.path.join(WORK, 'out', 'audio.wav'), 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype('<i2').tobytes())
print('audio ok', mix.shape[0] / SR)
