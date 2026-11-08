"""Bloques de subtítulos por SINTAGMAS para la plantilla de HyperFrames (docs/REGLAS.md): cada frase corta con sentido sale entera en una
misma pantalla, para que se entienda sin audio («¿Y qué milagro buscas?», «Quiero miles de alumnos», «y que no dependa todo de mí»).
- Se corta en la puntuación (. , ; : ? !) y en las pausas de más de HARD s (cambio de frase o de plano: la transcripción no siempre pone el punto).
  Una pausa corta (GAP–HARD s) solo corta si lo que queda no cabe en un bloque; si cabe, la frase sigue junta («les va a quitar el trabajo»).
- Si un trozo pasa de MAXW palabras o MAXC caracteres, se parte por el nexo más equilibrado (que, y, o, para, porque, pero, como, cuando, sin, con
  o un gerundio), nunca justo después de un artículo, preposición o nexo («y que», «para que», «va a quitar» van juntos) y nunca dejando una palabra sola.
- Cada bloque aparece entero de una vez (sin karaoke palabra a palabra), LEAD s antes de su primera palabra (sin pisar el final del bloque
  anterior), y se va cuando entra el siguiente (máx. 0,5 s después de la última palabra).
Uso como módulo: from captions import phrase_blocks · CLI: captions.py vo_words.json offset_P highlights.txt out_caps.json"""
import json, re, sys
MAXW, MAXC, GAP, HARD, LEAD = 8, 40, 0.35, 0.6, 0.3
NEXOS = {'que', 'y', 'e', 'o', 'u', 'para', 'porque', 'pero', 'como', 'cuando', 'sin', 'con', 'aunque', 'mientras', 'donde', 'desde', 'hasta', 'cuál', 'qué', 'quién', 'dónde', 'cómo', 'cuándo', 'cuánto'}
FUNC = NEXOS | {'a', 'al', 'de', 'del', 'en', 'por', 'el', 'la', 'los', 'las', 'lo', 'le', 'les', 'se', 'un', 'una', 'unos', 'unas', 'mi', 'tu', 'su', 'sus',
                'mis', 'tus', 'muy', 'más', 'no', 'va', 'van', 'es', 'cada', 'este', 'esta', 'estos', 'estas', 'ese', 'esa', 'esos', 'esas', 'tu', 'nuestro', 'nuestra'}   # palabras tras las que nunca se corta (la frase quedaría colgando)
norm = lambda w: re.sub(r'[^\wáéíóúñü]', '', w.lower())

def _len(ws): return len(' '.join(w['t'] for w in ws))

def _split(ws):
    if len(ws) <= MAXW and _len(ws) <= MAXC: return [ws]
    cand = []
    for i in range(2, len(ws) - 1):                       # nunca una palabra sola a un lado
        a, prev = norm(ws[i]['t']), norm(ws[i - 1]['t'])
        if (a in NEXOS or a.endswith('ndo')) and prev not in FUNC: cand.append(i)
    if not cand: cand = [i for i in range(2, len(ws) - 1) if norm(ws[i]['t']) in FUNC - {'de', 'del', 'a', 'al'} and norm(ws[i - 1]['t']) not in FUNC]   # antes de un artículo o preposición («de» y «a» suelen ir con lo anterior)
    if not cand: cand = [i for i in range(2, len(ws) - 1) if norm(ws[i - 1]['t']) not in FUNC] or [len(ws) // 2]
    i = min(cand, key=lambda i: abs(_len(ws[:i]) - _len(ws[i:])))
    return _split(ws[:i]) + _split(ws[i:])

def phrase_blocks(words, P, HL=frozenset(), AST=frozenset()):
    """words = [[ini, fin, texto], ...] (segundos de locución) -> [{'s','e','x','w':[{'t','s','e','hl','ast'}]}] en segundos de película (+P).
    HL: palabras resaltadas en color · AST: palabras en la fuente de titulares (en vez de repetirlas en un rótulo aparte: docs/REGLAS.md)."""
    chunks, cur = [], []                                  # [(palabras, corte_blando)]
    for i, (s, e, t) in enumerate(words):
        cur.append({'t': t, 's': round(s + P, 3), 'e': round(e + P, 3), 'hl': norm(t) in HL, 'ast': norm(t) in AST})
        gap = (words[i + 1][0] - e) if i + 1 < len(words) else 9
        if t[-1] in '.,;:?!' or gap > HARD: chunks.append((cur, False)); cur = []
        elif gap > GAP and norm(t) not in FUNC and len(cur) >= 2: chunks.append((cur, True)); cur = []   # pausa corta: corte blando
    if cur: chunks.append((cur, False))
    merged = []
    for ws, soft in chunks:                                # los cortes blandos se deshacen si la frase cabe junta
        nexo = norm(ws[0]['t']) in NEXOS and len(merged[-1][0]) >= 3 if merged else False   # «dónde se atascan | y usan…»
        if merged and merged[-1][1] and not nexo and len(merged[-1][0]) + len(ws) <= MAXW and _len(merged[-1][0] + ws) <= MAXC:
            merged[-1] = (merged[-1][0] + ws, soft)
        else: merged.append((ws, soft))
    chunks = [ws for ws, _ in merged]
    out = [b for c in chunks for b in _split(c)]
    caps = [{'s': round(c[0]['s'] - LEAD, 3), 'e': c[-1]['e'], 'w': c} for c in out]
    for a, b in zip(caps, caps[1:]): b['s'] = round(max(b['s'], a['e'] + 0.05), 3)       # entra antes, pero no pisa la frase anterior
    caps[0]['s'] = max(0.0, caps[0]['s'])
    for a, b in zip(caps, caps[1:]): a['x'] = min(b['s'], round(a['e'] + 0.5, 3))
    caps[-1]['x'] = round(caps[-1]['e'] + 0.5, 3)
    return caps

if __name__ == '__main__':
    words, P = json.load(open(sys.argv[1])), float(sys.argv[2])
    HL = {l.strip().lower() for l in open(sys.argv[3]) if l.strip()}
    caps = phrase_blocks(words, P, HL)
    json.dump(caps, open(sys.argv[4], 'w'), ensure_ascii=False)
    for c in caps: print(f"{c['s']:6.2f}  {' '.join(w['t'] for w in c['w'])}")

# ---- Números en cifras (regla de calidad): en subtítulos y rótulos los números van SIEMPRE en cifras («50», «5.000», «40 %»).
_U = {'cero': 0, 'uno': 1, 'una': 1, 'un': 1, 'dos': 2, 'tres': 3, 'cuatro': 4, 'cinco': 5, 'seis': 6, 'siete': 7, 'ocho': 8, 'nueve': 9, 'diez': 10,
      'once': 11, 'doce': 12, 'trece': 13, 'catorce': 14, 'quince': 15, 'dieciséis': 16, 'diecisiete': 17, 'dieciocho': 18, 'diecinueve': 19, 'veinte': 20,
      'veintiuno': 21, 'veintiún': 21, 'veintidós': 22, 'veintitrés': 23, 'veinticuatro': 24, 'veinticinco': 25, 'veintiséis': 26, 'veintisiete': 27,
      'veintiocho': 28, 'veintinueve': 29, 'treinta': 30, 'cuarenta': 40, 'cincuenta': 50, 'sesenta': 60, 'setenta': 70, 'ochenta': 80, 'noventa': 90,
      'cien': 100, 'ciento': 100, 'doscientos': 200, 'trescientos': 300, 'cuatrocientos': 400, 'quinientos': 500, 'seiscientos': 600,
      'setecientos': 700, 'ochocientos': 800, 'novecientos': 900}
_M = {'mil': 1000, 'millón': 10**6, 'millones': 10**6}
def _fmt(n): return f'{n:,}'.replace(',', '.') if n >= 1000 else str(n)
def numerals(blocks):
    """Reescribe en cada bloque las secuencias de números en letra como cifras (el tiempo es el de la primera palabra; el resto se quita).
    «un/una/uno» solo cuentan como número si van seguidos de mil/millón («una formación» se queda igual). «por ciento» → «%»."""
    for c in blocks:
        ws, out, i = c['w'], [], 0
        while i < len(ws):
            j, total, cur, seen = i, 0, 0, False
            while j < len(ws):
                t = norm(ws[j]['t'])
                if t in ('un', 'una', 'uno') and not (j + 1 < len(ws) and norm(ws[j + 1]['t']) in _M): break
                if t in _U: cur += _U[t]; seen = True
                elif t in _M and seen | (t == 'mil'): total += max(cur, 1) * _M[t]; cur = 0; seen = True
                elif t == 'y' and seen and j + 1 < len(ws) and norm(ws[j + 1]['t']) in _U: pass
                else: break
                j += 1
            if j > i and seen:
                n = total + cur; tail = re.sub(r'^[\wáéíóúñü]+', '', ws[j - 1]['t'])        # conserva la puntuación final («cincuenta,»)
                w = dict(ws[i], t=_fmt(n) + tail, e=ws[j - 1]['e'])
                if j + 1 < len(ws) and norm(ws[j]['t']) == 'por' and norm(ws[j + 1]['t']) == 'ciento':
                    w['t'] = _fmt(n) + ' %' + re.sub(r'^[\wáéíóúñü]+', '', ws[j + 1]['t']); w['e'] = ws[j + 1]['e']; j += 2
                out.append(w); i = j
            else: out.append(ws[i]); i += 1
        c['w'] = out
    return blocks
