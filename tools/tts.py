"""Eleven v4 TTS with char timestamps. usage: tts.py VOICE_ID script.txt out.json STABILITY [STYLE]
Writes out.json (audio_base64 + alignment) and out.mp3. Make 2-3 takes (stability 0.30/0.40/0.45) and keep the one Scribe reads exactly
and tools/pace.py passes. Ad pace comes from GENERATION, never post-processing (docs/REGLAS.md): the rhythm tag below is prepended
unless the text already starts with a rhythm tag. NO_RITMO=1 disables it.
"IA" is always said Í-A (stress on the I, pronunciation rule): every standalone "IA" is sent as "ía" (Scribe still writes "IA", captions unchanged)."""
import json, os, re, sys, base64, urllib.request, _keys
RITMO = '[very fast-paced social media ad, quick and direct, no long pauses]'
IA = 'ía'                                   # pronunciación Í-A (docs/REGLAS.md)
vid, script, out, stab = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]); style = float(sys.argv[5]) if len(sys.argv) > 5 else 0.0
text = open(script).read().strip()
if not os.environ.get("NO_RITMO") and not text.lower().startswith(("[ritmo", "[very fast")): text = f"{RITMO} {text}"
if os.environ.get("TTS_LANG", "es") == "es": text = re.sub(r'\bIA\b', IA, text)
body = {"text": text, "model_id": "eleven_v4", "language_code": os.environ.get("TTS_LANG", "es"),
        "voice_settings": {"stability": stab, "similarity_boost": 0.75, "style": style, "use_speaker_boost": True}}
req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{vid}/with-timestamps?output_format=mp3_44100_192",
      data=json.dumps(body).encode(), headers={"xi-api-key": _keys.eleven(), "Content-Type": "application/json"})
d = json.load(urllib.request.urlopen(req, timeout=300)); json.dump(d, open(out, 'w'))
open(out.replace('.json', '.mp3'), 'wb').write(base64.b64decode(d['audio_base64'])); print('ok', out)
