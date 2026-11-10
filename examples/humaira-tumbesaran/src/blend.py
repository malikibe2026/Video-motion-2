"""Gabung subbingkai motion blur: purata <out>_sub/fNNNNN_j.png -> <out>/fNNNNN.png
Guna: python3 blend.py fr3"""
import glob, os, sys
import numpy as np
from PIL import Image
out = sys.argv[1]; groups = {}
for p in glob.glob(os.path.join(out + '_sub', '*.png')):
    groups.setdefault(os.path.basename(p).rsplit('_', 1)[0], []).append(p)
for name, ps in sorted(groups.items()):
    acc = sum(np.asarray(Image.open(p).convert('RGB'), np.float32) for p in ps) / len(ps)
    Image.fromarray((acc + .5).astype(np.uint8)).save(os.path.join(out, name + '.png'), compress_level=1)
print('digabung', len(groups))
