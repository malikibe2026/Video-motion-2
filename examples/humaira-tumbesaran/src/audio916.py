"""Muzik & bunyi sintesis untuk cerita916.html (tiada sampel luar).

Guna: FILM=cerita916.html node render.js schedule ; python3 audio916.py
Hasil: cerita916_mix.wav. 96 BPM, F - C - Dm - Bb. Susunan ikut bab:
pembukaan senyap dan lapang, dram masuk pada bab polaroid, kemuncak pada
"Genap setahun", santai di pantai, hangat di bab keluarga, dan penutup lembut.
"""
import json, wave
import numpy as np

S = json.load(open('cerita916_schedule.json'))
SR, BEAT = 48000, 60 / 96
T = S['total'] + 0.3
N = int(SR * T); t = np.arange(N) / SR
rng = np.random.default_rng(20261108)
scene = {name: (a, b) for name, a, b in S['scenes']}
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
CH = [[53, 57, 60], [48, 52, 55], [50, 53, 57], [46, 50, 53]]     # F C Dm Bb
chord = lambda x: CH[int(x / (4 * BEAT) + 1e-6) % 4]
# tahap dram setiap bab: 0 tiada, .4 shaker sahaja, 1 penuh, >1 lebih rancak
LEVEL = {'buka': 0, 'lahir': .4, 'polaroid': 1, 'panel': 1, 'sorot': 1.1, 'odometer': 1, 'setahun': 1.4,
         'laluan': 1, 'kinetik': 1.25, 'pantai': .8, 'keluarga': .5, 'penutup': 0}
def level_at(x):
    for name, (a, b) in scene.items():
        if a - 1e-6 <= x < b - 1e-6: return LEVEL.get(name, 1)
    return 0

def ramp(a, b, x0, x1):
    s = np.clip((t - x0) / max(1e-6, x1 - x0), 0, 1); s = s * s * (3 - 2 * s); return a + (b - a) * s

def add(buf, t0, y, gain=1.0):
    i0 = int(t0 * SR)
    if i0 >= N or i0 + len(y) <= 0: return
    a, b = max(0, -i0), min(len(y), N - i0)
    buf[i0 + a:i0 + b] += gain * y[a:b]

def tone(f, dur, kind='bell'):
    n = int(dur * SR); tt = np.arange(n) / SR; att = 1 - np.exp(-tt * 500)
    if kind == 'bell':
        y = (np.sin(2*np.pi*f*tt)*np.exp(-tt*2.8) + .35*np.sin(2*np.pi*2*f*tt)*np.exp(-tt*5.5)
             + .16*np.sin(2*np.pi*3.01*f*tt)*np.exp(-tt*8) + .07*np.sin(2*np.pi*4.17*f*tt)*np.exp(-tt*12))
    elif kind == 'piano':
        y = (np.sin(2*np.pi*f*tt) + .4*np.sin(2*np.pi*2*f*tt)*np.exp(-tt*3) + .15*np.sin(2*np.pi*3*f*tt)*np.exp(-tt*5)) * np.exp(-tt*2.2)
    elif kind == 'bass':
        y = (np.sin(2*np.pi*f*tt) + .25*np.sin(2*np.pi*2*f*tt) + .08*np.sin(2*np.pi*3*f*tt)) * np.exp(-tt*3.4)
    elif kind == 'tick':
        y = np.sin(2*np.pi*f*tt) * np.exp(-tt*55)
    return y * att

def hp(w, L):                      # lulus-tinggi kasar
    return w - np.convolve(w, np.ones(L) / L, 'same')

def kick():
    n = int(.3 * SR); tt = np.arange(n) / SR; f = 44 + 95 * np.exp(-tt * 30)
    return np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-tt * 10) * (1 - np.exp(-tt * 900))
def snap():
    n = int(.14 * SR); tt = np.arange(n) / SR
    return (hp(rng.standard_normal(n), 14) * np.exp(-tt * 34) + .5 * np.sin(2*np.pi*1900*tt) * np.exp(-tt * 70))
def shaker(g=1.0):
    n = int(.07 * SR); tt = np.arange(n) / SR
    return hp(rng.standard_normal(n), 5) * np.exp(-tt * 55) * (1 - np.exp(-tt * 400)) * g

def noise_sweep(dur, f0, f1):
    n = int(dur * SR); w = rng.standard_normal(n); k = np.linspace(0, 1, n); y = np.zeros(n)
    for seg in range(16):
        a, b = seg * n // 16, (seg + 1) * n // 16
        f = f0 * (f1 / f0) ** (seg / 15); L = max(2, int(SR / f / 2))
        y[a:b] = np.convolve(w, np.ones(L) / L, 'same')[a:b]
    return y * np.sin(np.pi * k) ** 2
def riser(dur):
    n = int(dur * SR); k = np.linspace(0, 1, n)
    return hp(rng.standard_normal(n), 10) * k ** 2.4 * .9 + np.sin(2*np.pi*np.cumsum(200 * 4 ** k)/SR) * k ** 2 * .35

pad = np.zeros(N); mus = np.zeros(N); bell = np.zeros(N); fx = np.zeros(N); drum = np.zeros(N)
start_music = scene['lahir'][0]
end_music = scene['penutup'][0] + 2 * BEAT

# pad sepanjang masa
for b in range(int(T / (4 * BEAT)) + 1):
    t0 = b * 4 * BEAT
    if t0 >= T: break
    n = int((4 * BEAT + .6) * SR); tt = np.arange(n) / SR
    e = np.minimum(1, tt / .7) * np.clip((4 * BEAT + .6 - tt) / .7, 0, 1); y = np.zeros(n)
    for m in CH[b % 4]:
        for d in (-.7, .7): y += np.sin(2*np.pi*(hz(m + 12) + d)*tt + rng.uniform(0, 6.3))
    add(pad, t0, y * e, .16)

# bes, arpeggio piano dan dram
k = 0
while k * BEAT < T - 1:
    x = k * BEAT; ch = chord(x); L = level_at(x); bar = k % 4
    if start_music - .01 <= x < end_music:
        if bar in (0, 2): add(mus, x, tone(hz(ch[0] - 12), 1.5, 'bass'), .55)
        if bar == 3 and L >= 1: add(mus, x + BEAT / 2, tone(hz(ch[2] - 12), .5, 'bass'), .35)     # not laluan
        for hh in range(2):
            m = ch[(k * 2 + hh) % 3] + (12 if (k // 2) % 2 else 24)
            add(mus, x + hh * BEAT / 2, tone(hz(m), .9, 'piano'), .085 if L < 1.2 else .1)
    if L >= .8:
        if bar in (0, 2): add(drum, x, kick(), .9 * min(L, 1.2))
        if bar == 2 and L >= 1.2: add(drum, x + BEAT * .75, kick(), .5)
        if bar in (1, 3): add(drum, x, snap(), .34 * min(L, 1.2))
    if L >= .4:
        steps = 4 if L >= 1.3 else 2
        for j in range(steps):
            add(drum, x + j * BEAT / steps, shaker(), (.16 if j % (steps // 2) else .09) * min(1.1, L + .3))
    k += 1

# kilauan menaik di pembukaan
for j, m in enumerate([65, 69, 72, 76, 77, 81, 84]):
    add(bell, .7 + j * .15, tone(hz(m + 12), 2.2), .22)

# penaik (riser) sebelum bab kemuncak
add(fx, scene['setahun'][0] - 1.5, riser(1.5), .9)
add(fx, scene['kinetik'][0] - .9, riser(.9), .5)
# hari jadi: loceng tinggi tambahan
a, b = scene['setahun']; x = a
while x < b - BEAT:
    ch = chord(x); add(bell, x + BEAT / 4, tone(hz(ch[int(x / BEAT) % 3] + 36), .6), .07); x += BEAT / 2

cnt = 0
for e in S['events']:
    x, ty = e['t'], e['type']
    if ty == 'pop':
        ch = chord(x); m = ch[cnt % 3] + 24 + (12 if cnt % 6 >= 3 else 0)
        add(bell, x, tone(hz(min(m, 86)), 1.8), .42); cnt += 1
    elif ty == 'tick':
        add(bell, x, tone(hz([77, 81, 84, 89][e.get('k', 0) % 4] + 12), .5), .1)
    elif ty == 'flip':
        add(fx, x, tone(1500 + 220 * (cnt % 3), .12, 'tick'), .3); cnt += 1
    elif ty == 'stamp':
        add(drum, x, kick(), 1.1); add(fx, x, tone(900, .1, 'tick'), .5)
    elif ty == 'trans':
        kind = e.get('kind')
        if kind in ('pushUp', 'pushLeft', 'whip', 'zoom', 'wipe', 'flood'):
            dur = .5 if kind == 'whip' else .8
            add(fx, x - dur * .4, noise_sweep(dur, 300, 900 if kind == 'zoom' else 2400), .9 if kind == 'whip' else .65)
            if kind == 'flood':
                for j, m in enumerate([72, 77, 81]): add(bell, x + .25 + j * .08, tone(hz(m + 12), 1.4), .13)
        elif kind == 'fade':
            for j, m in enumerate([77, 81, 84]): add(bell, x + j * .09, tone(hz(m + 12), 1.4), .12)
        elif kind == 'flash':
            for j, m in enumerate([72, 77, 81, 84, 89]): add(bell, x + j * .05, tone(hz(m + 12), 1.8), .2)
            add(drum, x + .3, kick(), 1.1)
    elif ty == 'whip':
        add(fx, x - .22, noise_sweep(.5, 300, 2600), .9)
    elif ty == 'roll':
        for j in range(6): add(fx, x - .1 + j * .045, tone(1200 + j * 120, .1, 'tick'), .25)
    elif ty == 'draw':
        n = int(1.3 * SR); tt = np.arange(n) / SR
        f = 300 * (4 ** (tt / 1.3)); add(fx, x, np.sin(2*np.pi*np.cumsum(f)/SR) * np.sin(np.pi*tt/1.3) * .5, .35)
    elif ty == 'confetti':
        for j in range(30): add(fx, x + j * .03 + rng.uniform(0, .02), tone(hz(84 + [0, 4, 7, 12][j % 4]), .4), .15)
    elif ty == 'waves':
        a, b = x, e['t1']; n = int((b - a) * SR); tt = np.arange(n) / SR
        w = np.convolve(rng.standard_normal(n), np.ones(40) / 40, 'same')
        amp = (.55 + .45 * np.sin(2*np.pi*tt/4.2 - 1.5)) * np.minimum(1, tt / .8) * np.clip((b - a - tt) / .8, 0, 1)
        add(fx, a, w * amp, 2.2)
    elif ty == 'outro':
        for j, m in enumerate([65, 69, 72, 77, 81]): add(bell, x + j * .16, tone(hz(m + 12), 3.2), .3)
        add(mus, x + .9, tone(hz(41), 3.5, 'bass'), .6)

nrm = lambda y: y / max(1e-9, np.abs(y).max())
mix = (.20 * nrm(pad) * ramp(0, 1, 0, 1.6) + .40 * nrm(mus) + .46 * nrm(bell) + .20 * nrm(fx) + .30 * nrm(drum))
mix *= ramp(1, 0, T - 2.6, T - .2)
mix = np.tanh(nrm(mix) * 1.25) / np.tanh(1.25) * .88          # had lembut
st = np.stack([mix, np.roll(mix, 18)], 1)
w = wave.open('cerita916_mix.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((st * 32767).astype('<i2').tobytes()); w.close()
print('ok', round(T, 2), 's; bunyi gambar:', cnt)
