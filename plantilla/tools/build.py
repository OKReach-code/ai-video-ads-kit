"""Construye film/index.html desde src/template.html con marca.json + escenas.json + los tiempos reales de la locución.
Tiempo de película = tiempo de locución + P. Plano de Kling de la persona: segundo del clip = (t − P) + c (audio/hybrid_premium.json, tools/kling_sync.py).

escenas.json (ver docs/ESCENAS.md):
  "escenas":  tramos que se suceden, cada uno hasta que empieza el siguiente. Inicio: "desde": "B2" (bloque del guion) o "desde_palabra": "texto".
     {"tipo": "persona", "plano": "S1"}                       persona a pantalla completa (plano de Kling)
     {"tipo": "persona", "plano": "S2", "modo": "ventana"}    se encoge a una ventana arriba; debajo caben tarjetas ("posicion": "abajo")
     {"tipo": "fondo"}                                       tramo en off sobre el fondo de líneas (para tarjetas, contadores, B-roll)
     {"tipo": "broll", "archivo": "b1.mp4"}                   vídeo a pantalla completa (destello al volver a la persona)
     {"tipo": "cta", "desde_palabra": "¿Quieres"}             pantalla final: la pregunta palabra a palabra + logo (obligatoria, la última)
  "insertos": encima de las escenas, de "desde_palabra" a "hasta_palabra" (opcional "en": "B3" para buscar a partir de ese bloque).
     {"tipo": "clip"|"imagen", "archivo": "x.mp4|x.png", "modo": "tarjeta3d"|"tarjeta"|"recorte"|"completa", "posicion": "arriba"|"centro"|"abajo", "ancho": 760}
     {"tipo": "contador", "de": 0, "a": 5000, "sufijo": " alumnos", "etiqueta": "en 6 meses", "posicion": "centro"}
     {"tipo": "titular", "texto": "...", "posicion": "arriba"}
  "resaltar": [palabras en color] · "fuente_titulares": [palabras en la fuente de titulares dentro del subtítulo]
  "titulares": {"palabra": "acento|resaltado|primario|alerta|texto"} (una palabra grande por bloque) · "inclinados": ["palabra"] (1-2 por anuncio)
  "cta_resaltar": "gratis|demo" · "encuadre_persona": "50% 30%" """
import json, re, pathlib, subprocess, sys, shutil
R = pathlib.Path(__file__).resolve().parent.parent; ROOT = R.parents[1]
sys.path.insert(0, str(ROOT/'tools')); from captions import phrase_blocks, numerals
P = 0.15
M = json.load(open(R/'marca.json' if (R/'marca.json').exists() else ROOT/'marca/marca.json'))
C = json.load(open(R/'escenas.json'))
H = json.load(open(R/'audio/hybrid_premium.json'))
words = json.load(open(R/'audio/vo_words_premium.json'))
f = lambda vo: round(vo + P, 3)
norm = lambda w: re.sub(r'[^\wáéíóúñü%]', '', w.lower())
def W(txt, en=None, n=1):
    a = H[en]['a'] if en else 0.0; hits = [s for s, e, t in words if norm(t) == norm(txt) and s >= a - 0.01]
    if len(hits) < n: sys.exit(f'✗ no encuentro la palabra «{txt}» (n={n}, en={en}) en audio/vo_words.json: escríbela como la transcribe Scribe')
    return f(hits[n - 1])
def start(e):
    if 'desde' in e: return f(H[e['desde']]['a'])
    if 'desde_palabra' in e: return W(e['desde_palabra'], e.get('en'), e.get('n', 1))
    sys.exit(f'✗ falta "desde" o "desde_palabra" en {e}')
def mdur(p): return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p)], capture_output=True, text=True).stdout)
def dims(p):
    o = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', str(p)], capture_output=True, text=True).stdout.strip()
    if o: w, h = o.split(',')[:2]; return int(w), int(h)
    from struct import unpack; b = open(p, 'rb').read(32)
    return unpack('>II', b[16:24]) if b[:8] == b'\x89PNG\r\n\x1a\n' else (1000, 1000)
shot_block = {v['shot']: k for k, v in H.items() if 'shot' in v}
ms = lambda shot, t: round((t - P) + H[shot_block[shot]]['c'], 3)
END = round(f(max(v['b'] for v in H.values())) + 0.45, 3)
DUR = round(END + 2.0, 2)
VID, IMG = R/'film/assets/video', R/'film/assets/img'
FACE = C.get('encuadre_persona', '50% 30%')

# ---- escenas
E = sorted(C['escenas'], key=start)
assert E[-1]['tipo'] == 'cta', 'la última escena tiene que ser la del CTA (pregunta + logo, sin persona ni cartela)'
starts = [0.0 if i == 0 else round(start(e) - (0.12 if 'desde' in e else 0.05), 3) for i, e in enumerate(E)]
ends = starts[1:] + [DUR]
CTA = starts[-1]
items, fondos, flashes, html_v, scenes, warn = [], [], [], [], [], []
prev = None
for i, (e, t0, t1) in enumerate(zip(E, starts, ends)):
    d = round(t1 - t0, 3); scenes.append([t0, t1, e.get('nombre', e['tipo'] + (' ' + e.get('plano', '') if e.get('plano') else ''))])
    if e['tipo'] == 'persona':
        s = e['plano']; fn = VID/f'{s}.mp4'; m = ms(s, t0); lim = mdur(fn)
        if m < 0: sys.exit(f'✗ la escena del plano {s} empieza antes que su frase: ajusta "desde"')
        if m + d > lim + 0.042: warn.append(f'· el plano {s} se acaba {m + d - lim:.2f} s antes del final de su escena: la escena sigue sobre el fondo'); d = round(lim - m - 0.03, 3)
        if e.get('modo') == 'ventana':
            st = 'z-index:2;left:30px;top:90px;width:1020px;height:760px;object-position:50% ' + e.get('ventana_y', '41%'); cls = 'clip win'
            fondos.append((t0, t1 - t0))
        else: st, cls = 'z-index:1', 'clip'
        vid = f'v{i}'; html_v.append(f'<video id="{vid}" class="{cls}" src="assets/video/{s}.mp4" data-start="{t0}" data-duration="{d}" data-media-start="{m}" muted playsinline style="{st}"></video>')
        items.append({'id': vid, 't': t0, 'd': d, 'o': FACE, 'modo': e.get('modo', 'completa'), 'full': e.get('modo') != 'ventana'})
        if prev in ('broll',) : flashes.append(t0)
    elif e['tipo'] == 'broll':
        vid = f'v{i}'; m = e.get('media_inicio', 0.2)
        html_v.append(f'<video id="{vid}" class="clip" src="assets/video/{e["archivo"]}" data-start="{t0}" data-duration="{d}" data-media-start="{m}" muted playsinline style="z-index:1"></video>')
        items.append({'id': vid, 't': t0, 'd': d, 'o': '50% 40%', 'modo': 'completa'})
    elif e['tipo'] in ('fondo', 'cta'): fondos.append((t0, d))
    prev = e['tipo']

# ---- insertos
POS = {'arriba': 300, 'centro': 560, 'abajo': 690}
ins_html, counters, titles, busy = [], [], [], []
for j, x in enumerate(C.get('insertos', [])):
    t0 = round(W(x['desde_palabra'], x.get('en'), x.get('n', 1)) - 0.1, 3)
    t1 = round(W(x['hasta_palabra'], x.get('en'), x.get('n_hasta', 1)) if 'hasta_palabra' in x else t0 + x.get('duracion', 2.5), 3)
    t0 = max(t0, max([s for s in starts if s <= t0 + 0.3] or [0.0]))           # si arranca justo con una escena, entra con ella
    t1 = min(t1, next((s for s in starts if s > t0 + 0.3), DUR) - 0.05)       # nunca cruza un cambio de escena
    if t1 - t0 < 0.4: sys.exit(f'✗ el inserto {x} dura {t1 - t0:.2f} s: revisa desde/hasta')
    d = round(t1 - t0, 3); iid = f'i{j}'; pos = x.get('posicion', 'centro'); top = POS[pos]
    if x['tipo'] in ('clip', 'imagen'):
        modo = x.get('modo', 'tarjeta3d'); src = (VID if x['tipo'] == 'clip' else IMG)/x['archivo']; w, h = dims(src)
        if modo == 'completa': st = 'z-index:9'
        else:
            W0 = x.get('ancho', 760); H0 = round(W0 * h / w)
            hmax = (1080 - top) if pos != 'arriba' else 760
            if H0 > hmax: H0 = hmax; W0 = round(H0 * w / h)
            st = f'z-index:10;left:{(1080 - W0) // 2}px;top:{top}px;width:{W0}px;height:{H0}px'
        cls = 'clip' + ('' if modo == 'completa' else (' cut' if modo == 'recorte' else ' card'))
        if x['tipo'] == 'clip':
            ins_html.append(f'<video id="{iid}" class="{cls}" src="assets/video/{x["archivo"]}" data-start="{t0}" data-duration="{d}" data-media-start="{x.get("media_inicio", 0.2)}" muted playsinline style="{st}"></video>')
        else: ins_html.append(f'<img id="{iid}" class="{cls}" src="assets/img/{x["archivo"]}" alt="" data-start="{t0}" data-duration="{d}" style="{st}" />')
        items.append({'id': iid, 't': t0, 'd': d, 'modo': modo})
    elif x['tipo'] == 'contador':
        ins_html.append(f'<div id="{iid}" class="cnt clip" data-start="{t0}" data-duration="{d}" style="top:{top}px"><div class="n">0</div><div class="l">{x.get("etiqueta", "")}</div></div>')
        counters.append({'id': iid, 't': t0, 'de': x.get('de', 0), 'a': x['a'], 'sufijo': x.get('sufijo', ''), 'dur': round(max(0.6, min(2.2, d - 0.55)), 3)})   # acaba ≥ 0,35 s antes del corte
    elif x['tipo'] == 'titular':
        ins_html.append(f'<div id="{iid}" class="tit clip" data-start="{t0}" data-duration="{d}" style="top:{top}px">{x["texto"]}</div>')
        titles.append({'id': iid, 't': t0})
    busy.append((t0, t1, pos, x.get('modo', '')))

# ---- subtítulos
caps = numerals(phrase_blocks(words, P, {norm(w) for w in C.get('resaltar', [])}, {norm(w) for w in C.get('fuente_titulares', [])}))
cuts = starts[1:]
for c in caps:
    nxt = [t for t in cuts if c['s'] < t < c['x']]
    if nxt: c['x'] = min(c['x'], max(nxt[0], c['e'] - 0.02))
    if c['s'] < starts[1] - 0.1 and E[0]['tipo'] == 'persona': c['prog'] = True            # gancho palabra a palabra
caps = [c for c in caps if c['s'] < CTA - 0.3]                                           # la pregunta del CTA ya sale en pantalla
caps[-1]['x'] = min(caps[-1]['x'], CTA)
full = [(it['t'], it['t'] + it['d']) for it in items if it.get('full')]
def clear(a, b):                                    # persona a pantalla completa sin nada encima → subtítulo a la altura del pecho
    return any(s <= a and b <= e for s, e in full) and not any(s < b and a < e for s, e, p, m in busy)
KIN, TILT = {norm(k): v for k, v in C.get('titulares', {}).items()}, {norm(k) for k in C.get('inclinados', [])}
for c in caps:
    c['y'], c['a'] = (1150, 'c') if clear(c['s'], c['x']) else (1250, 'b')
    ks = [w for w in c['w'] if norm(w['t']) in KIN][-1:]
    over = any(s < c['x'] and c['s'] < e and p in ('abajo', 'centro') and m != 'completa' for s, e, p, m in busy)
    if ks and not over and not c.get('prog'):                                             # nunca encima de una tarjeta
        c['kin'] = True; w = ks[0]; w['k'] = KIN[norm(w['t'])]; w['ast'] = w['hl'] = False; c['tilt'] = norm(w['t']) in TILT
if sum(1 for c in caps if c.get('tilt')) > 2: warn.append('· hay más de 2 titulares inclinados: deja 1-2 como mucho')

# ---- página
T = {'dur': DUR, 'END': END, 'CTA': CTA, 'items': items, 'counters': counters, 'titles': titles, 'flashes': flashes,
     'CW': [[f(s), t] for s, e, t in words if f(s) >= CTA - 0.01], 'ctaHL': C.get('cta_resaltar', '')}
col = M['colores']; fon = M['fuentes']
fondos_html = '\n  '.join(f'<div class="clip spot" data-start="{a}" data-duration="{round(d, 3)}"></div>' for a, d in fondos)
D = {'DUR': f'{DUR:.3f}', 'CTA': f'{CTA:.3f}', 'CTA_D': f'{DUR - CTA:.3f}', 'C_PRIMARY': col['primario'], 'C_ACCENT': col['acento'], 'C_HIGHLIGHT': col['resaltado'],
     'C_ALERT': col.get('alerta', '#ff5470'), 'C_BG': col.get('fondo', '#0b0b12'), 'FONT_TEXT': fon['texto'], 'FONT_HEAD': fon['titulares'],
     'HEAD_CASE': fon.get('titulares_mayusculas', 'none'), 'LOGO': pathlib.Path(M['logo']).name}
html = (R/'src/template.html').read_text().replace('__VIDEOS__', '\n  '.join(html_v)).replace('__INSERTOS__', '\n  '.join(ins_html)).replace('__FONDOS__', fondos_html)
for k in sorted(D, key=len, reverse=True): html = html.replace(f'__{k}__', D[k])
html = html.replace('/*__CAPS__*/[]', json.dumps(caps, ensure_ascii=False)).replace('/*__T__*/{}', json.dumps(T, ensure_ascii=False))
left = re.findall(r'__[A-Z0-9_]+__', html); assert not left, left
(R/'film/index.html').write_text(html)
for k in ('texto', 'titulares'): shutil.copy(ROOT/'marca/fuentes'/fon[k], R/'film/assets/fonts'/fon[k]) if (ROOT/'marca/fuentes'/fon[k]).exists() else None
logo = (ROOT/M['logo']) if (ROOT/M['logo']).exists() else R/M['logo']
if logo.exists(): shutil.copy(logo, IMG/logo.name)
scenes[-1][2] = 'CTA'
json.dump({'S': {'END': END, 'CTA': CTA, 'cuts': cuts, 'insertos': [b[0] for b in busy]}, 'vids': items, 'dur': DUR, 'scenes': scenes}, open(R/'film/timeline.json', 'w'), indent=1)
json.dump(caps, open(R/'film/caps.json', 'w'), ensure_ascii=False)
print(f'ok film/index.html · {len(caps)} subtítulos · {DUR} s · escenas: ' + ' | '.join(f'{a:.1f} {n}' for a, b, n in scenes))
for w in warn: print(w)
