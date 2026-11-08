"""Música (ElevenLabs Music) y SFX (Sound Effects) del anuncio. Se piden EN SERIE (en paralelo dan 429).
usage: sonido.py <proyecto> [music] [sfx] [--dur=45] [--musica="descripción de la música"]
La música va muy baja en la mezcla (≈ 19 dB bajo la voz): pide algo épico/enérgico con poca melodía en los tramos con voz."""
import json, sys, pathlib, urllib.request
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); import _keys
args = [a for a in sys.argv[1:] if a not in ('music', 'sfx')]
if not args: sys.exit(__doc__)
T = pathlib.Path(__file__).resolve().parent
R = (T.parent/'proyectos'/args[0]) if not pathlib.Path(args[0]).exists() else pathlib.Path(args[0]).resolve()
(R/'audio/sfx').mkdir(parents=True, exist_ok=True)
DUR = float(next((a.split('=')[1] for a in sys.argv if a.startswith('--dur=')), 45))
MUSIC_PROMPT = next((a.split('=', 1)[1] for a in sys.argv if a.startswith('--musica=')), None)
H = {'xi-api-key': _keys.eleven(), 'Content-Type': 'application/json'}
def post(url, body, out):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=H)
    open(out, 'wb').write(urllib.request.urlopen(req, timeout=600).read()); print('ok', out)

MUSIC = MUSIC_PROMPT or (f"Instrumental epic and energetic background music for a {int(DUR)}-second vertical video ad, 110 BPM, cinematic modern percussion "
         "and pulsing synths, no vocals, steady intensity without big melodic lines so a voice-over sits on top, short riser before the final third, clean ending.")
SFX = {'whoosh': ('fast cinematic whoosh transition, clean', 0.8), 'whooshsoft': ('soft airy swoosh, UI card sliding in', 0.6),
       'pop': ('short soft UI pop, bubbly', 0.5), 'ping': ('smartphone message notification ping, short', 0.6),
       'blip': ('short negative UI alert blip, subtle', 0.5), 'impact': ('deep cinematic impact hit, short, punchy', 1.0), 'rise': ('gentle rising chime, positive progress', 1.5),
       'sparkle': ('magical sparkle shimmer, short', 1.0), 'cierre': ('elegant cinematic ending: single low piano note with soft string pad and a subtle deep boom, sophisticated, premium brand logo reveal', 3.0)}
if 'music' in sys.argv:
    post('https://api.elevenlabs.io/v1/music', {'prompt': MUSIC, 'music_length_ms': int(DUR * 1000), 'model_id': 'music_v1'}, R/'audio/music.mp3')
if 'sfx' in sys.argv:
    for k, (p, d) in SFX.items():
        if (R/f'audio/sfx/{k}.mp3').exists() and (R/f'audio/sfx/{k}.mp3').stat().st_size > 0: continue
        post('https://api.elevenlabs.io/v1/sound-generation', {'text': p, 'duration_seconds': d, 'prompt_influence': 0.6}, R/f'audio/sfx/{k}.mp3')
