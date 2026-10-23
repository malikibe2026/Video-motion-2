import math, io, json, urllib.request
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
SVC = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
def get(z, x, y):
    u = SVC.format(z=z, x=x, y=y)
    for _ in range(3):
        try:
            return urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=30).read()
        except Exception as e:
            err = e
    raise err
def build(name, z, x0, x1, y0, y1):
    nx, ny = x1 - x0 + 1, y1 - y0 + 1
    im = Image.new('RGB', (nx * 256, ny * 256))
    jobs = [(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)]
    with ThreadPoolExecutor(16) as ex:
        res = list(ex.map(lambda p: get(z, p[0], p[1]), jobs))
    for (x, y), d in zip(jobs, res):
        im.paste(Image.open(io.BytesIO(d)).convert('RGB'), ((x - x0) * 256, (y - y0) * 256))
    im.save(f'tex/{name}.jpg', quality=93)
    return dict(name=name, z=z, x0=x0, y0=y0, nx=nx, ny=ny, w=nx * 256, h=ny * 256)
meta = [build('z4', 4, 0, 15, 0, 15), build('z5', 5, 21, 28, 12, 17), build('z6', 6, 46, 54, 28, 34)]
json.dump(meta, open('tex/meta.json', 'w'))
print(meta)
