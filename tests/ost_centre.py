# Playlist OST commune (pack fecc483, Groovy Crew) : Center-Town, Fréquence Strip, Pulse Plaza, Steel Arena.
# Vérifie : fichiers MP3 octet-identiques (SHA-256), un seul lecteur <audio>, continuité sans coupure ni remise à zéro entre les 4 zones
# (et l'intérieur change_in), enchaînement complet 01 -> 02 -> 03 -> 04 -> 01 en fin de piste, API rythme/kick (ostCentre),
# respect du bouton Son / autoplay, retour à l'ambiance hors des 4 zones, canon Groovy Crew (aucun nom civil).
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

R = []
def check(n, ok, d=''):
    R.append({'test': n, 'ok': bool(ok), 'detail': str(d)[:220]})
    print(('OK    ' if ok else 'ECHEC ') + n, '' if ok else str(d)[:220], flush=True)

MP3_BYTES = {}
for fname, sha_ref, _ in EXPECTED_TRACKS:
    raw = urllib.request.urlopen(URL + 'assets/audio/ost_centre/' + fname).read()
    MP3_BYTES[fname] = raw
    h = hashlib.sha256(raw).hexdigest()
    check(f'MP3 servi octet-identique (SHA-256) : {fname}', h == sha_ref, h)

# python -m http.server n'envoie pas Accept-Ranges: bytes (contrairement à GitHub Pages) ; ce gestionnaire sert les octets exacts en 200/206 pour permettre le seek vers la fin de piste.
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
        ctx.route('**/assets/audio/ost_centre/*.mp3', serve_mp3_range)
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
        check(f'{prof}: muette avant tout geste utilisateur', s0['paused'] and s0['nAudio'] == 1 and s0['sameEl'], s0)
        E("localStorage.removeItem('nml_muted'); localStorage.removeItem('nml_save_auto')")
        tapel('#m-new'); time.sleep(0.35); tapel('#cr-next'); tapel('#cr-enter')
        pg.wait_for_function('!document.body.classList.contains("menu-open")')
        time.sleep(0.6)

        # Canon crédits : Groovy Crew, aucun nom civil interdit
        cred_dump = E("JSON.stringify(window.__nml.ostCentre.tracks)")
        check(f'{prof}: canon crédits Groovy Crew (aucun nom civil)',
              all(t['artist'] == 'Groovy Crew' and set(t.keys()) <= {'index', 'id', 'file', 'title', 'artist'} for t in json.loads(cred_dump)),
              cred_dump)

        # Entrée dans Center-Town : démarre la rotation commune sur la piste 1
        E("(()=>{const g=window.__nml.game,s=g.snapshot();s.location='steel_center';s.player.x=33;s.player.z=2;g.restore(s,true)})()")
        pg.wait_for_function("window.__nml.ostCentre.active && !window.__nml.music.paused && window.__nml.music.currentTime > 0.25", timeout=10000)
        time.sleep(1.2)
        E("window.__nml.music.dataset.ostMark = 'singleton'")
        c0 = S()
        check(f'{prof}: Center-Town lance la piste 01 (un seul <audio>, loop=false, volume≈0.55)',
              c0['active'] and not c0['paused'] and not c0['muted'] and not c0['loop']
              and c0['idx'] == 0 and c0['id'] == '01_bad_buzz_protocol_remix'
              and '01_bad_buzz_protocol_remix.mp3' in c0['src']
              and c0['nAudio'] == 1 and abs(c0['vol'] - 0.55) < 0.06, c0)

        # Traversée continue des 4 zones par vraies portes : Center-Town -> Pulse Plaza -> Fréquence Strip -> Steel Arena -> Strip
        t_prev = c0['t']
        src_prev = c0['src']
        for px, pz, door, target_loc, label in [
            (33, 1.5, 'c_nord', 'steel_pulse', 'Center-Town -> Pulse Plaza'),
            (46.5, 13, 'pp_est', 'steel_strip', 'Pulse Plaza -> Fréquence Strip'),
            (78.5, 13, 'fs_est', 'steel_arena', 'Fréquence Strip -> Steel Arena'),
            (1.5, 44, 'ar_ouest', 'steel_strip', 'Steel Arena -> Fréquence Strip'),
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

        # Intérieur de Center-Town (Change de Teng) : même piste continue, volume atténué à ~0,25
        E("(()=>{const g=window.__nml.game,s=g.snapshot();s.location='steel_center';s.player.x=13;s.player.z=8.7;g.restore(s,true)})()")
        E("window.__nml.game.useDoor('c_change_door')")
        pg.wait_for_function("window.__nml.state.location === 'change_in'", timeout=8000)
        time.sleep(2.0)
        cin = S()
        check(f'{prof}: intérieur Center-Town (change_in) : piste continue sans coupure, volume atténué',
              cin['loc'] == 'change_in' and cin['active'] and not cin['paused']
              and cin['idx'] == 0 and cin['t'] > t_prev + 1.0 and cin['vol'] < 0.3, cin)
        E("window.__nml.game.useDoor('change_in_door')")
        pg.wait_for_function("window.__nml.state.location === 'steel_center'", timeout=8000)

        # Analyse de rythme / kick branchée sur la même lecture (pour Pulse Plaza)
        E("(()=>{const g=window.__nml.game,s=g.snapshot();s.location='steel_pulse';s.player.x=24;s.player.z=18;g.restore(s,true)})()")
        E('''() => {
          window.__kickEvents = [];
          window.__offKick = window.__nml.ostCentre.onKick(ev => window.__kickEvents.push(ev));
          window.__nml.music.currentTime = 42;
        }''')
        max_energy = 0.0
        max_bass = 0.0
        max_beat = 0.0
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
        time.sleep(0.8)
        kicks_still = E("window.__kickEvents.length")
        check(f'{prof}: API rythme Pulse Plaza active (AnalyserNode, energy={max_energy:.2f}, bass={max_bass:.2f}, kicks={kicks_logged})',
              S()['hasAnalyser'] and max_energy > 0.05 and max_bass > 0.1 and 0 < max_beat <= 1.0
              and kicks_logged >= 1 and first_kick and first_kick['beat'] == 1,
              (max_energy, max_bass, max_beat, kicks_logged, first_kick))
        check(f'{prof}: désabonnement onKick() respecté', kicks_still == kicks_after_off, (kicks_after_off, kicks_still))
        # Calques *_v2_3q_pulse / *_faisceau / *_ecran de Pulse Plaza : varient franchement au rythme OST et respectent la priorité mobile
        pulse_samples = []
        for _ in range(16):
            time.sleep(0.06)
            pulse_samples.append(E("Object.fromEntries(window.__nml.view.pulses().filter(p=>p.priorite>0).map(p=>[p.key,p.opacity]))"))
        feed_ops = [x.get('pp_ecran_feed_v2_3q_pulse', 0) for x in pulse_samples]
        nord_ops = [x.get('pp_nord_a_v2_3q_pulse', 0) for x in pulse_samples]
        bb_ops = [x.get('pp_billboard_v2_3q_pulse', 0) for x in pulse_samples]
        bb_ec = [x.get('pp_billboard_v2_3q_ecran', 0) for x in pulse_samples]
        check(f'{prof}: calques Pulse Plaza *_v2_3q_pulse / *_ecran modulés franchement par ostCentre',
              max(feed_ops) - min(feed_ops) > 0.12 and max(nord_ops) - min(nord_ops) > 0.12
              and max(bb_ops) - min(bb_ops) > 0.10 and max(bb_ec) > 0.3,
              (round(min(feed_ops), 3), round(max(feed_ops), 3), round(min(nord_ops), 3), round(max(nord_ops), 3)))

        # Calques ar2_*_pulse2 / *_faisceau de Steel Arena : modulés sur la même lecture singleton ostCentre
        E("(()=>{const g=window.__nml.game,s=g.snapshot();s.location='steel_arena';s.player.x=44;s.player.z=40;g.restore(s,true)})()")
        time.sleep(0.5)
        arena_samples = []
        for _ in range(16):
            time.sleep(0.06)
            arena_samples.append(E("Object.fromEntries(window.__nml.view.pulses().filter(p=>p.priorite>=3).map(p=>[p.key,p.opacity]))"))
        ar_ex = [x.get('ar2_ecran_geant_x_pulse2', 0) for x in arena_samples]
        ar_ez = [x.get('ar2_ecran_geant_z_pulse2', 0) for x in arena_samples]
        ar_fs = [x.get('ar2_facade_entree_faisceau', 0) for x in arena_samples]
        check(f'{prof}: calques Steel Arena (écrans géants pulse2 + faisceaux) modulés franchement par ostCentre',
              max(ar_ex) - min(ar_ex) > 0.12 and max(ar_ez) - min(ar_ez) > 0.10 and max(ar_fs) - min(ar_fs) > 0.10,
              (round(min(ar_ex), 3), round(max(ar_ex), 3), round(min(ar_fs), 3), round(max(ar_fs), 3)))

        if prof == 'desktop':
            # Enchaînement complet fin de piste -> piste suivante sur les 4 titres puis retour à la piste 01
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

            # Toggle Son (#k-son) : coupe la lecture audible et remet beat/energy à 0, puis rétablit
            tapel('#k-son'); time.sleep(0.25)
            sm = S()
            check('desktop: bouton Son coupe (muted=true, beat=0, energy=0)',
                  sm['muted'] and not sm['playing'] and sm['beat'] == 0 and sm['energy'] == 0, sm)
            tapel('#k-son'); time.sleep(0.4)
            su = S()
            check('desktop: bouton Son rétablit la lecture', not su['muted'] and su['playing'] and not su['paused'], su)

            # Sortie vers une zone hors scope (Lower-Town) -> retour à l'ambiance, puis retour Center-Town -> reprise OST
            E("window.__nml.music.currentTime = 28")
            time.sleep(0.4)
            t_saved = S()['t']
            E("(()=>{const g=window.__nml.game,s=g.snapshot();s.location='steel_lower';s.player.x=6;s.player.z=18;g.restore(s,true)})()")
            time.sleep(0.8)
            sl = S()
            check("desktop: hors des 4 zones (Lower-Town) : délègue à l'ambiance en boucle",
                  not sl['active'] and 'dusk_town_ambiance.mp3' in sl['src'] and sl['loop'] and not sl['paused'], sl)
            E("(()=>{const g=window.__nml.game,s=g.snapshot();s.location='steel_center';s.player.x=45;s.player.z=18;g.restore(s,true)})()")
            pg.wait_for_function("window.__nml.ostCentre.active && !window.__nml.music.paused && window.__nml.music.currentTime > 20", timeout=10000)
            time.sleep(0.5)
            sr = S()
            check('desktop: retour dans Center-Town : reprend la rotation OST là où elle en était',
                  sr['active'] and sr['idx'] == 0 and sr['t'] >= t_saved - 0.5 and not sr['paused'], (t_saved, sr))

        check(f'{prof}: aucune erreur JS / console', not errs, errs[:3])
        ctx.close()
    br.close()

ok_count = sum(r['ok'] for r in R)
print(f'{ok_count}/{len(R)} OK')
json.dump(R, open(OUT + 'ost_centre.json', 'w'), indent=1, ensure_ascii=False)
sys.exit(0 if ok_count == len(R) else 1)
