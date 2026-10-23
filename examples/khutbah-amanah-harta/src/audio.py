import numpy as np, wave
SR = 48000; T = 60.0; N = int(SR * T); t = np.arange(N) / SR
rng = np.random.default_rng(64)
def env(a, b, x0, x1):
    s = np.clip((t - x0) / (x1 - x0), 0, 1); s = s * s * (3 - 2 * s); return a + (b - a) * s
def lp(x, k): return np.convolve(x, np.ones(k) / k, 'same')
# lapisan ambien: hingar ditapis sangat rendah, tiada melodi
bed = lp(lp(rng.standard_normal(N), 200), 200)
bed = bed / np.abs(bed).max() * (0.7 + 0.3 * np.sin(2 * np.pi * t / 11)) * env(0, 1, 0, 2.5) * env(1, 0, 58, 60)
def whoosh(t0, dur, gain):
    idx = (t >= t0) & (t < t0 + dur); n = idx.sum(); tt = np.arange(n) / SR
    o = lp(rng.standard_normal(n), 30) * np.sin(np.pi * tt / dur) ** 2
    y = np.zeros(N); y[idx] = o * gain; return y
fx = sum(whoosh(b - 0.45, 0.9, 1.0) for b in [4.5, 12.5, 21.5, 30.5, 37.5, 46.5, 55.5])
def thump(t0, f, gain, dur=1.2):
    y = np.zeros(N); i0 = int(t0 * SR); n = int(dur * SR); tt = np.arange(n) / SR
    y[i0:i0 + n] = gain * np.sin(2 * np.pi * f * tt) * np.exp(-tt * 3.5) * (1 - np.exp(-tt * 300)); return y
th = thump(0.2, 55, 1.0) + thump(55.6, 50, 1.0)
mix = 0.35 * bed + 0.22 * fx / np.abs(fx).max() + 0.4 * th / np.abs(th).max()
mix = mix / np.abs(mix).max() * 0.8
st = np.stack([mix, np.roll(mix, 14)], 1)
w = wave.open('mix_raw.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype('<i2').tobytes()); w.close()
