"""Gabung video Borak + Makan (wajah ditukar) dengan kad tajuk, peralihan dan sari kata.
python3 compose.py probe t1 t2 ... | python3 compose.py chunk k n"""
import sys, os, math, subprocess
import numpy as np
from PIL import Image, ImageFilter
FPS, W, H = 24, 1920, 1080
WORK = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'work')
T = dict(B0=3.2, INT=13.2, M0=15.0, END=25.0, FIN=28.8)
NF = int(round(T['FIN'] * FPS))
clamp = lambda x, a=0., b=1.: max(a, min(b, x))
def io(t):
    t = clamp(t); return 4 * t ** 3 if t < .5 else 1 - (-2 * t + 2) ** 3 / 2
def fr(d, i): return os.path.join(WORK, d, '%04d.png' % max(1, min(240, i)))
_c = {}
def img(p, blur=0):
    k = (p, blur)
    if k not in _c:
        if len(_c) > 10: _c.clear()
        im = Image.open(p).convert('RGB')
        if blur: im = im.filter(ImageFilter.GaussianBlur(blur))
        _c[k] = im
    return _c[k]
def warp(im, z):
    k = (1280 / W) / z
    return np.asarray(im.transform((W, H), Image.AFFINE, (k, 0, 640 - 960 * k, 0, k, 360 - 540 * k), Image.BICUBIC), np.float32)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
_r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
VIG = (1 - .28 * np.clip((_r - .55) / .85, 0, 1) ** 1.6)[..., None]; del yy, xx, _r
def layer(t):
    """-> (array, darken) satu lapisan; peralihan = campuran dua lapisan."""
    B0, INT, M0, END = T['B0'], T['INT'], T['M0'], T['END']
    if t < B0:   # tajuk: latar kabur hidangan
        return warp(img(fr('makan_swap', 150), 16), 1.12 - .05 * io(t / B0)), .5
    if t < INT:
        k = t - B0; return warp(img(fr('borak_raw', int(k * FPS) + 1)), 1.0 + .04 * io(k / 10)), 0
    if t < M0:
        return warp(img(fr('makan_swap', 1), 16), 1.10 - .04 * io((t - INT) / 1.8)), .5
    if t < END:
        k = t - M0; return warp(img(fr('makan_swap', int(k * FPS) + 1)), 1.0 + .04 * io(k / 10)), 0
    k = t - END; d = io(k / 1.4)
    return warp(img(fr('makan_swap', 240), int(round(d * 14))), 1.04 + .05 * io(k / 3.8)), .5 * d
def base(t):
    a, d = layer(t)
    a = a * (1 - d)
    # lebur silang pada setiap sempadan (0.5 s)
    for tb in (T['B0'], T['INT'], T['M0'], T['END']):
        if tb <= t < tb + .5 and tb != T['END']:
            b, d2 = layer(tb - 1e-3 if tb != T['B0'] else tb - 1e-3)
            w = 1 - io((t - tb) / .5); a = a * (1 - w) + b * (1 - d2) * w
    # gred hangat ringan
    a = (a - 128) * 1.04 + 128; a[..., 0] *= 1.02; a[..., 2] *= .97
    return a * VIG
def frame(fi, ovdir):
    t = fi / FPS; a = base(t)
    fade = min(clamp(t / .6), clamp((T['FIN'] - t) / .9)); a *= fade
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert('RGBA')
    ov = os.path.join(ovdir, '%05d.png' % fi)
    if os.path.exists(ov):
        o = Image.open(ov).convert('RGBA')
        if fade < 1: o.putalpha(o.getchannel('A').point(lambda v: int(v * fade)))
        im = Image.alpha_composite(im, o)
    return im.convert('RGB')
if __name__ == '__main__':
    os.chdir(WORK)
    if sys.argv[1] == 'probe':
        os.makedirs('probe', exist_ok=True)
        for s in sys.argv[2:]:
            fi = int(round(float(s) * FPS)); frame(fi, 'ov').save('probe/c_%s.jpg' % s, quality=90)
    else:
        k, n = int(sys.argv[2]), int(sys.argv[3]); a, b = NF * k // n, NF * (k + 1) // n
        os.makedirs('out', exist_ok=True)
        p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1920x1080', '-r', str(FPS), '-i', '-',
                              '-vf', 'scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv420p', '-c:v', 'libx264', '-crf', '14',
                              '-color_range', 'tv', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', 'out/chunk_%d.mp4' % k], stdin=subprocess.PIPE)
        for fi in range(a, b): p.stdin.write(frame(fi, 'ov').tobytes())
        p.stdin.close(); p.wait(); print('chunk', k, 'done')
