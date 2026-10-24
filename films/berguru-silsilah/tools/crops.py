# Crop the infographic's illustrations (display coords x 1.376 = source px) and build a contact sheet.
import sys, json
from PIL import Image, ImageDraw
root = sys.argv[1]
S = 1536 / 1116
im = Image.open(f"{root}/assets/source.png").convert("RGB")
boxes = {
  "book":     (58, 370, 285, 575),
  "phone":    (636, 352, 765, 585),
  "magic":    (185, 595, 490, 735),
  "dreamer":  (185, 595, 360, 735),
  "magician": (355, 595, 490, 735),
  "scholars": (55, 1010, 305, 1230),
  "lantern":  (490, 1020, 630, 1215),
  "pillars":  (868, 1070, 948, 1262),
  "heart":    (965, 1105, 1052, 1185),
  "compass":  (128, 1398, 240, 1528),
  "pray":     (70, 1680, 245, 1945),
  "guide":    (270, 1655, 400, 1895),
  "king":     (930, 1665, 1075, 1845),
  "darkman":  (785, 1790, 935, 1968),
}
out = {}
tiles = []
for k, b in boxes.items():
    sb = tuple(round(v * S) for v in b)
    c = im.crop(sb); c.save(f"{root}/assets/{k}.png"); out[k] = c.size
    tiles.append((k, c))
W = 1800; x = y = 0; rowh = 0
sheet = Image.new("RGB", (W, 1400), "white"); d = ImageDraw.Draw(sheet)
for k, c in tiles:
    if x + c.width > W: x = 0; y += rowh + 30; rowh = 0
    sheet.paste(c, (x, y + 20)); d.text((x + 4, y + 2), k, fill="red")
    x += c.width + 10; rowh = max(rowh, c.height)
sheet.crop((0, 0, W, y + rowh + 30)).save(f"{root}/probe_crops.png")
print(json.dumps(out))
