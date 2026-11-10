# Audio des quartiers centraux de Steel (packs fecc483 + cc1e161, Groovy Crew) :
# - Rotation des 4 remixes limitée à Pulse Plaza + Steel Arena (continuité sans coupure entre les deux zones, enchaînement 01->02->03->04->01, API rythme ostCentre).
# - OST dédiée en boucle à Center-Town (steel_center + intérieur change_in atténué).
# - OST dédiée en boucle à Fréquence Strip (steel_strip).
# - Vérifie aussi la boucle circulaire des portes : Center-Town -> Pulse Plaza -> Steel Arena -> Fréquence Strip -> Center-Town, et l'absence de tout nom civil interdit.
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); from nml_boot import passer_boot  # menu Terminal : sauter l'allumage
import sys, os, re, time, json, hashlib, urllib.request
from playwright.sync_api import sync_playwright

URL = os.environ.get('URL', 'http://127.0.0.1:8877/')
if not URL.endswith('/'): URL += '/'
OUT = os.environ.get('OUT', '/tmp/nml-test-out/ost_centre/')
os.makedirs(OUT, exist_ok=True)

EXPECTED_TRACKS = [
    ('01_bad_buzz_protocol_remix.mp3', 'd4a3c36e1cdb16bed286fd366b061fc89a3fa954cdbe15543c15263e3b1ef989', 'Bad Buzz Protocol (Remix)'),
    ('02_dance_soit_plus_chrome_16bit.mp3', '675d4fac382b9fe8c00e0f87b7b0aeec84998e35303e54a64e8fe45350ec6ea8', 'Dance soit plus chrome (16bit)'),
    ('03_steel_megalopolis_remix.mp3', 'e9907344e92729284a8642927ec177139a252acda90314f579749132bd43daae', 'Steel-Megalopolis (Remix)'),
    ('04_we_already_knew_remix.mp3', '1bc6564eb8863983fb0a4315cd59dc0fe24f32df6ebc42614637bae1dd3cd89b', 'We Already Knew (Remix)'),
]
DEDICATED_TRACKS = [
    ('assets/audio/ost_center_town/01_center_town.mp3', '6268ed3983aa0821d8d130ca1ffeb88a4b2b23319084dd12c4a1962ff9468_placeholder'),
]

R = []
def check(n, ok, d=''):
    R.append({'test': n, 'ok': bool(ok), 'detail': str(d)[:220]})
    print(('OK    ' if ok else 'ECHEC ') + n, '' if ok else str(d)[:220], flush=True)

MP3_BYTES = {}
for fname, sha_ref, _ in EXPECTED_TRACKS:
    raw = urllib.request.urlopen(URL + 'assets/audio/ost_centre/' + fname).read()
    MP3_BYTES[fname] = raw
    h = hashlib.sha256(raw).hexdigest()
    check(f'MP3 ost_centre servi octet-identique (SHA-256) : {fname}', h == sha_ref, h)

for rel, fname, sha_ref in [
    ('assets/audio/ost_center_town/01_center_town.mp3', '01_center_town.mp3', '6268ed3983aa0821d8d130ca1ffeb88a4b2b23319084dd12c82c4a1962ff9468'),
    ('assets/audio/ost_strip/01_we_already_knew_frequence_strip.mp3', '01_we_already_knew_frequence_strip.mp3', 'a615c67cc7c03a3877d46f14d585a5d337f7d635228e758c8dd46cb940f1e890'),
]:
    raw = urllib.request.urlopen(URL + rel).read()
    MP3_BYTES[fname] = raw
    h = hashlib.sha256(raw).hexdigest()
    check(f'MP3 dédié servi octet-identique (SHA-256) : {fname}', h == sha_ref, h)

def serve_mp3_range(route, request):
    fname = request.url.rsplit('/', 1)[-1].split('?')[0]
    data = MP3_BYTES.get(fname)
    if data is None:
        return route.continue_()
    total = len(data)
    rng = request.headers.get('range')
    if rng:
        m = re.match(r'bytes=(\d+)-(\d*)', rng)
        if m:
            start = int(m.group(1))
            end = int(m.group(2)) if m.group(2) else total - 1
            end = min(end, total - 1)
            chunk = data[start:end + 1]
            return route.fulfill(status=206, body=chunk, headers={
                'Content-Type': 'audio/mpeg',
                'Accept-Ranges': 'bytes',
                'Content-Range': f'bytes {start}-{end}/{total}',
                'Content-Length': str(len(chunk)),
            })
    return route.fulfill(status=200, body=data, headers={
        'Content-Type': 'audio/mpeg',
        'Accept-Ranges': 'bytes',
        'Content-Length': str(total),
    })

with sync_playwright() as p:
    br = p.chromium.launch(channel='chrome', args=[
        '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
        '--ignore-gpu-blocklist', '--autoplay-policy=user-gesture-required'
    ])
    for prof in ('desktop', 'mobile'):
        ctx = (br.new_context(viewport={'width': 1280, 'height': 800})
               if prof == 'desktop'
               else br.new_context(viewport={'width': 390, 'height': 844}, has_touch=True, is_mobile=True, device_scale_factor=2))
        ctx.route('**/assets/audio/**/*.mp3', serve_mp3_range)
        pg = ctx.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: m.type == 'error' and errs.append(m.text))
        pg.goto(URL)
        pg.wait_for_function('window.__nml && window.__nml.ostCentre && window.__nml.shell', timeout=60000)
        time.sleep(1.0)
        E = pg.evaluate
        gesture = pg.touchscreen.tap if prof == 'mobile' else pg.mouse.click

        def tapel(sel):
            b = pg.locator(sel).bounding_box()
            gesture(b['x'] + b['width'] / 2, b['y'] + b['height'] / 2)
            time.sleep(0.3)

        S = lambda: E('''() => {
          const a = window.__nml.music, o = window.__nml.ostCentre;
          return {
            loc: window.__nml.state.location,
            zones: o.zones,
            mode: o.mode,
            active: o.active,
            playing: o.playing,
            idx: o.trackIndex,
            id: o.track?.id,
            title: o.track?.title,
            artist: o.track?.artist,
            paused: a.paused,
            muted: a.muted,
            loop: a.loop,
            vol: +a.volume.toFixed(3),
            t: +a.currentTime.toFixed(3),
            dur: +(a.duration || 0).toFixed(2),
            src: a.currentSrc,
            nAudio: document.querySelectorAll('audio').length,
            sameEl: o.el === a,
            beat: +o.beat.toFixed(3),
            energy: +o.energy.toFixed(3),
            bass: +o.bass.toFixed(3),
            kicks: o.kickCount,
            bpm: o.bpm,
            hasAnalyser: !!o.analyser
          };
        }''')

        s0 = S()
        check(f'{prof}: muette avant tout geste utilisateur et zones ost_centre = [steel_pulse, steel_arena]',
              s0['paused'] and s0['nAudio'] == 1 and s0['sameEl'] and s0['zones'] == ['steel_pulse', 'steel_arena'], s0)
        E("localStorage.removeItem('nml_muted'); localStorage.removeItem('nml_save_auto')")
        passer_boot(pg); tapel('#m-new'); time.sleep(0.35); tapel('#cr-next'); tapel('#cr-enter')
        pg.wait_for_function('!document.body.classList.contains("menu-open")')
        time.sleep(0.6)

        cred_dump = E("JSON.stringify(window.__nml.ostCentre.tracks)")
        check(f'{prof}: canon crédits Groovy Crew (aucun nom civil)',
              all(t['artist'] == 'Groovy Crew' and set(t.keys()) <= {'index', 'id', 'file', 'title', 'artist'} for t in json.loads(cred_dump)),
              cred_dump)

        # 1. Center-Town : OST dédiée en boucle, continue et atténuée dans change_in
        E("(()=>{const g=window.__nml.game,s=g.snapshot();s.location='steel_center';s.player.x=13;s.player.z=8.7;g.restore(s,true)})()")
        pg.wait_for_function("!window.__nml.music.paused && window.__nml.music.currentTime > 0.2 && Math.abs(window.__nml.music.volume - 0.55) < 0.05", timeout=10000)
        time.sleep(1.0)
        E("window.__nml.music.dataset.ostMark = 'singleton'")
        ct0 = S()
        check(f'{prof}: Center-Town joue son OST dédiée en boucle (01_center_town.mp3, active=false)',
              not ct0['active'] and ct0['mode'] == 'ost_center_town' and ct0['loop'] and not ct0['paused']
              and '01_center_town.mp3' in ct0['src'] and ct0['nAudio'] == 1 and abs(ct0['vol'] - 0.55) < 0.06, ct0)
        t_ct = ct0['t']
        E("window.__nml.game.useDoor('c_change_door')")
        pg.wait_for_function("window.__nml.state.location === 'change_in'", timeout=8000)
        time.sleep(1.8)
        cin = S()
        check(f'{prof}: intérieur Center-Town (change_in) : OST Center-Town continue sans coupure, volume atténué',
              cin['loc'] == 'change_in' and '01_center_town.mp3' in cin['src'] and not cin['paused']
              and cin['t'] > t_ct + 0.8 and cin['vol'] < 0.3, cin)
        E("window.__nml.game.useDoor('change_in_door')")
        pg.wait_for_function("window.__nml.state.location === 'steel_center'", timeout=8000)

        # 2. Boucle Center-Town -> Pulse Plaza -> Steel Arena (continuité des 4 titres entre Pulse et Arena)
        E("(()=>{const g=window.__nml.game,s=g.snapshot();s.location='steel_center';s.player.x=33;s.player.z=1.5;g.restore(s,true)})()")
        E("window.__nml.game.useDoor('c_nord')")
        pg.wait_for_function("window.__nml.state.location === 'steel_pulse' && window.__nml.ostCentre.active && !window.__nml.music.paused && window.__nml.music.currentTime > 0.2", timeout=10000)
        time.sleep(1.0)
        p0 = S()
        check(f'{prof}: Pulse Plaza lance la rotation des 4 titres (piste 01, loop=false, active=true)',
              p0['active'] and not p0['paused'] and not p0['loop'] and p0['idx'] == 0
              and '01_bad_buzz_protocol_remix.mp3' in p0['src'], p0)

        t_prev = p0['t']
        src_prev = p0['src']
        for px, pz, door, target_loc, label in [
            (46.5, 13, 'pp_est', 'steel_arena', 'Pulse Plaza -> Steel Arena'),
            (1.5, 44, 'ar_ouest', 'steel_pulse', 'Steel Arena -> Pulse Plaza'),
            (46.5, 13, 'pp_est', 'steel_arena', 'Pulse Plaza -> Steel Arena (retour)'),
        ]:
            E(f"(()=>{{const g=window.__nml.game,s=g.snapshot();s.player.x={px};s.player.z={pz};g.restore(s,true)}})()")
            E(f"window.__nml.game.useDoor('{door}')")
            pg.wait_for_function(f"window.__nml.state.location === '{target_loc}'", timeout=8000)
            time.sleep(0.9)
            cur = S()
            same_dom = E("window.__nml.music.dataset.ostMark === 'singleton'")
            check(f'{prof}: continuité {label} (même piste, même instance, temps {t_prev:.2f}s -> {cur["t"]:.2f}s)',
                  cur['loc'] == target_loc and same_dom and cur['active'] and not cur['paused']
                  and cur['idx'] == 0 and cur['src'] == src_prev and cur['t'] > t_prev + 0.5,
                  (t_prev, cur))
            t_prev = cur['t']

        # 3. Suite de la boucle : Steel Arena (ar_est) -> Fréquence Strip (OST dédiée) -> Center-Town (fs_ouest -> c_strip)
        E("(()=>{const g=window.__nml.game,s=g.snapshot();s.player.x=94.5;s.player.z=44;g.restore(s,true)})()")
        E("window.__nml.game.useDoor('ar_est')")
        pg.wait_for_function("window.__nml.state.location === 'steel_strip' && !window.__nml.music.paused && window.__nml.music.currentTime > 0.15", timeout=10000)
        time.sleep(0.8)
        fs0 = S()
        check(f'{prof}: Steel Arena -> Fréquence Strip : bascule sur OST dédiée Strip en boucle (active=false)',
              fs0['loc'] == 'steel_strip' and not fs0['active'] and fs0['mode'] == 'ost_strip'
              and fs0['loop'] and '01_we_already_knew_frequence_strip.mp3' in fs0['src'], fs0)

        E("(()=>{const g=window.__nml.game,s=g.snapshot();s.player.x=1.5;s.player.z=10;g.restore(s,true)})()")
        E("window.__nml.game.useDoor('fs_ouest')")
        pg.wait_for_function("window.__nml.state.location === 'steel_center' && !window.__nml.music.paused", timeout=10000)
        time.sleep(0.6)
        ct1 = S()
        check(f'{prof}: Fréquence Strip -> Center-Town : boucle fermée, retour sur OST Center-Town',
              ct1['loc'] == 'steel_center' and ct1['mode'] == 'ost_center_town' and '01_center_town.mp3' in ct1['src'], ct1)

        # 4. Analyse de rythme / kick sur Pulse Plaza (v3) et Steel Arena (_faisceau_fix)
        E("(()=>{const g=window.__nml.game,s=g.snapshot();s.location='steel_pulse';s.player.x=24;s.player.z=18;g.restore(s,true)})()")
        pg.wait_for_function("window.__nml.ostCentre.active && !window.__nml.music.paused", timeout=10000)
        E('''() => {
          window.__kickEvents = [];
          window.__offKick = window.__nml.ostCentre.onKick(ev => window.__kickEvents.push(ev));
          window.__nml.music.currentTime = 42;
        }''')
        max_energy = max_bass = max_beat = 0.0
        for _ in range(25):
            time.sleep(0.1)
            st_b = S()
            max_energy = max(max_energy, st_b['energy'])
            max_bass = max(max_bass, st_b['bass'])
            max_beat = max(max_beat, st_b['beat'])
        kicks_logged = E("window.__kickEvents.length")
        first_kick = E("window.__kickEvents[0] || null")
        E("window.__offKick()")
        kicks_after_off = E("window.__kickEvents.length")
        time.sleep(0.6)
        kicks_still = E("window.__kickEvents.length")
        check(f'{prof}: API rythme Pulse Plaza active (AnalyserNode, energy={max_energy:.2f}, bass={max_bass:.2f}, kicks={kicks_logged})',
              S()['hasAnalyser'] and max_energy > 0.05 and max_bass > 0.1 and 0 < max_beat <= 1.0
              and kicks_logged >= 1 and first_kick and first_kick['beat'] == 1,
              (max_energy, max_bass, max_beat, kicks_logged, first_kick))
        check(f'{prof}: désabonnement onKick() respecté', kicks_still == kicks_after_off, (kicks_after_off, kicks_still))

        pulse_samples = []
        for _ in range(16):
            time.sleep(0.06)
            pulse_samples.append(E("Object.fromEntries(window.__nml.view.pulses().filter(p=>p.priorite>0).map(p=>[p.key,p.opacity]))"))
        feed_ops = [x.get('pp_ecran_feed_v3_3q_pulse', 0) for x in pulse_samples]
        feed_ec = [x.get('pp_ecran_feed_v3_3q_ecran', 0) for x in pulse_samples]
        nord_ops = [x.get('pp_nord_a_v2_3q_pulse', 0) for x in pulse_samples]
        bb_ops = [x.get('pp_billboard_v2_3q_pulse', 0) for x in pulse_samples]
        bb_ec = [x.get('pp_billboard_v2_3q_ecran', 0) for x in pulse_samples]
        pont_fs = [x.get('pp_pont_projecteurs_v3_3q_faisceau', 0) for x in pulse_samples]
        check(f'{prof}: calques Pulse Plaza v3 (Feed v3, Billboard, Nord_A, Pont v3 faisceau<=0.5) frappent sur le kick',
              max(feed_ops) - min(feed_ops) > 0.45 and max(feed_ec) - min(feed_ec) > 0.45
              and max(bb_ops) - min(bb_ops) > 0.45 and max(bb_ec) - min(bb_ec) > 0.45
              and max(nord_ops) - min(nord_ops) > 0.45
              and max(pont_fs) - min(pont_fs) > 0.20 and max(pont_fs) <= 0.50,
              (round(min(feed_ops), 3), round(max(feed_ops), 3), round(min(pont_fs), 3), round(max(pont_fs), 3)))

        E("(()=>{const g=window.__nml.game,s=g.snapshot();s.location='steel_arena';s.player.x=44;s.player.z=40;g.restore(s,true)})()")
        time.sleep(0.5)
        arena_samples = []
        for _ in range(16):
            time.sleep(0.06)
            arena_samples.append(E("Object.fromEntries(window.__nml.view.pulses().filter(p=>p.priorite>=3).map(p=>[p.key,p.opacity]))"))
        ar_ex = [x.get('ar2_ecran_geant_x_pulse2', 0) for x in arena_samples]
        ar_ez = [x.get('ar2_ecran_geant_z_pulse2', 0) for x in arena_samples]
        ar_ep = [x.get('ar2_facade_entree_pulse2', 0) for x in arena_samples]
        ar_fs = [x.get('ar2_facade_entree_faisceau_fix', 0) for x in arena_samples]
        check(f'{prof}: calques Steel Arena (écrans géants + entrée pulse2 + faisceau_fix) frappent sur le kick',
              max(ar_ex) - min(ar_ex) > 0.45 and max(ar_ez) - min(ar_ez) > 0.45
              and max(ar_ep) - min(ar_ep) > 0.45 and max(ar_fs) - min(ar_fs) > 0.40,
              (round(min(ar_ex), 3), round(max(ar_ex), 3), round(min(ar_ep), 3), round(max(ar_ep), 3)))

        if prof == 'desktop':
            for expected_next_idx, (next_fname, _, next_title) in [
                (1, EXPECTED_TRACKS[1]),
                (2, EXPECTED_TRACKS[2]),
                (3, EXPECTED_TRACKS[3]),
                (0, EXPECTED_TRACKS[0]),
            ]:
                pg.wait_for_function("window.__nml.music.duration > 60 && window.__nml.music.seekable.length > 0", timeout=10000)
                E("window.__nml.music.currentTime = window.__nml.music.duration - 0.9")
                pg.wait_for_function(
                    f"window.__nml.ostCentre.trackIndex === {expected_next_idx} && !window.__nml.music.paused && window.__nml.music.currentTime > 0.1 && window.__nml.music.currentTime < 6",
                    timeout=10000
                )
                time.sleep(0.3)
                sn = S()
                check(f'desktop: enchaînement fin de piste -> piste {expected_next_idx + 1} ({next_fname})',
                      sn['idx'] == expected_next_idx and next_fname in sn['src'] and sn['title'] == next_title
                      and not sn['paused'] and 0 < sn['t'] < 6, sn)

            tapel('#k-son'); time.sleep(0.25)
            sm = S()
            check('desktop: bouton Son coupe (muted=true, beat=0, energy=0)',
                  sm['muted'] and not sm['playing'] and sm['beat'] == 0 and sm['energy'] == 0, sm)
            tapel('#k-son'); time.sleep(0.4)
            su = S()
            check('desktop: bouton Son rétablit la lecture', not su['muted'] and su['playing'] and not su['paused'], su)

            E("window.__nml.music.currentTime = 28")
            time.sleep(0.4)
            t_saved = S()['t']
            E("(()=>{const g=window.__nml.game,s=g.snapshot();s.location='steel_lower';s.player.x=6;s.player.z=18;g.restore(s,true)})()")
            time.sleep(0.8)
            sl = S()
            check("desktop: hors des zones musicales (Lower-Town) : délègue à l'ambiance en boucle",
                  not sl['active'] and 'dusk_town_ambiance.mp3' in sl['src'] and sl['loop'] and not sl['paused'], sl)
            E("(()=>{const g=window.__nml.game,s=g.snapshot();s.location='steel_pulse';s.player.x=24;s.player.z=18;g.restore(s,true)})()")
            pg.wait_for_function("window.__nml.ostCentre.active && !window.__nml.music.paused && window.__nml.music.currentTime > 20", timeout=10000)
            time.sleep(0.5)
            sr = S()
            check('desktop: retour dans Pulse Plaza : reprend la rotation OST là où elle en était',
                  sr['active'] and sr['idx'] == 0 and sr['t'] >= t_saved - 0.5 and not sr['paused'], (t_saved, sr))

        check(f'{prof}: aucune erreur JS / console', not errs, errs[:3])
        ctx.close()
    br.close()

ok_count = sum(r['ok'] for r in R)
print(f'{ok_count}/{len(R)} OK')
json.dump(R, open(OUT + 'ost_centre.json', 'w'), indent=1, ensure_ascii=False)
sys.exit(0 if ok_count == len(R) else 1)
