"""Sediakan gambar kartun untuk film.html.

Guna:  python3 prepare.py <folder_png_asal>

Baca PNG berlatar telus (nama fail ikut format Humaira_Kartun_Tersusun),
kecilkan, tambah garis luar putih gaya pelekat dan bayang lembut,
kemudian tulis assets/img/NNN.png dan assets/manifest.json.
Umur diambil daripada nama fail sahaja (bukan dianggar daripada rupa).
"""
import json, os, re, sys
from PIL import Image, ImageFilter, ImageChops

SRC = sys.argv[1] if len(sys.argv) > 1 else 'input'
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'assets', 'img')
os.makedirs(OUT, exist_ok=True)
MAXD, OUTLINE, PAD = 900, 9, 44


# Pembetulan umur yang diberi pengguna (mengatasi label pada nama fail).
# Siri meniarap di pantai (baju merah jambu) sebenarnya 1 tahun 7 bulan.
AGE_OVERRIDES = [('Meniarap_Di_Pantai', '1 Tahun 7 Bulan', 19, 19)]
AGE_RE = r'(Baru_Lahir|Bawah_7_Bulan|\d+_Tahun_\d+_Bulan|\d+_Tahun|\d+_Bulan)_?'


def describe(name):
    """Keterangan pose/pakaian daripada nama fail, cth. 'Tidur Berbedung Biru'."""
    s = re.sub(r'\.png$', '', name)
    s = re.sub(r'^\d+\._?|^\d+_', '', s).replace('Humaira_', '')
    s = re.sub(AGE_RE, '', s)
    s = re.sub(r'_\d+$', '', s)
    return s.replace('_', ' ').strip()


def parse_age(name):
    """Pulangkan (label, bulan_min, bulan_max) daripada nama fail."""
    for key, label, a, b in AGE_OVERRIDES:
        if key in name:
            return label, a, b
    s = name.replace('_', ' ')
    if 'Baru Lahir' in s:
        return 'Baru Lahir', 0, 0
    if 'Bawah 7 Bulan' in s:
        return 'Bawah 7 Bulan', 0, 6.9
    m = re.search(r'(\d+) Tahun (\d+) Bulan', s)
    if m:
        y, mo = int(m.group(1)), int(m.group(2))
        return f'{y} Tahun {mo} Bulan', 12 * y + mo, 12 * y + mo
    m = re.search(r'(\d+) Tahun', s)
    if m:
        y = int(m.group(1))
        return f'{y} Tahun', 12 * y, 12 * y
    m = re.search(r'(\d+) Bulan', s)
    if m:
        mo = int(m.group(1))
        return f'{mo} Bulan', mo, mo
    return None, None, None


def sticker(im):
    im = im.convert('RGBA')
    bbox = im.getchannel('A').point(lambda a: 255 if a > 8 else 0).getbbox()
    if bbox:
        im = im.crop(bbox)
    k = MAXD / max(im.size)
    if k < 1:
        im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    W, H = im.width + 2 * PAD, im.height + 2 * PAD
    a = Image.new('L', (W, H), 0)
    a.paste(im.getchannel('A'), (PAD, PAD))
    # garis luar putih: kembangkan alfa, licinkan tepi
    ring = a.point(lambda v: 255 if v > 40 else 0).filter(ImageFilter.MaxFilter(2 * OUTLINE + 1))
    ring = ring.filter(ImageFilter.GaussianBlur(1.2))
    # bayang lembut di bawah
    sh = Image.new('L', (W, H), 0)
    sh.paste(ring, (0, 12))
    sh = sh.filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * 0.30))
    out = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    out.paste(Image.new('RGBA', (W, H), (70, 40, 60, 255)), (0, 0), sh)
    white = Image.new('RGBA', (W, H), (255, 255, 255, 255))
    out = Image.composite(white, out, ring)
    out.alpha_composite(im, (PAD, PAD))
    return out


items = []
files = sorted(f for f in os.listdir(SRC) if f.lower().endswith('.png') or re.fullmatch(r'\d+', f))
for f in files:
    num = re.match(r'(\d+)', f)
    if not num:
        continue
    n = int(num.group(1))
    label, a, b = parse_age(f)
    out_name = f'{n:03d}.png'
    dst = os.path.join(OUT, out_name)
    if os.path.exists(dst) and '--force' not in sys.argv:   # pelekat sudah ada: guna semula
        img = Image.open(dst)
    else:
        img = sticker(Image.open(os.path.join(SRC, f)))
        img.save(dst, optimize=True)
    items.append({'n': n, 'file': 'assets/img/' + out_name, 'w': img.width, 'h': img.height,
                  'age': label, 'm0': a, 'm1': b, 'desc': describe(f), 'src': f})
    print(out_name, img.size, label)

# susun ikut umur (gambar tanpa umur, iaitu keluarga, di akhir), kemudian nombor fail
items.sort(key=lambda i: (i['m1'] if i['m1'] is not None else 99, i['n']))
json.dump(items, open(os.path.join(HERE, 'assets', 'manifest.json'), 'w'), ensure_ascii=False, indent=1)
print('jumlah', len(items))
