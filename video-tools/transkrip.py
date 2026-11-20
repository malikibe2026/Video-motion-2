"""Transkrip audio/video dengan Whisper (faster-whisper) -> SRT + JSON masa setiap perkataan.

Guna:
    python3 scripts/transkrip.py VIDEO_ATAU_AUDIO [--model small] [--bahasa ms] [--keluar FOLDER]

Hasil (dalam --keluar, lalai: folder yang sama dengan input):
    <nama>.srt         caption biasa, sedia untuk FFmpeg (subtitles=) atau editor video
    <nama>.words.json  setiap perkataan dengan masa mula/tamat, untuk caption beranimasi
                       (HyperFrames / Remotion)

Model: tiny / base / small / medium / large-v3. Lebih besar = lebih tepat tetapi lebih lambat.
Model dimuat turun dari huggingface.co pada kali pertama sahaja.
"""
import argparse
import json
import os
from pathlib import Path

os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
from faster_whisper import WhisperModel  # noqa: E402


def masa_srt(saat: float) -> str:
    ms = int(round(saat * 1000))
    j, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{j:02}:{m:02}:{s:02},{ms:03}"


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("input")
    p.add_argument("--model", default="small")
    p.add_argument("--bahasa", default="ms", help="kod bahasa, cth. ms, en; 'auto' untuk kesan sendiri")
    p.add_argument("--keluar", default=None)
    a = p.parse_args()

    src = Path(a.input)
    out = Path(a.keluar) if a.keluar else src.parent
    out.mkdir(parents=True, exist_ok=True)

    model = WhisperModel(a.model, device="cpu", compute_type="int8")
    segs, info = model.transcribe(
        str(src),
        language=None if a.bahasa == "auto" else a.bahasa,
        word_timestamps=True,
        vad_filter=True,
    )

    srt, words, segments = [], [], []
    for i, s in enumerate(segs, 1):
        text = s.text.strip()
        srt.append(f"{i}\n{masa_srt(s.start)} --> {masa_srt(s.end)}\n{text}\n")
        segments.append({"start": round(s.start, 3), "end": round(s.end, 3), "text": text})
        for w in s.words or []:
            words.append({"word": w.word.strip(), "start": round(float(w.start), 3),
                          "end": round(float(w.end), 3), "prob": round(float(w.probability), 3)})

    (out / f"{src.stem}.srt").write_text("\n".join(srt), encoding="utf-8")
    (out / f"{src.stem}.words.json").write_text(
        json.dumps({"language": info.language, "segments": segments, "words": words},
                   ensure_ascii=False, indent=2),
        encoding="utf-8")
    print(f"Bahasa: {info.language} | segmen: {len(segments)} | perkataan: {len(words)}")
    print(f"Ditulis: {out / (src.stem + '.srt')}")
    print(f"Ditulis: {out / (src.stem + '.words.json')}")


if __name__ == "__main__":
    main()
