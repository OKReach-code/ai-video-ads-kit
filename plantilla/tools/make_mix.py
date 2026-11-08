"""Escribe mix_premium.json con los efectos según film/timeline.json (ejecutar tras build.py) y luego: python3 ../../tools/mix.py mix_premium.json
Reglas (docs/REGLAS.md): golpe en el primer fotograma, impacto en cada cambio de escena, «pop» al entrar cada inserto, ningún efecto encima de
una sílaba (los whoosh solo en huecos sin voz), cierre al final; música comprimida ≈ 19 dB por debajo de la voz (mix.py lo mide)."""
import json, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
T = json.load(open(R/'film/timeline.json')); S = T['S']
have = lambda k: (R/f'audio/sfx/{k}.mp3').exists()
sfx = lambda k, t, g: [[f'audio/sfx/{k}.mp3', round(max(0, t), 2), g]] if have(k) else []
VW = [(a + 0.15, b + 0.15) for a, b, _ in json.load(open(R/'audio/vo_words_premium.json'))]
free = lambda t0, t1: not any(a < t1 and b > t0 for a, b in VW)
def gap(k, t, g, d=0.35):
    for i in range(9):
        if free(t - i * 0.05, t - i * 0.05 + d): return sfx(k, t - i * 0.05, g)
    return []
SFX = sfx('impact', 0.0, 0.38)
for t in S['cuts']: SFX += sfx('impact', t, 0.2) + gap('whoosh', t - 0.1, 0.25)
for t in S['insertos']: SFX += sfx('pop', t + 0.1, 0.15)
for c in json.load(open(R/'film/caps.json')):
    if c.get('kin'): SFX += gap('whooshsoft', c['w'][0]['s'] - 0.4, 0.14)
SFX += sfx('pop', S['CTA'] + 0.05, 0.16) + sfx('cierre', S['END'] + 0.1, 0.4)
SFX.sort(key=lambda x: x[1])
c = {'video': 'render/video_noaudio_premium.mp4', 'out': 'final_premium.mp4', 'dur': T['dur'], 'vo': 'audio/vo_premium.wav', 'vo_delay': 0.15,
     'music': 'audio/music.mp3', 'music_gain': 0.6, 'music_start': 0.0,
     'music_af': 'acompressor=threshold=-34dB:ratio=10:attack=40:release=350:makeup=1', 'sfx': SFX}
s = json.dumps(c, ensure_ascii=False)
open(R/'mix_premium.json', 'w').write(s.replace(', "sfx"', ',\n "sfx"').replace('], [', '],\n  [') + '\n')
print('ok mix_premium.json ·', len(SFX), 'efectos · dur', T['dur'])
