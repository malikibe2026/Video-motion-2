"""Narration (take 2) + soft synthesized SFX on the scene cues, two-pass loudnorm to -14 LUFS -> out/audio.wav"""
import json, re, subprocess, os
import numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__))
SR = 48000
TL = json.loads(re.search(r"window\.TL=(.*);", open(f"{ROOT}/timeline.js").read()).group(1))
C, LEAD, END = TL["cue"], TL["lead"], TL["cue"]["end"]
rng = np.random.default_rng(7)

subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{ROOT}/audio/take2.mp3", "-ac", "1", "-ar", str(SR), "-f", "f32le", f"{ROOT}/audio/vo.f32"], check=True)
vo = np.fromfile(f"{ROOT}/audio/vo.f32", dtype=np.float32)
n = int(END * SR) + SR
mix = np.zeros(n, np.float32)
a = int(LEAD * SR)
mix[a:a + len(vo)] += vo[: n - a]
# a copy at film timing for the HTML preview
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", f"{ROOT}/audio/narration.wav"], input=mix.tobytes(), check=True)


def env(length, attack, decay):
    t = np.arange(length) / SR
    return np.minimum(1, t / attack) * np.exp(-t / decay)


def whoosh(dur=0.7):
    m = int(dur * SR)
    x = rng.standard_normal(m).astype(np.float32)
    # one-pole low-pass sweeping up then down
    y = np.zeros(m, np.float32); s = 0.0
    cut = np.sin(np.linspace(0, np.pi, m)) * 0.25 + 0.02
    for i in range(m):
        s += cut[i] * (x[i] - s); y[i] = s
    return y * np.sin(np.linspace(0, np.pi, m)) ** 2 * 1.4


def chime(f0=880.0, dur=2.2):
    m = int(dur * SR); t = np.arange(m) / SR
    y = sum(g * np.sin(2 * np.pi * f0 * r * t) * np.exp(-t / (dur * d)) for r, g, d in [(1, 1, .45), (2.01, .45, .25), (3.02, .22, .15), (4.2, .1, .08)])
    return (y * np.minimum(1, t / 0.004)).astype(np.float32)


def thump(dur=0.28):
    m = int(dur * SR); t = np.arange(m) / SR
    f = 140 * np.exp(-t / 0.08) + 55
    ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) * env(m, 0.003, 0.09)).astype(np.float32)


def tick(dur=0.06):
    m = int(dur * SR); t = np.arange(m) / SR
    return (np.sin(2 * np.pi * 1900 * t) * env(m, 0.001, 0.012)).astype(np.float32)


def place(sig, at, gain):
    i = int(at * SR)
    j = min(n, i + len(sig))
    if i < n:
        mix[i:j] += sig[: j - i] * gain


for k, g in [("s1", .10), ("s1b", .07), ("s1c", .07), ("s2", .13), ("s3", .13), ("s4", .09)]:
    place(whoosh(), C[k] - 0.45, g)
for k, f, g in [("inilah", 784, .045), ("rasul", 988, .04), ("nur", 1175, .05), ("ikhlas", 880, .045), ("semoga", 784, .045)]:
    place(chime(f), C[k], g)
for k in ["mufti", "tipu", "palsu"]:
    place(thump(), C[k] + 0.02, .35)
place(tick(), C["tapi"], .12)
place(tick(), C["mursyid"], .08)

fade = int(1.0 * SR)
mix[-fade:] *= np.linspace(1, 0, fade)
mix = mix[: int(END * SR)]
raw = f"{ROOT}/audio/mix.f32"
mix.astype(np.float32).tofile(raw)
inp = ["-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", raw]
r = subprocess.run(["ffmpeg", "-hide_banner"] + inp + ["-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True)
m = json.loads(r.stderr[r.stderr.rindex("{"):])
af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
      f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
os.makedirs(f"{ROOT}/out", exist_ok=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + inp + ["-af", af, "-ar", str(SR), "-ac", "2", f"{ROOT}/out/audio.wav"], check=True)
print("audio ->", f"{ROOT}/out/audio.wav", "input", m["input_i"], "LUFS")
