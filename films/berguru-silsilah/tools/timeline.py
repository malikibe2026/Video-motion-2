# Word timings -> subtitle chunks + scene cue times, written to timeline.js (times in film seconds).
import json, re
LEAD = 0.6   # narration starts 0.6 s into the film
TAIL = 3.2
W = [w for w in json.load(open("audio/words2.json"))["words"] if w["type"] == "word" and not w["text"].startswith("[")]
words = [{"t": re.sub(r'["]', "", w["text"]).replace("...", "…"), "s": round(w["start"] + LEAD, 3), "e": round(w["end"] + LEAD, 3)} for w in W]
# fix display spellings
for w in words:
    if w["t"].lower().startswith("magic"): w["t"] = w["t"].replace("magic", "“magic”")
    if w["t"] == "mufti": w["t"] = "“mufti"
    if w["t"] == "plastik": w["t"] = "plastik”"

chunks, cur = [], []
def flush():
    global cur
    if cur: chunks.append(cur); cur = []
for i, w in enumerate(words):
    cur.append(i)
    txt = " ".join(words[j]["t"] for j in cur)
    end_sent = re.search(r"[.?!:…]$", w["t"])
    comma = w["t"].endswith(",")
    nxt_gap = words[i + 1]["s"] - w["e"] if i + 1 < len(words) else 9
    open_quote = w["t"].startswith("“") and not w["t"].endswith("”")
    nxt = words[i + 1]["t"] if i + 1 < len(words) else ""
    nxt_ends = bool(re.search(r"[.?!:…,]$", nxt)) and len(txt) + len(nxt) <= 46
    if open_quote and not end_sent: continue
    if end_sent or (comma and len(cur) >= 3) or (len(txt) >= 34 and not nxt_ends) or (nxt_gap > 0.35 and len(cur) >= 2):
        flush()
flush()
# merge tiny trailing chunks (1 word) into previous when same sentence
out = []
for c in chunks:
    if out and len(c) == 1 and not re.search(r"[.?!:…]$", words[out[-1][-1]]["t"]) and len(" ".join(words[j]["t"] for j in out[-1] + c)) <= 46:
        out[-1] += c
    else:
        out.append(c)
CH = [{"a": c[0], "b": c[-1]} for c in out]

def at(phrase, after=0):
    toks = phrase.lower().split()
    for i in range(len(words)):
        if words[i]["s"] < after: continue
        if all(re.sub(r"[^\w-]", "", words[i + k]["t"].lower()) == t for k, t in enumerate(toks) if i + k < len(words)):
            return words[i]["s"]
    raise SystemExit("cue not found: " + phrase)

C = {}
C["hook"] = at("ilmu agama")
C["tapi"] = at("tapi")
C["inilah"] = at("inilah")
C["s1"] = at("pertama")
C["membaca"] = at("membaca kitab")
C["murakkab"] = at("jahil murakkab")
C["jahil2"] = at("jahil", C["murakkab"] + 1)
C["mutasy"] = at("mutasyabihat")
C["s1b"] = at("kedua")
C["tiktok"] = at("tiktok")
C["mufti"] = at("mufti")
C["s1c"] = at("ketiga")
C["mimpi"] = at("mimpi")
C["magic"] = at("magic")
C["tipu"] = at("tipu daya")
C["s2"] = at("jadi")
C["berguru"] = at("berguru dengan guru")
C["silsilah"] = at("silsilah ialah")
C["gurukepada"] = at("guru kepada guru")
C["rasul"] = at("rasulullah")
C["sah"] = at("guru yang sah")
C["s2b"] = at("di dalam hati")
C["nur"] = at("nur nubuwah")
C["cahaya"] = at("cahaya kenabian")
C["bukan"] = at("ia bukan")
C["kurnia"] = at("kurniaan allah")
C["s2c"] = at("guru yang benar juga")
C["syariat"] = at("syariat")
C["tarekat"] = at("tarekat")
C["bersih"] = at("membersihkan hati")
C["s3"] = at("namun")
C["kunci"] = at("kuncinya")
C["ikhlas"] = at("keikhlasan")
C["ihdinas"] = at("ihdinas")
C["tunjuk"] = at("tunjukilah")
C["doa"] = at("doa ini")
C["s3b"] = at("sesiapa")
C["mursyid"] = at("mursyid")
C["s3c"] = at("tetapi jika")
C["nafsu"] = at("nafsu")
C["palsu"] = at("guru palsu")
C["s4"] = at("maka")
C["niat"] = at("betulkan niat")
C["carilah"] = at("carilah")
C["semoga"] = at("semoga")
C["voend"] = words[-1]["e"]
C["end"] = round(words[-1]["e"] + TAIL, 2)
open("timeline.js", "w").write("window.TL=" + json.dumps({"lead": LEAD, "words": words, "chunks": CH, "cue": C}, ensure_ascii=False) + ";\n")
for c in CH: print(round(words[c["a"]]["s"], 2), " ".join(words[j]["t"] for j in range(c["a"], c["b"] + 1)))
print(C)
