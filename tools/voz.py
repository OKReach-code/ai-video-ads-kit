"""Locución del anuncio con el RITMO DE ANUNCIO (docs/REGLAS.md, docs/REGLAS.md), sin ningún postprocesado de velocidad.
Lee proyectos/<p>/audio/guion.json, genera N tomas por bloque con Eleven v4 (tools/tts.py añade la etiqueta de ritmo y envía «IA» como «ía»),
transcribe cada toma con Scribe y se queda con la que se lee EXACTA y va más rápida sin pausas > 0,6 s. Cada bloque se usa tal cual sale
(solo se quita el silencio de antes y después); 0,05 s entre bloques.
  guion.json = {"voz": "<voice_id>", "idioma": "es", "stability": 0.3, "style": 0.15,
                "bloques": [["B1", "texto del guion…"], ["B2", "…"]]}     (un bloque = una frase del guion / un plano)
  Las etiquetas de tono [entre corchetes] y los «…» frenan el ritmo: se quitan («…» → coma) salvo con --literal. Nunca se cambian palabras.
uso: tools/voz.py <proyecto> [N=3] [--literal]
sale: audio/vo.wav · audio/vo_words.json · audio/bloques.json · audio/medidas.json (+ copias *_premium, que leen build.py y mix)
      y el veredicto de tools/pace.py (≥ 6,4 síl/s, sin pausas > 0,6 s, ≤ 9 % de silencio). Si falla: regenerar (más tomas), nunca acelerar."""
import json, subprocess, sys, pathlib, re, shutil, types
T = pathlib.Path(__file__).resolve().parent; PY = sys.executable
args = [a for a in sys.argv[1:] if not a.startswith('--')]; LITERAL = '--literal' in sys.argv
if not args: sys.exit(__doc__)
R = (T.parent/'proyectos'/args[0]) if not pathlib.Path(args[0]).exists() else pathlib.Path(args[0]).resolve()
N = int(args[1]) if len(args) > 1 else 3
G = json.load(open(R/'audio/guion.json'))
import os; os.environ['TTS_LANG'] = G.get('idioma', 'es')
V, STAB, STYLE, GAP = G['voz'], str(G.get('stability', 0.3)), str(G.get('style', 0.15)), 0.05
B = [(k, t if LITERAL else re.sub(r'\[[^\]]*\] ?', '', t).replace('… ', ', ').replace('…', ',').strip()) for k, t in G['bloques']]
D = R/'audio/tomas'; D.mkdir(parents=True, exist_ok=True)
_src = open(T/'pace.py').read(); _src = _src[_src.index("_U = "):_src.index("NUM = _Num()") + len("NUM = _Num()")]
_m = types.ModuleType('_num'); _m.re = re; exec(_src, _m.__dict__); NUM = _m.NUM          # cifras de Scribe («70 %», «5.000») → como se dicen
norm = lambda s: re.sub(r'[^\wáéíóúñü ]', '', re.sub(r'\[[^\]]*\]', '', s).lower()).split()
def syl(w):
    w = re.sub(r'[^a-záéíóúüñ]', '', w.lower()); return max(1, len(re.findall(r'[aeoáéíóú]+[iuy]?|[iuü]+[aeoáéíóú]?', w))) if w else 0
def measure(w):
    span = w[-1][1] - w[0][0]; s = sum(sum(syl(t) for t in NUM.get(x[2].strip('.,¿?'), x[2]).split()) for x in w)
    gaps = [b[0] - a[1] for a, b in zip(w, w[1:])] or [0]
    return dict(sps=round(s / span, 2), pausa_max=round(max(gaps), 2), pausas=round(sum(g for g in gaps if g > .25) / span * 100, 1), dur=round(span, 2))
words, bl, parts, med, t = [], [], [], {}, 0.0
for k, txt in B:
    takes = []
    for i in range(1, N + 1):
        f = D/f'{k}_t{i}'; (D/f'{k}.txt').write_text(txt)
        if not f.with_suffix('.json').exists():
            subprocess.run([PY, T/'tts.py', V, D/f'{k}.txt', f.with_suffix('.json'), STAB, STYLE], check=True, cwd=T, capture_output=True)
        wav, wj = f.with_suffix('.wav'), D/f'{k}_t{i}_words.json'
        if not wav.exists(): subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f.with_suffix('.mp3'), '-ac', '1', '-ar', '48000', wav], check=True)
        if not wj.exists(): subprocess.run([PY, T/'scribe.py', wav, wj], check=True, capture_output=True, cwd=T)
        w = json.load(open(wj))
        said = norm(' '.join(NUM.get(x[2].strip('.,¿?'), x[2]) for x in w))
        takes.append(dict(i=i, wav=wav, w=w, exact=said == norm(txt), **measure(w)))
    ok = [x for x in takes if x['exact']] or takes
    best = max(ok, key=lambda x: (x['pausa_max'] <= 0.6, x['sps']))
    med[k] = [{kk: v for kk, v in x.items() if kk not in ('wav', 'w')} | {'elegida': x is best} for x in takes]
    w = best['w']; a0, a1 = w[0][0], w[-1][1]; s0 = max(0, a0 - 0.05); t += GAP if bl else 0
    parts.append((best['wav'], s0, a1 + 0.12 - s0, t))
    end = txt.rstrip()[-1] if txt.rstrip()[-1] in '.?!,;:' else ''
    w = [list(x) for x in w]
    if end and w[-1][2][-1] not in '.?!,;:': w[-1][2] += end     # la última palabra lleva la puntuación del guion: el subtítulo corta en el cambio de bloque
    words += [[round(t + x[0] - s0, 3), round(t + x[1] - s0, 3), x[2]] for x in w]
    bl.append([k, 'D', round(t + a0 - s0, 3), round(t + a1 - s0, 3), txt]); t += a1 + 0.12 - s0
    print(k, ' · '.join(f"t{x['i']} {'EXACTA' if x['exact'] else 'NO EXACTA'} {x['sps']} síl/s pausa máx {x['pausa_max']}s" for x in takes), '→ t', best['i'])
inp, fc = [], []
for i, (f, s0, d, at) in enumerate(parts):
    inp += ['-i', str(f)]; fc.append(f'[{i}:a]aresample=48000,atrim={s0:.3f}:{s0 + d:.3f},asetpts=PTS-STARTPTS,afade=t=out:st={max(0, d - 0.03):.3f}:d=0.03,adelay={int(at * 1000)}:all=1[a{i}]')
fc.append(''.join(f'[a{i}]' for i in range(len(parts))) + f'amix=inputs={len(parts)}:normalize=0,atrim=0:{t + 0.3:.3f}[out]')
A = R/'audio'
subprocess.run(['ffmpeg', '-v', 'error', '-y', *inp, '-filter_complex', ';'.join(fc), '-map', '[out]', '-ac', '1', '-ar', '48000', str(A/'vo.wav')], check=True)
json.dump(words, open(A/'vo_words.json', 'w'), ensure_ascii=False); json.dump(bl, open(A/'bloques.json', 'w'), ensure_ascii=False, indent=1)
json.dump(med, open(A/'medidas.json', 'w'), ensure_ascii=False, indent=1)
shutil.copy(A/'vo.wav', A/'vo_premium.wav'); shutil.copy(A/'vo_words.json', A/'vo_words_premium.json')
print(f'ok {A/"vo.wav"} · {t:.2f} s')
subprocess.run([PY, T/'pace.py', A/'vo_words.json'])
