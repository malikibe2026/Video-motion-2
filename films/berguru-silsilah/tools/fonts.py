# Download Google Fonts (latin + arabic subsets) as local woff2 and write fonts/fonts.css.
import re, urllib.request, sys, os
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
fams = ["DM+Serif+Display:ital@0;1", "Plus+Jakarta+Sans:wght@400;500;600;700;800", "Amiri:wght@400;700"]
url = "https://fonts.googleapis.com/css2?" + "&".join("family=" + f for f in fams) + "&display=block"
css = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA})).read().decode()
out = []
blocks = re.findall(r"/\* ([\w-]+) \*/\s*(@font-face \{.*?\})", css, re.S)
for subset, block in blocks:
    if subset not in ("latin", "latin-ext", "arabic"): continue
    src = re.search(r"url\((https://[^)]+)\)", block).group(1)
    fam = re.search(r"font-family: '([^']+)'", block).group(1).replace(" ", "")
    w = re.search(r"font-weight: (\d+)", block).group(1)
    st = re.search(r"font-style: (\w+)", block).group(1)
    name = f"{fam}-{w}-{st}-{subset}.woff2"
    if not os.path.exists(f"fonts/{name}"):
        urllib.request.urlretrieve(src, f"fonts/{name}")
    out.append(block.replace(src, name))
open("fonts/fonts.css", "w").write("\n".join(out))
print(len(out), "faces")
