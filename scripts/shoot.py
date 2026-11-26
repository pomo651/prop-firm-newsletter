from playwright.sync_api import sync_playwright
url="file:///workspace/prop-firm-newsletter/demo-email-funded-tape.html"
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/google-chrome")
    for name,w,scale in [("desktop",1000,1),("mobile",390,2)]:
        pg=b.new_page(viewport={"width":w,"height":800},device_scale_factor=scale)
        pg.goto(url); pg.screenshot(path=f"/workspace/prop-firm-newsletter/demo-email-{name}.png",full_page=True)
        print(name, pg.evaluate("document.documentElement.scrollWidth"), pg.evaluate("document.body.scrollHeight"))
    b.close()
