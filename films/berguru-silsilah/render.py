"""Render the film frame by frame with Playwright, pipe JPEG frames to ffmpeg.

python render.py probe 3 12 20 ...        -> probe/sheet.png (stills at those seconds)
python render.py chunk K N [fps]          -> out/chunk_K.mp4 (frames K/N of the film)
python render.py all [fps] [N]            -> N chunks in parallel, then concat -> out/video.mp4
"""
import asyncio, subprocess, sys, os, math, json, functools, http.server, threading
from playwright.async_api import async_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = 8765
W, H = 1080, 1920


def serve():
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
    handler.log_message = lambda *a: None
    try:
        srv = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), handler)
    except OSError:
        return  # another process already serves the folder
    threading.Thread(target=srv.serve_forever, daemon=True).start()


async def open_page(p):
    b = await p.chromium.launch(executable_path=os.environ.get("CHROME", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"), args=["--font-render-hinting=none", "--force-color-profile=srgb", "--disable-checker-imaging"])
    page = await b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
    await page.goto(f"http://127.0.0.1:{PORT}/index.html?render=1")
    await page.wait_for_function("window.ready === true", timeout=60000)
    return b, page


async def shot(page, t, fmt="jpeg"):
    await page.evaluate(f"window.seek({t:.5f})")
    await page.evaluate("new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))")
    if fmt == "png":
        return await page.screenshot(type="png")
    return await page.screenshot(type="jpeg", quality=95)


async def probe(times):
    os.makedirs(f"{ROOT}/probe", exist_ok=True)
    async with async_playwright() as p:
        b, page = await open_page(p)
        for t in times:
            open(f"{ROOT}/probe/t{t:07.2f}.png", "wb").write(await shot(page, t, "png"))
        await b.close()
    files = " ".join(f"-i {ROOT}/probe/t{t:07.2f}.png" for t in times)
    n = len(times)
    cols = min(n, 4)
    rows = math.ceil(n / cols)
    inputs = "".join(f"[{i}:v]scale=360:-1[s{i}];" for i in range(n))
    pad = n < cols * rows
    layout = "|".join(f"{(i % cols) * 360}_{(i // cols) * 640}" for i in range(n))
    cmd = f"ffmpeg -y -loglevel error {files} -filter_complex \"{inputs}{''.join(f'[s{i}]' for i in range(n))}xstack=inputs={n}:layout={layout}:fill=black\" {ROOT}/probe/sheet.png"
    if n == 1:
        cmd = f"ffmpeg -y -loglevel error {files} -vf scale=540:-1 {ROOT}/probe/sheet.png"
    subprocess.run(cmd, shell=True, check=True)


async def chunk(k, n, fps):
    os.makedirs(f"{ROOT}/out", exist_ok=True)
    async with async_playwright() as p:
        b, page = await open_page(p)
        dur = await page.evaluate("window.DUR")
        total = int(math.ceil(dur * fps))
        a, z = total * k // n, total * (k + 1) // n
        ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(fps), "-c:v", "mjpeg", "-i", "-",
                               "-vf", "scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv420p",
                               "-c:v", "libx264", "-preset", "medium", "-crf", "15", "-color_range", "tv", "-colorspace", "bt709",
                               "-color_primaries", "bt709", "-color_trc", "bt709", f"{ROOT}/out/chunk_{k}.mp4"], stdin=subprocess.PIPE)
        for f in range(a, z):
            ff.stdin.write(await shot(page, f / fps))
            if (f - a) % 300 == 0:
                print(f"chunk {k}: {f - a}/{z - a}", flush=True)
        ff.stdin.close(); ff.wait()
        await b.close()
        json.dump({"frames": z - a}, open(f"{ROOT}/out/chunk_{k}.json", "w"))


def main():
    serve()
    mode = sys.argv[1]
    if mode == "probe":
        asyncio.run(probe([float(x) for x in sys.argv[2:]]))
    elif mode == "chunk":
        asyncio.run(chunk(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]) if len(sys.argv) > 4 else 30))
    elif mode == "all":
        fps = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        n = int(sys.argv[3]) if len(sys.argv) > 3 else 4
        procs = [subprocess.Popen([sys.executable, __file__, "chunk", str(k), str(n), str(fps)]) for k in range(n)]
        for pr in procs:
            if pr.wait() != 0:
                raise SystemExit("chunk failed")
        with open(f"{ROOT}/out/concat.txt", "w") as f:
            for k in range(n):
                f.write(f"file 'chunk_{k}.mp4'\n")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", f"{ROOT}/out/concat.txt", "-c", "copy", f"{ROOT}/out/video.mp4"], check=True)
        print("video ->", f"{ROOT}/out/video.mp4")


if __name__ == "__main__":
    main()
