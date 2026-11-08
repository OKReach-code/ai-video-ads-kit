"""Sincroniza los planos de Kling con NUESTRA locución (Premium por defecto, docs/REGLAS.md): en el máster suena audio/vo.wav y los
planos entran mudos. Escribe audio/hybrid_premium.json = {B1..Bn: {a, b[, shot, c]}}: en los bloques con plano de persona, segundo del clip
= segundo de la locución + c, con c = lead − vo_a + desfase (kling/offsets.json, lo que mide tools/qa.py si el desfase es fijo).
Cada plano se asigna al bloque que contiene su frase (kling/refs/segs.json). Lo leen build.py (ms(k, t) = (t − P) + c) y la mezcla.
uso: tools/kling_sync.py <proyecto>"""
import json, sys, pathlib, shutil
T = pathlib.Path(__file__).resolve().parent
if len(sys.argv) < 2: sys.exit(__doc__)
R = (T.parent/'proyectos'/sys.argv[1]) if not pathlib.Path(sys.argv[1]).exists() else pathlib.Path(sys.argv[1]).resolve()
segs = json.load(open(R/'kling/refs/segs.json')); bl = json.load(open(R/'audio/bloques.json'))
off = json.load(open(R/'kling/offsets.json')) if (R/'kling/offsets.json').exists() else {}
H = {}
for k, sp, a, b, txt in bl:
    H[k] = {'a': a, 'b': b}
    for s, v in segs.items():
        if a - 0.3 <= v['vo_a'] + 0.1 <= b: H[k].update(shot=s, c=round(v['lead'] - v['vo_a'] + off.get(s, 0.0), 3))
for f in ('vo.wav', 'vo_words.json'):
    shutil.copy(R/'audio'/f, R/'audio'/f.replace('.', '_premium.', 1))
json.dump(H, open(R/'audio/hybrid_premium.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in H.items() if 'shot' in v}))
