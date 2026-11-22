"""Tukar wajah Tok Ma (video Makan) kepada wajah dalam work/sumber_wajah.png. Jejak ikut embedding + kedudukan."""
import cv2, numpy as np, os, subprocess, insightface
from insightface.app import FaceAnalysis
W = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'work'); os.chdir(W)
app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider']); app.prepare(ctx_id=-1, det_size=(640, 640), det_thresh=0.3)
sw = insightface.model_zoo.get_model('/root/.insightface/models/inswapper_128.onnx', providers=['CPUExecutionProvider'])
src = cv2.imread('sumber_wajah.png', cv2.IMREAD_UNCHANGED)
if src.shape[2] == 4:
    a = src[:, :, 3:] / 255.; src = (src[:, :, :3] * a + 255 * (1 - a)).astype('uint8')
SF = app.get(src)[0]
os.makedirs('makan_raw', exist_ok=True); os.makedirs('makan_swap', exist_ok=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'makan.mp4', '-q:v', '1', '-qmin', '1', 'makan_raw/%04d.png'], check=True)
files = sorted(os.listdir('makan_raw'))
ref = None; last = None; miss = []
for k, fn in enumerate(files):
    img = cv2.imread('makan_raw/' + fn); faces = app.get(img)
    if ref is None:  # bingkai pertama: wajah paling tua = Tok Ma
        tok = max(faces, key=lambda f: f.age); ref = tok.normed_embedding
    else:
        best, bs = None, -9
        for f in faces:
            c = (f.bbox[:2] + f.bbox[2:]) / 2
            s = float(np.dot(f.normed_embedding, ref)) - (np.linalg.norm(c - last) / 600 if last is not None else 0)
            if s > bs: best, bs = f, s
        tok = best if best is not None and bs > 0.15 else None
    if tok is None:
        miss.append(k); out = img
    else:
        last = (tok.bbox[:2] + tok.bbox[2:]) / 2
        out = sw.get(img, tok, SF, paste_back=True)
    cv2.imwrite('makan_swap/' + fn, out)
print('frames', len(files), 'miss', miss)
