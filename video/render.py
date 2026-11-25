"""Render 30fps frames of template.html with Playwright, pipe to ffmpeg, mux with mix.wav.
Usage: python3 render.py [--preview t1,t2,...]"""
import json, os, subprocess, sys
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__)); B = os.path.join(HERE, "build")
ep = json.load(open(os.path.join(HERE, "episode.json"))); tl = json.load(open(os.path.join(B, "timeline.json")))
FPS = 30
OUT = os.path.join(HERE, f"funded-tape-short-{ep['slug']}.mp4")

def page_ctx(p):
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
    pg = b.new_page(viewport={"width": 1080, "height": 1920})
    pg.add_init_script("window.DATA = " + json.dumps({"ep": ep, "timeline": tl}) + ";")
    pg.goto("file://" + os.path.join(HERE, "template.html")); pg.wait_for_timeout(300)
    return b, pg

with sync_playwright() as p:
    b, pg = page_ctx(p)
    if len(sys.argv) > 2 and sys.argv[1] == "--preview":
        os.makedirs(os.path.join(B, "preview"), exist_ok=True)
        for t in sys.argv[2].split(","):
            pg.evaluate(f"render({float(t)})"); pg.screenshot(path=os.path.join(B, "preview", f"t{float(t):06.2f}.png"))
        sys.exit(0)
    pg.evaluate("renderCover()"); pg.screenshot(path=os.path.join(HERE, f"cover-{ep['slug']}.png"))
    if "--cover" in sys.argv: sys.exit(0)
    n = int(round(tl["duration"] * FPS))
    silent = os.path.join(B, "video_noaudio.mp4")
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-",
                           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(FPS), silent], stdin=subprocess.PIPE)
    for i in range(n):
        pg.evaluate(f"render({i / FPS})")
        ff.stdin.write(pg.screenshot(type="jpeg", quality=93))
        if i % 300 == 0: print("frame", i, "/", n, flush=True)
    ff.stdin.close(); ff.wait(); b.close()
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", silent, "-i", os.path.join(B, "mix.wav"), "-map", "0:v", "-map", "1:a",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", OUT], check=True)
print("wrote", OUT)
