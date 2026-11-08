"""API keys: env var first, then the repo's .env, then a key file (keys/elevenlabs.txt, keys/openrouter.txt). Never commit keys."""
import os, re, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
def _env(name):
    if os.environ.get(name): return os.environ[name]
    f = ROOT/'.env'
    if f.exists():
        for l in f.read_text().splitlines():
            if l.strip().startswith(name + '='): return l.split('=', 1)[1].strip().strip('"\'')
    return None
def eleven():
    k = _env('ELEVENLABS_API_KEY') or (ROOT/'keys/elevenlabs.txt').read_text()
    return k.split()[-1]
def openrouter():
    k = _env('OPENROUTER_API_KEY') or (ROOT/'keys/openrouter.txt').read_text()
    return re.search(r'sk-or-[\w-]+', k).group(0)
