"""Ad pace check (docs/REGLAS.md): is the voice and the edit as fast as the winning reference ads?
usage: pace.py words.json [video.mp4]          words.json = [[start, end, text], ...] (Scribe of the FINAL voice: vo_words*.json)
Voice thresholds, measured on the winning ads (6.8-6.9 syllables/s, longest pause 0.4-0.5 s, pauses ~6 % of the time):
  syllables/s >= 6.4 · no gap > 0.6 s · pauses > 0.25 s <= 9 % of the time. words/s is shown but depends on the text (long words).
Video (optional, WARNING only: the winning ads keep long talking-head stretches up to ~12 s): average visual change every <= 3.5 s and
no stretch > 6 s without a cut, punch-in or card -> reported as AVISO so you can add a punch-in or an insert there.
Exit code 1 if any check fails -> regenerate the take (rhythm tag, voice, script without '…'). NEVER speed it up or stretch it: docs/REGLAS.md"""
import json, re, subprocess, sys
def syl(w):
    w = re.sub(r'[^a-záéíóúüñ]', '', w.lower())
    return max(1, len(re.findall(r'[aeoáéíóú]+[iuy]?|[iuü]+[aeoáéíóú]?', w))) if w else 0
_U = 'cero uno dos tres cuatro cinco seis siete ocho nueve diez once doce trece catorce quince dieciséis diecisiete dieciocho diecinueve'.split()
_D = 'veinte treinta cuarenta cincuenta sesenta setenta ochenta noventa'.split()
_C = 'cien doscientos trescientos cuatrocientos quinientos seiscientos setecientos ochocientos novecientos'.split()
def _say(n):   # Spanish words for 0..999999 (only to count syllables of numbers Scribe writes as digits)
    if n < 20: return _U[n]
    if n < 30: return 'veinti' + _U[n - 20] if n > 20 else 'veinte'
    if n < 100: return _D[n // 10 - 2] + ('' if n % 10 == 0 else ' y ' + _U[n % 10])
    if n < 1000: return ('cien' if n == 100 else ('ciento' if n < 200 else _C[n // 100 - 1])) + ('' if n % 100 == 0 else ' ' + _say(n % 100))
    return ('mil' if n < 2000 else _say(n // 1000) + ' mil') + ('' if n % 1000 == 0 else ' ' + _say(n % 1000))
class _Num(dict):   # Scribe writes some numbers as digits ("90%", "5.000"): count them as they are said
    def get(self, k, d=None):
        if k.strip() == '%': return 'por ciento'
        m = re.fullmatch(r'(\d[\d.]*)(%?)', k.replace(' ', ''))
        if not m: return d
        return _say(int(m.group(1).replace('.', ''))) + (' por ciento' if m.group(2) else '')
NUM = _Num()
w = [x for x in json.load(open(sys.argv[1])) if re.search(r'[\w%]', x[2])]   # «%» suelto (Scribe: «70 %») cuenta como «por ciento», no como pausa
span = w[-1][1] - w[0][0]; gaps = [b[0] - a[1] for a, b in zip(w, w[1:])]
big = [g for g in gaps if g > 0.25]; long_ = [g for g in gaps if g > 0.6]
wps, sps, pshare = len(w) / span, sum(sum(syl(t) for t in NUM.get(x[2].strip('.,'), x[2]).split()) for x in w) / span, sum(big) / span
checks = [('sílabas/s', f'{sps:.2f}', '>= 6.4', sps >= 6.4),
          ('pausas > 0,6 s', ' '.join(f'{g:.2f}' for g in long_) or '0', 'ninguna', not long_),
          ('tiempo en pausas', f'{pshare * 100:.1f} %', '<= 9 %', pshare <= 0.09)]
if len(sys.argv) > 2:
    v = sys.argv[2]
    d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', v], capture_output=True, text=True).stdout)
    e = subprocess.run(['ffmpeg', '-nostats', '-i', v, '-an', '-vf', "scale=180:-2,select='gt(scene,0.08)',showinfo", '-f', 'null', '-'], capture_output=True, text=True).stderr
    t = sorted({round(float(x), 1) for x in re.findall(r'pts_time:([\d.]+)', e)}); t = [a for i, a in enumerate(t) if i == 0 or a - t[i - 1] > 0.4]
    T = [0] + t + [d]; L = [b - a for a, b in zip(T, T[1:])]; worst = max(range(len(L)), key=L.__getitem__)
    warn = [('cambio visual cada', f'{d / len(L):.2f} s', '<= 3,5 s', d / len(L) <= 3.5),
            ('tramo sin cambio más largo', f'{L[worst]:.1f} s (en {T[worst]:.1f} s)', '<= 6 s', L[worst] <= 6)]
for name, val, target, ok in checks: print(f"{'OK   ' if ok else 'FALLA'} {name:28s} {val:>22s}   objetivo {target}")
for name, val, target, ok in (warn if len(sys.argv) > 2 else []): print(f"{'OK   ' if ok else 'AVISO'} {name:28s} {val:>22s}   objetivo {target}")
print(f'voz {span:.1f} s · {len(w)} palabras · {wps:.2f} palabras/s (orientativo)' + ('' if all(c[3] for c in checks) else '  ->  RITMO LENTO: ver docs/REGLAS.md'))
sys.exit(0 if all(c[3] for c in checks) else 1)
