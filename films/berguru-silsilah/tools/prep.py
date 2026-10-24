# Upscale crops 2.5x (Lanczos + light unsharp) and record each crop's edge colour for its medallion fill.
import json, glob, os
from PIL import Image, ImageFilter
import numpy as np
meta = {}
for f in sorted(glob.glob("assets/*.png")):
    k = os.path.basename(f)[:-4]
    if k == "source" or k.endswith("@2x"): continue
    im = Image.open(f).convert("RGB")
    a = np.asarray(im).astype(float)
    edge = np.concatenate([a[:4].reshape(-1, 3), a[-4:].reshape(-1, 3), a[:, :4].reshape(-1, 3), a[:, -4:].reshape(-1, 3)])
    c = np.median(edge, axis=0).astype(int)
    big = im.resize((round(im.width * 2.5), round(im.height * 2.5)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 60, 2))
    big.save(f"assets/{k}@2x.png")
    meta[k] = {"w": big.width, "h": big.height, "edge": "#%02x%02x%02x" % tuple(c)}
json.dump(meta, open("assets/meta.json", "w"), indent=1)
print(json.dumps(meta))
