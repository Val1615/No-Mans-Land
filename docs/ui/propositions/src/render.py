import time
from playwright.sync_api import sync_playwright
J = []
with sync_playwright() as p:
    br = p.chromium.launch(channel='chrome')
    d = br.new_page(viewport={'width': 1280, 'height': 800})
    m = br.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2).new_page()
    for D in 'ABC':
        for s, bg in [('dlg', 'bg_bar.png'), ('inv', 'bg_street.png'), ('mini', 'bg_street.png')]:
            d.goto(f'file:///workspace/nml/docs/ui/propositions/src/ui.html?d={D}&s={s}&bg={bg}'); time.sleep(0.6); d.screenshot(path=f'{D}_desk_{s}.png')
        for s in ['dlg', 'inv']:
            m.goto(f'file:///workspace/nml/docs/ui/propositions/src/ui.html?d={D}&s={s}&m=1&bg=bg_mobile.png'); time.sleep(0.6); m.screenshot(path=f'{D}_mob_{s}.png')
    br.close()
