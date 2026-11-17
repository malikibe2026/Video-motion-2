# Buang latar belakang video Humaira.
#   python matte.py track  <video> <models_dir> <out_dir>   -> wajah setiap bingkai, transform.json
#   python matte.py matte  <video> <models_dir> <out_dir> f0 f1  -> fg_k.mp4 (warna) + al_k.mp4 (alfa)
import sys, json, subprocess, numpy as np, cv2, os
import mediapipe as mp
from mediapipe.tasks import python as mpp
from mediapipe.tasks.python import vision
mode, VID, MD, OUT = sys.argv[1:5]
W, H, FPS = 1080, 1920, 30
os.makedirs(OUT, exist_ok=True)
def reader(scale=1, start=0, n=None):
    w, h = W // scale, H // scale
    cmd = ['ffmpeg', '-loglevel', 'error', '-ss', f'{start / FPS:.4f}', '-i', VID, '-vf', f'scale={w}:{h}', '-f', 'rawvideo', '-pix_fmt', 'rgb24']
    if n: cmd += ['-frames:v', str(n)]
    p = subprocess.Popen(cmd + ['-'], stdout=subprocess.PIPE, bufsize=10 ** 8)
    while True:
        b = p.stdout.read(w * h * 3)
        if len(b) < w * h * 3: break
        yield np.frombuffer(b, np.uint8).reshape(h, w, 3)
if mode == 'track':
    fd = vision.FaceDetector.create_from_options(vision.FaceDetectorOptions(base_options=mpp.BaseOptions(model_asset_path=f'{MD}/face_short.tflite'), min_detection_confidence=.4))
    seg = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(base_options=mpp.BaseOptions(model_asset_path=f'{MD}/selfie_multiclass.tflite'), output_confidence_masks=True))
    rows = []
    for i, fr in enumerate(reader(2)):
        img = mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(fr))
        dets = fd.detect(img).detections
        face = None
        if dets:
            b = max(dets, key=lambda d: d.bounding_box.width).bounding_box
            face = [2 * (b.origin_x + b.width / 2), 2 * (b.origin_y + b.height / 2), 2 * b.width]
        # pusat jisim kanak-kanak dari mask rambut+kulit muka (kelas 1,3)
        cm = seg.segment(img).confidence_masks
        hf = np.squeeze(cm[1].numpy_view()) + np.squeeze(cm[3].numpy_view()); mh, mw = hf.shape
        ys, xs = np.nonzero(hf > .5)
        head = [float(xs.mean() / mw * W), float(ys.min() / mh * H), float(np.percentile(ys, 90) / mh * H)] if len(xs) > 50 else None
        rows.append({'f': i, 'face': face, 'head': head})
    json.dump(rows, open(f'{OUT}/track.json', 'w'))
    # transformasi licin: kepala Humaira ke (540, 640), lebar muka -> 235 px
    n = len(rows); cx = np.full(n, np.nan); cy = np.full(n, np.nan); fw = np.full(n, np.nan)
    for r in rows:
        if r['face']: cx[r['f']], cy[r['f']], fw[r['f']] = r['face']
        elif r['head']: cx[r['f']] = r['head'][0]; cy[r['f']] = (r['head'][1] + r['head'][2]) / 2
    def fill(a):
        idx = np.arange(len(a)); ok = ~np.isnan(a)
        return np.interp(idx, idx[ok], a[ok]) if ok.any() else a
    cx, cy, fw = fill(cx), fill(cy), fill(fw)
    med = np.nanmedian(fw)
    fw = np.clip(fw, med * .75, med * 1.3)
    def smooth(a, k):
        a = np.pad(a, k, mode='edge'); w = np.hanning(2 * k + 1); w /= w.sum(); return np.convolve(a, w, 'valid')
    cx, cy, fw = smooth(cx, 25), smooth(cy, 25), smooth(fw, 60)
    s = np.clip(235 / fw, .6, 1.4)
    T = [{'cx': float(cx[i]), 'cy': float(cy[i]), 's': float(s[i])} for i in range(n)]
    json.dump(T, open(f'{OUT}/transform.json', 'w'))
    print('frames', n, 'faces', sum(1 for r in rows if r['face']), 'median face w', med)
else:
    f0, f1 = int(sys.argv[5]), int(sys.argv[6])
    T = json.load(open(f'{OUT}/transform.json')); rows = json.load(open(f'{OUT}/track.json'))
    seg = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(base_options=mpp.BaseOptions(model_asset_path=f'{MD}/selfie_multiclass.tflite'), output_confidence_masks=True))
    enc = lambda name, fmt: subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', fmt, '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                                              '-c:v', 'libx264', '-preset', 'fast', '-crf', '12', '-pix_fmt', 'yuv444p' if fmt == 'rgb24' else 'yuv420p', f'{OUT}/{name}'], stdin=subprocess.PIPE)
    pc, pa = enc(f'fg_{f0}.mp4', 'rgb24'), enc(f'al_{f0}.mp4', 'gray')
    warm = min(f0, 10); prev = None
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    for j, fr in enumerate(reader(1, f0 - warm, f1 - f0 + warm)):
        i = f0 - warm + j
        bgr = cv2.cvtColor(fr, cv2.COLOR_RGB2BGR)
        cm = seg.segment(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(fr))).confidence_masks
        a = 1 - np.squeeze(cm[0].numpy_view())
        a = cv2.resize(a, (W, H), interpolation=cv2.INTER_LINEAR)
        prev = a if prev is None else .65 * a + .35 * prev   # licin masa, kurang berkelip
        a = cv2.ximgproc.guidedFilter(bgr, (prev * 255).astype(np.uint8), 10, 1e-2 * 255 * 255).astype(np.float32) / 255
        a = np.clip((a - .35) / .3, 0, 1)
        # buang cadar hijau
        hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
        green = ((hsv[..., 0] > 32) & (hsv[..., 0] < 85) & (hsv[..., 1] > 45)).astype(np.float32)
        green = cv2.GaussianBlur(green, (9, 9), 0); a *= 1 - green
        # hanya kawasan badan Humaira (buang tangan/kaki orang dewasa, selimut, bantal)
        t = T[i]; fw = 235 / t['s']; cx, cy = t['cx'], t['cy']
        hip = cy + 2.4 * fw
        half = np.where(yy < hip, 1.7 * fw, 1.85 * fw)
        dx = np.abs(xx - cx) / half
        dy = np.where(yy < cy, (cy - yy) / (1.7 * fw), 0)
        reg = np.clip((1.15 - np.maximum(dx, dy)) / .15, 0, 1)
        LB = float(os.environ.get('LEFTBAND', '.07')); reg *= np.clip((xx - W * LB) / (W * .03), 0, 1)          # jalur tepi kiri: tangan masuk dari situ
        a *= reg
        # 'pakaian' di luar lebar badan, di atas pinggang = selimut/bantal
        cf = lambda k: cv2.resize(np.squeeze(cm[k].numpy_view()), (W // 4, H // 4))
        hair, skin = cf(1), cf(2) + cf(3)
        up = lambda z: cv2.resize(z, (W, H), interpolation=cv2.INTER_LINEAR)
        side = np.clip((np.abs(xx - cx) - .95 * fw) / (.15 * fw), 0, 1) * np.clip((hip - .3 * fw - yy) / (.3 * fw), 0, 1)
        a *= 1 - np.clip(1 - up(np.clip(skin + hair, 0, 1)) * 1.3, 0, 1) * side          # di sisi atas: hanya kulit/rambut
        above = np.clip((cy - .75 * fw - yy) / (.15 * fw), 0, 1)
        a *= 1 - np.clip(1 - up(hair) * 1.3, 0, 1) * above                               # di atas kepala: hanya rambut
        # kulit gelap (tangan dewasa) di sebelah kiri badan
        V = hsv[..., 2].astype(np.float32); Sx = hsv[..., 1].astype(np.float32)
        dark = np.clip((158 - V) / 22, 0, 1) * np.clip((Sx - 40) / 30, 0, 1)
        leftz = np.clip((cx - 1.1 * fw - xx) / (.2 * fw), 0, 1)
        a *= 1 - cv2.GaussianBlur(dark * leftz, (15, 15), 0)
        m = (a > .5).astype(np.uint8)
        er = cv2.erode(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (19, 19)))
        nlab, lab, st, _ = cv2.connectedComponentsWithStats(er)
        if nlab > 1:
            px, py = int(np.clip(cx, 0, W - 1)), int(np.clip(cy + .9 * fw, 0, H - 1))
            k = lab[py, px]
            if k == 0:
                k2 = lab[int(np.clip(cy, 0, H - 1)), px]; k = k2 if k2 > 0 else 1 + np.argmax(st[1:, cv2.CC_STAT_AREA])
            keep = cv2.dilate((lab == k).astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31))).astype(np.float32)
            a *= cv2.GaussianBlur(keep, (9, 9), 0)
        # transform ke kanvas: kepala ke (540,700)
        s = t['s']; Mx = np.float32([[s, 0, 540 - s * t['cx']], [0, s, 640 - s * t['cy']]])
        rgb2 = cv2.warpAffine(fr, Mx, (W, H), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0))
        a2 = cv2.warpAffine(a, Mx, (W, H), flags=cv2.INTER_LINEAR, borderValue=0)
        # pelekat: garis putih + bayang
        hard = (a2 > .4).astype(np.uint8)
        out = cv2.dilate(hard, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (27, 27))).astype(np.float32)
        out = cv2.GaussianBlur(out, (7, 7), 0)
        sh = cv2.GaussianBlur(np.roll(np.roll(out, 14, 0), 6, 1), (41, 41), 0) * .35
        col = np.zeros((H, W, 3), np.float32); al = np.zeros((H, W), np.float32)
        for c, aa in ((np.array([60, 20, 70], np.float32), sh), (np.array([255, 255, 255], np.float32), out)):
            na = aa + al * (1 - aa); col = (c * aa[..., None] + col * (al * (1 - aa))[..., None]) / np.maximum(na, 1e-4)[..., None]; al = na
        aa = a2; na = aa + al * (1 - aa)
        col = (rgb2.astype(np.float32) * aa[..., None] + col * (al * (1 - aa))[..., None]) / np.maximum(na, 1e-4)[..., None]; al = na
        if j < warm: continue
        pc.stdin.write(np.clip(col, 0, 255).astype(np.uint8).tobytes()); pa.stdin.write((al * 255).astype(np.uint8).tobytes())
        if (i - f0) % 300 == 0: print(f0, i, flush=True)
    pc.stdin.close(); pa.stdin.close(); pc.wait(); pa.wait(); print('done', f0, f1)
