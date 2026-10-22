import numpy as np, wave
SR = 48000; T = 51.4; N = int(SR * T); t = np.arange(N) / SR
rng = np.random.default_rng(20260930)
def env(a, b, x0, x1):
    s = np.clip((t - x0) / (x1 - x0), 0, 1); s = s * s * (3 - 2 * s); return a + (b - a) * s
def lp(x, k):
    return np.convolve(x, np.ones(k) / k, 'same')
# ---- pad: major-ish until 24, minor after; fades down toward barzakh
def chord(freqs):
    y = np.zeros(N)
    for f, g in freqs:
        for d in (-0.35, 0.35): y += g * np.sin(2 * np.pi * (f + d) * t + rng.uniform(0, 6.28))
    return y
pa = chord([(55, 1.0), (82.41, 0.7), (110, 0.55), (138.59, 0.35), (164.81, 0.25)])
pb = chord([(55, 1.0), (82.41, 0.7), (110, 0.55), (130.81, 0.35), (164.81, 0.25)])
mixab = env(0, 1, 23, 26)
pad = pa * (1 - mixab) + pb * mixab
pad *= (0.6 + 0.4 * np.sin(2 * np.pi * t / 7.5 - 1.2))
pad *= env(0, 1, 0, 3) * env(0.55, 1.0, 3, 19) * env(1, 0.45, 24, 34) * env(1, 0.06, 40.5, 42.8) * env(1, 0, 49.5, 51.4)
pad = 0.20 * pad / np.abs(pad).max()
# ---- whooshes
def whoosh(t0, dur, f0, f1, gain):
    idx = (t >= t0) & (t < t0 + dur); n = idx.sum(); tt = np.arange(n) / SR
    noise = rng.standard_normal(n); ph = 2 * np.pi * np.cumsum(f0 * (f1 / f0) ** (tt / dur)) / SR
    o = lp(noise * (0.5 + 0.5 * np.sin(ph)), 24) * np.sin(np.pi * tt / dur) ** 2
    y = np.zeros(N); y[idx] = o * gain; return y
fx = whoosh(3.1, 2.4, 200, 1400, 0.9) + whoosh(8.6, 1.9, 300, 1800, 0.8) + whoosh(12.3, 1.1, 300, 1500, 0.5) + whoosh(15.8, 1.1, 400, 1600, 0.5) + whoosh(24.8, 5.6, 150, 800, 0.45) + whoosh(35.2, 1.9, 120, 500, 0.4)
fx = 0.28 * fx / np.abs(fx).max()
# ---- blips and tones
def blip(t0, f, gain, dur=0.35, dec=14):
    y = np.zeros(N); i0 = int(t0 * SR); n = int(dur * SR); tt = np.arange(n) / SR
    y[i0:i0 + n] = gain * np.sin(2 * np.pi * f * tt) * np.exp(-tt * dec) * (1 - np.exp(-tt * 900)); return y
bl = sum(blip(x, f, g) for x, f, g in [(0.45, 660, .6), (4.89, 740, .6), (7.62, 784, .6), (9.82, 880, .6), (12.56, 988, .6), (15.98, 1175, .6), (18.95, 1319, .8), (28.8, 660, .6), (35.4, 523, .6), (42.8, 440, .6)])
tones = sum(blip(x, f, 0.5, 2.2, 1.6) for x, f in [(20.4, 330), (30.6, 330), (44.0, 294)])
# ---- lahad foley (sintesis ringkas)
def thud(t0, f, gain, dur=0.7):
    y = np.zeros(N); i0 = int(t0 * SR); n = int(dur * SR); tt = np.arange(n) / SR
    y[i0:i0 + n] = gain * np.sin(2 * np.pi * f * np.exp(-tt * 3) * tt * 0 + 2 * np.pi * f * tt) * np.exp(-tt * 7); return y
def burst(t0, dur, gain, k, dec):
    y = np.zeros(N); i0 = int(t0 * SR); n = int(dur * SR); tt = np.arange(n) / SR
    y[i0:i0 + n] = gain * lp(rng.standard_normal(n), k) * np.exp(-tt * dec); return y
def swell(t0, t1, gain, k):
    y = np.zeros(N); i0, i1 = int(t0 * SR), int(t1 * SR); n = i1 - i0; tt = np.arange(n) / SR
    y[i0:i1] = gain * lp(rng.standard_normal(n), k) * np.sin(np.pi * tt / (t1 - t0)) ** 2; return y
fol = thud(35.2, 52, 0.5) + burst(37.2, 0.6, 0.5, 40, 5) + burst(38.5, 0.12, 1.0, 6, 40) + thud(38.5, 180, 0.3, 0.15) + burst(38.66, 0.12, 0.9, 6, 40) + thud(38.66, 170, 0.3, 0.15) + swell(39.5, 40.8, 0.8, 30) + thud(40.8, 48, 0.55)
fol = 0.3 * fol / np.abs(fol).max()
# ---- barzakh: hampir sunyi, desiran halus, swell pada soalan penutup
bz = (np.sin(2 * np.pi * 41 * t) * 0.8 + 0.06 * np.sin(2 * np.pi * 1320 * t) * (0.5 + 0.5 * np.sin(2 * np.pi * t / 6)) + 0.04 * np.sin(2 * np.pi * 1760 * t) * (0.5 + 0.5 * np.sin(2 * np.pi * t / 8 + 1)))
bz *= env(0, 1, 42.4, 45.0) * env(1, 0, 50.0, 51.4) * 0.07
q = (np.sin(2 * np.pi * 110 * t) + 0.7 * np.sin(2 * np.pi * 164.81 * t) + 0.5 * np.sin(2 * np.pi * 220 * t)) * env(0, 1, 48.3, 49.8) * env(1, 0, 50.2, 51.4) * 0.09
mix = pad + fx + 0.16 * bl + 0.12 * tones + fol + bz + q
mix *= env(1, 0, 50.9, 51.4)
mix = mix / np.abs(mix).max() * 0.8
st = np.stack([mix, np.roll(mix, 14)], 1)
w = wave.open('mix2_raw.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((st * 32767).astype('<i2').tobytes()); w.close(); print('ok', N)
