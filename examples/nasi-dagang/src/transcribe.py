"""Transkripsi audio asal (Whisper turbo via sherpa-onnx, luar talian), dipecah ikut jeda senyap."""
import sys, subprocess, json, numpy as np, sherpa_onnx
M = '/root/asr/sherpa-onnx-whisper-turbo/turbo-'
rec = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=M + 'encoder.int8.onnx', decoder=M + 'decoder.int8.onnx',
                                                 tokens=M + 'tokens.txt', language='ms', task='transcribe', num_threads=4)
SR = 16000
def load(p):
    b = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
    return np.frombuffer(b, np.float32)
def asr(x):
    s = rec.create_stream(); s.accept_waveform(SR, x); rec.decode_stream(s); return s.result.text.strip()
out = {}
for p in sys.argv[1:]:
    x = load(p)
    # tenaga per 20 ms -> segmen bercakap
    hop = 320; e = np.array([np.sqrt(np.mean(x[i:i + hop] ** 2)) for i in range(0, len(x) - hop, hop)])
    th = max(0.01, np.percentile(e, 30) * 2.2); on = e > th
    segs = []; i = 0
    while i < len(on):
        if on[i]:
            j = i
            while j < len(on) and (on[j] or (on[j:j + 18].any())): j += 1  # rapatkan jeda < 0.36 s
            if j - i > 10: segs.append((i * hop / SR, j * hop / SR))
            i = j
        else: i += 1
    full = asr(x)
    res = []
    for a, b in segs:
        a2, b2 = max(0, a - .08), min(len(x) / SR, b + .1)
        res.append({'start': round(a2, 2), 'end': round(b2, 2), 'text': asr(x[int(a2 * SR):int(b2 * SR)])})
    out[p] = {'full': full, 'segments': res}
    print('==', p); print('FULL:', full)
    for r in res: print('  %5.2f-%5.2f  %s' % (r['start'], r['end'], r['text']))
json.dump(out, open('transcript.json', 'w'), ensure_ascii=False, indent=1)
