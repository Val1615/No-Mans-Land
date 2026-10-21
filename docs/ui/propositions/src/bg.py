import time
from playwright.sync_api import sync_playwright
HIDE = "document.querySelectorAll('#hud,#act,#labels,#dialogue,#msg').forEach(e=>e.style.visibility='hidden')"
def place(pg, loc, x, z, cx, cz):
    pg.evaluate(f"()=>{{const s=__nml.state; s.location='{loc}'; s.junctionLock='x'; Object.assign(s.player,{{x:{x},z:{z},path:[]}}); Object.assign(s.companion,{{x:{cx},z:{cz},path:[],location:'{loc}'}})}}"); time.sleep(1.5)
with sync_playwright() as p:
    br = p.chromium.launch(channel='chrome', args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    pg = br.new_page(viewport={'width': 1280, 'height': 800}); pg.goto('http://127.0.0.1:8765/'); pg.wait_for_function('window.__nml', timeout=60000); time.sleep(2); pg.evaluate(HIDE)
    place(pg, 'dusk_q1', 26.6, 15.2, 27.9, 15.8); pg.evaluate('__nml.setCamera({x:24,z:15,ppm:50})'); time.sleep(0.8); pg.screenshot(path='bg_street.png')
    place(pg, 'bar_in', 4.6, 3.6, 6, 6.6); pg.evaluate('__nml.setCamera({x:5,z:4.5,ppm:85})'); time.sleep(0.8); pg.screenshot(path='bg_bar.png')
    ctx = br.new_context(viewport={'width': 390, 'height': 844}, has_touch=True, is_mobile=True, device_scale_factor=2)
    m = ctx.new_page(); m.goto('http://127.0.0.1:8765/'); m.wait_for_function('window.__nml', timeout=60000); time.sleep(2); m.evaluate(HIDE)
    place(m, 'dusk_q1', 26.6, 15.2, 27.9, 15.8); m.screenshot(path='bg_mobile.png')
    br.close()
