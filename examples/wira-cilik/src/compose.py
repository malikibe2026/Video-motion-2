"""Gabung Video 1 + Video 2 dengan kamera, peralihan, gerak perlahan dan lapisan grafik.

python3 compose.py probe t1 t2 ...        -> probe/c_<t>.jpg
python3 compose.py chunk k n              -> out/chunk_k.mp4 (bahagian k daripada n)
"""
import sys, os, math, subprocess
import numpy as np
from PIL import Image, ImageFilter

FPS = 30
W, H = 1920, 1080
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, '..', 'work')
T = dict(intro_end=3.0, ch1=3.0, play1=5.5, slow1=7.5, norm1=12.3, ch2=17.9,
         slow2=20.1, norm2=24.9, outro=30.3, end=33.8)
NFRAMES = int(round(T['end'] * FPS))


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def io(t):
    t = clamp(t)
    return 4 * t ** 3 if t < .5 else 1 - (-2 * t + 2) ** 3 / 2


def o5(t):
    return 1 - (1 - clamp(t)) ** 5


def expo(t):
    t = clamp(t)
    return 1 if t >= 1 else 1 - 2 ** (-10 * t)


def af(d, i):
    return os.path.join(WORK, d, '%04d.jpg' % max(1, min(i, 298 if d.endswith('a') else 166)))


def source(t):
    """-> (path, kind) untuk masa output t."""
    if t < T['play1']:
        return af('v1a', 1), ('blur' if t < T['intro_end'] else 'sharp')
    if t < T['slow1']:
        return af('v1a', int(round((t - T['play1']) * 30)) + 1), 'sharp'
    if t < T['norm1']:
        src = 2.0 + (t - T['slow1']) * .5
        return af('v1s', int(round((src - 2.0) * 60)) + 1), 'sharp'
    if t < T['ch2']:
        return af('v1a', int(round((4.4 + t - T['norm1']) * 30)) + 1), 'sharp'
    if t < T['slow2']:
        return af('v2a', int(round((t - T['ch2']) * 30)) + 1), 'sharp'
    if t < T['norm2']:
        src = 2.2 + (t - T['slow2']) * .5
        return af('v2s', int(round((src - 2.2) * 60)) + 1), 'sharp'
    if t < T['outro']:
        return af('v2a', int(round((4.6 + t - T['norm2']) * 30)) + 1), 'sharp'
    return af('v2a', 298), 'sharp'


def punch(t, t0, amt, tau=.35):
    return 0 if t < t0 else amt * math.exp(-(t - t0) / tau)


def camera(t):
    """-> zoom (1 = penuh bingkai)."""
    P1, S1, N1, C2, S2, N2, O = T['play1'], T['slow1'], T['norm1'], T['ch2'], T['slow2'], T['norm2'], T['outro']
    if t < T['intro_end']:
        z = 1.18 - .08 * io(t / 3.0)
    elif t < P1:
        z = 1.0 + .05 * o5((t - 3.0) / (P1 - 3.0)) + .10 * (1 - expo((t - 3.0) / .5))
    elif t < S1:
        z = 1.05 - .05 * io((t - P1) / 1.6)
    elif t < N1:
        z = 1.0 + .08 * io((t - S1) / (N1 - S1))
    elif t < C2:
        z = 1.08 - .08 * io((t - N1) / 1.4) + .03 * io((t - N1 - 1.4) / 4.2)
    elif t < S2:
        z = 1.0 + .12 * (1 - expo((t - C2) / .55))
    elif t < N2:
        z = 1.0 + .08 * io((t - S2) / (N2 - S2))
    elif t < O:
        z = 1.08 - .08 * io((t - N2) / 1.4) + .03 * io((t - N2 - 1.4) / 4.0)
    else:
        z = 1.0 + .12 * io((t - O) / 3.5)
    z += punch(t, N1 + .05, .035) + punch(t, N2 + .05, .035)
    return z


def shake(t):
    amp = 0
    for a, b in ((T['slow1'] + .8, T['slow1'] + 2.0), (T['slow2'] + 1.2, T['slow2'] + 2.4)):
        if a <= t < b:
            amp = 7 * (1 - (t - a) / (b - a))
    if amp == 0:
        return 0, 0
    return amp * math.sin(t * 61.3) * math.cos(t * 23.7), amp * math.sin(t * 47.9 + 1.3)


def flash(t):
    f = 0
    for t0, peak, dec in ((3.0, 1.0, .32), (T['ch2'], 1.0, .32), (T['norm1'] + .05, .32, .3), (T['norm2'] + .05, .32, .3)):
        if t0 - .12 <= t < t0:
            f = max(f, peak * ((t - (t0 - .12)) / .12) ** 2)
        elif t >= t0:
            f = max(f, peak * math.exp(-(t - t0) / dec))
    return f


def zoomblur(t):
    for t0 in (3.0, T['ch2']):
        if t0 - .22 <= t < t0:
            return .10 * ((t - (t0 - .22)) / .22) ** 2
        if t0 <= t < t0 + .3:
            return .10 * (1 - (t - t0) / .3) ** 2
    return 0


_cache = {}


def load(path, kind):
    key = (path, kind)
    if key not in _cache:
        im = Image.open(path).convert('RGB')
        if kind == 'blur':
            im = im.filter(ImageFilter.GaussianBlur(14))
        if len(_cache) > 8:
            _cache.clear()
        _cache[key] = im
    return _cache[key]


def warp(im, z, dx=0, dy=0):
    s = 1280 / W  # 0.6667
    k = s / z
    return im.transform((W, H), Image.AFFINE, (k, 0, 640 - 960 * k + dx, 0, k, 360 - 540 * k + dy), Image.BICUBIC)


yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
_r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
VIGN = (1 - .32 * np.clip((_r - .55) / .85, 0, 1) ** 1.6)[..., None]
del yy, xx, _r


def frame(fi, ovdir):
    t = fi / FPS
    path, kind = source(t)
    im = load(path, kind)
    z = camera(t)
    sx, sy = shake(t)
    zb = zoomblur(t)
    if zb > 0:
        acc = None
        for j in range(7):
            w = np.asarray(warp(im, z * (1 + zb * j / 6), sx, sy), np.float32)
            acc = w if acc is None else acc + w
        a = acc / 7
    else:
        a = np.asarray(warp(im, z, sx, sy), np.float32)
    # gred: kontras + ketepuan ringan
    a = (a - 128) * 1.06 + 128
    lum = a.mean(axis=2, keepdims=True)
    a = lum + (a - lum) * 1.08
    if kind == 'blur':
        a *= .42
    if t >= T['outro']:
        d = io((t - T['outro']) / 1.2)
        a = a * (1 - .58 * d)
    a *= VIGN
    # aberasi kromatik semasa kilatan
    f = flash(t)
    ca = int(round(f * 10))
    if ca > 0:
        a[:, :, 0] = np.roll(a[:, :, 0], ca, axis=1)
        a[:, :, 2] = np.roll(a[:, :, 2], -ca, axis=1)
    if f > 0:
        a = a + (255 - a) * min(1, f) * .92
    a = np.clip(a, 0, 255).astype(np.uint8)
    img = Image.fromarray(a, 'RGB').convert('RGBA')
    ov = os.path.join(ovdir, '%05d.png' % fi)
    if os.path.exists(ov):
        img = Image.alpha_composite(img, Image.open(ov).convert('RGBA'))
    img = img.convert('RGB')
    # pudar masuk / keluar
    fade = min(clamp(t / .5), clamp((T['end'] - t) / .7))
    if fade < 1:
        img = Image.fromarray((np.asarray(img, np.float32) * fade).astype(np.uint8))
    return img


def main():
    mode = sys.argv[1]
    if mode == 'probe':
        os.makedirs('probe', exist_ok=True)
        for s in sys.argv[2:]:
            fi = int(round(float(s) * FPS))
            ovdir = 'ovprobe'
            os.makedirs(ovdir, exist_ok=True)
            src = os.path.join('probe', 'ov_%s.png' % s)
            if os.path.exists(src):
                os.replace(src, os.path.join(ovdir, '%05d.png' % fi))
            frame(fi, ovdir).save('probe/c_%s.jpg' % s, quality=90)
        return
    k, n = int(sys.argv[2]), int(sys.argv[3])
    a, b = NFRAMES * k // n, NFRAMES * (k + 1) // n
    os.makedirs('out', exist_ok=True)
    cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '%dx%d' % (W, H), '-r', str(FPS),
           '-i', '-', '-vf', 'scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv420p',
           '-c:v', 'libx264', '-preset', 'medium', '-crf', '12', '-color_range', 'tv', '-colorspace', 'bt709',
           '-color_primaries', 'bt709', '-color_trc', 'bt709', 'out/chunk_%d.mp4' % k]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for fi in range(a, b):
        p.stdin.write(frame(fi, 'ov').tobytes())
    p.stdin.close()
    p.wait()
    print('chunk', k, a, b, 'done')


if __name__ == '__main__':
    main()
