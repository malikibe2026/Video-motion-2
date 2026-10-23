import json, os, urllib.request
from concurrent.futures import ThreadPoolExecutor
SVC = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
need = json.load(open('needed3.json'))
def one(k):
    z, x, y = k.split('/')
    p = f'tiles/{z}/{y}/{x}.jpg'
    if os.path.exists(p) and os.path.getsize(p) > 0: return 0
    os.makedirs(os.path.dirname(p), exist_ok=True)
    for _ in range(4):
        try:
            d = urllib.request.urlopen(urllib.request.Request(SVC.format(z=z, x=x, y=y), headers={'User-Agent': 'Mozilla/5.0'}), timeout=30).read()
            open(p, 'wb').write(d); return 0
        except Exception: pass
    return 1
with ThreadPoolExecutor(24) as ex: fails = sum(ex.map(one, need))
print('tiles', len(need), 'failed', fails)
