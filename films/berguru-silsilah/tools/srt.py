# Subtitle chunks from timeline.js -> out/berguru-silsilah.ms.srt
import json, re
TL = json.loads(re.search(r"window\.TL=(.*);", open("timeline.js").read()).group(1))
W, CH = TL["words"], TL["chunks"]
f = lambda s: "%02d:%02d:%02d,%03d" % (s // 3600, s % 3600 // 60, int(s % 60), round((s - int(s)) * 1000) % 1000)
out = []
for i, c in enumerate(CH):
    s = W[c["a"]]["s"] - .12
    nxt = W[CH[i + 1]["a"]]["s"] - .12 if i + 1 < len(CH) else 1e9
    e = min(nxt, W[c["b"]]["e"] + .7)
    out.append(f"{i + 1}\n{f(s)} --> {f(e)}\n{' '.join(W[j]['t'] for j in range(c['a'], c['b'] + 1))}\n")
open("out/berguru-silsilah.ms.srt", "w").write("\n".join(out))
print(len(out), "cues")
