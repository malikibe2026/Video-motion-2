import numpy as np, wave
SR = 48000; T = 24.0; N = int(SR * T); t = np.arange(N) / SR
rng = np.random.default_rng(20260930)
def env(a, b, x0, x1):  # smooth ramp a->b between x0,x1
    s = np.clip((t - x0) / (x1 - x0), 0, 1); s = s * s * (3 - 2 * s); return a + (b - a) * s
# pad: A1 + E2 + A2 + C#3, slow detune beating, swells with the zoom
pad = np.zeros(N)
for f, g in [(55, 1.0), (82.41, 0.7), (110, 0.55), (138.59, 0.35), (164.81, 0.25)]:
    for d in (-0.35, 0.35):
        pad += g * np.sin(2 * np.pi * (f + d) * t + rng.uniform(0, 6.28))
pad *= (0.6 + 0.4 * np.sin(2 * np.pi * t / 7.5 - 1.2)) * env(0.0, 1.0, 0.0, 3.0) * env(1.0, 0.0, 22.2, 24.0)
pad *= env(0.55, 1.0, 3, 19)
# whooshes: band-limited noise with rising centre
def whoosh(t0, dur, f0, f1, gain):
    idx = (t >= t0) & (t < t0 + dur); n = idx.sum(); tt = np.arange(n) / SR
    noise = rng.standard_normal(n); out = np.zeros(n)
    # one-pole bandpass approximation via moving centre: sum of 3 resonant sines modulated by noise
    ph = 2 * np.pi * np.cumsum(f0 * (f1 / f0) ** (tt / dur)) / SR
    out = noise * (0.5 + 0.5 * np.sin(ph))
    k = np.ones(24) / 24; out = np.convolve(out, k, 'same')
    w = np.sin(np.pi * tt / dur) ** 2
    y = np.zeros(N); y[idx] = out * w * gain; return y
fx = whoosh(3.1, 2.4, 200, 1400, 0.9) + whoosh(8.6, 1.9, 300, 1800, 0.8) + whoosh(12.3, 1.1, 300, 1500, 0.5) + whoosh(15.8, 1.1, 400, 1600, 0.5)
# label blips
def blip(t0, f, gain, dur=0.35):
    y = np.zeros(N); i0 = int(t0 * SR); n = int(dur * SR); tt = np.arange(n) / SR
    y[i0:i0 + n] = gain * np.sin(2 * np.pi * f * tt) * np.exp(-tt * 14) * (1 - np.exp(-tt * 900)); return y
bl = sum(blip(x, f, g) for x, f, g in [(0.45, 660, .6), (4.89, 740, .6), (7.62, 784, .6), (9.82, 880, .6), (12.56, 988, .6), (15.98, 1175, .6), (18.95, 1319, .8)])
# arrival: soft swell + pulse pings matching the ring
arr = np.zeros(N)
for f, g in [(220, 1), (277.18, .8), (329.63, .8), (440, .5)]:
    arr += g * np.sin(2 * np.pi * f * t)
arr *= env(0, 1, 18.9, 20.2) * env(1, 0, 21.8, 23.9) * (t >= 18.9) * 0.22
pings = sum(blip(18.95 + k * 1.111, 1760, 0.18, 0.5) for k in range(0, 5))
mix = 0.20 * pad / np.abs(pad).max() + 0.55 * fx / max(1e-9, np.abs(fx).max()) * 0.5 + 0.16 * bl + 0.18 * arr / max(1e-9, np.abs(arr).max()) + pings * 0.6
mix *= env(1, 0, 23.2, 24.0)
mix = mix / np.abs(mix).max() * 0.8
st = np.stack([mix, np.roll(mix, 14)], 1)  # tiny Haas offset for width
w = wave.open('mix_raw.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((st * 32767).astype('<i2').tobytes()); w.close()
print('ok', N)
