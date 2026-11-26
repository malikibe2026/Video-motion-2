"""Capture a web page at 2x retina scale via HyperFrames' headless Chrome for a `page:` or `receipt:` scene.
usage: capture.py URL OUT_PNG [--width 960] [--height 4000] [--mobile]
Default --width 960 outputs a crisp 1920px-wide PNG for 16:9 explainers (--mobile sets width=540 for 1080px-wide 9:16)."""
import argparse, os, subprocess

from common import die, hf_cmd, hf_env


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("out")
    ap.add_argument("--width", type=int, default=960, help="CSS viewport width (PNG is 2x wide)")
    ap.add_argument("--height", type=int, default=4000, help="PNG height in device pixels")
    ap.add_argument("--mobile", action="store_true", help="Shortcut for --width 540 (1080px PNG for 9:16)")
    a = ap.parse_args()
    width = 540 if a.mobile else a.width

    chrome = subprocess.run(hf_cmd("browser", "path"), capture_output=True, text=True, env=hf_env()).stdout.strip().splitlines()
    if not chrome or not os.path.isfile(chrome[-1]):
        die("HyperFrames has no Chrome yet: run setup.sh")

    out = os.path.abspath(a.out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    subprocess.run([
        chrome[-1], "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2",
        f"--window-size={width},{a.height // 2}", "--virtual-time-budget=8000", f"--screenshot={out}", a.url,
    ], capture_output=True)
    if not os.path.isfile(out):
        die(f"Chrome could not capture {a.url}")
    print(f"Captured {a.url} -> {out} ({width * 2}px wide). Inspect it, then pick a TOP>TOP drift for page: or mark boxes for receipt:.")


if __name__ == "__main__":
    main()
