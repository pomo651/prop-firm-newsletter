import glob
from playwright.sync_api import sync_playwright
from PIL import Image
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/google-chrome")
    for f in sorted(glob.glob("/workspace/prop-firm-newsletter/designs/design-*.html")):
        k=f.split("design-")[1][0]
        pg=b.new_page(viewport={"width":900,"height":1400}); pg.goto("file://"+f)
        pg.screenshot(path=f"design-{k}-desktop.png")
        m=b.new_page(viewport={"width":390,"height":1600},device_scale_factor=2); m.goto("file://"+f)
        m.screenshot(path=f"design-{k}-mobile.png")
        print(k, "mobile scrollWidth", m.evaluate("document.documentElement.scrollWidth"))
    b.close()
ims=[Image.open(f"design-{k}-desktop.png").crop((130,0,770,1400)) for k in "abcd"]
W=sum(i.width for i in ims)+50; c=Image.new("RGB",(W,1400),"white"); x=10
for i in ims: c.paste(i,(x,0)); x+=i.width+10
c.save("compare-desktop.png"); print(c.size)
