import sys, numpy as np, cv2, mediapipe as mp
from mediapipe.tasks import python as mpp
from mediapipe.tasks.python import vision
M = sys.argv[1]; files = sys.argv[2:]
seg = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(base_options=mpp.BaseOptions(model_asset_path=M), output_confidence_masks=True, output_category_mask=False))
tiles = []
for f in files:
    bgr = cv2.imread(f); rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    res = seg.segment(mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb))
    cm = res.confidence_masks
    bg = cm[0].numpy_view()
    a = 1 - bg
    a = cv2.resize(a, (rgb.shape[1], rgb.shape[0]), interpolation=cv2.INTER_LINEAR)
    # guided filter refine
    a = cv2.ximgproc.guidedFilter(bgr, (a * 255).astype(np.uint8), 8, 1e-2 * 255 * 255).astype(np.float32) / 255
    a = np.clip((a - .35) / .3, 0, 1)
    m = (a > .5).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    if n > 1:
        k = 1 + np.argmax(st[1:, cv2.CC_STAT_AREA]); keep = (lab == k).astype(np.uint8)
        keep = cv2.dilate(keep, np.ones((25, 25), np.uint8)); a = a * keep
    out = np.zeros_like(bgr); out[:] = (180, 120, 255)
    comp = (bgr * a[..., None] + out * (1 - a[..., None])).astype(np.uint8)
    tiles.append(cv2.resize(comp, (270, 480)))
cv2.imwrite('seg_sheet.png', np.hstack(tiles))
