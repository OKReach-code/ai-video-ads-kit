"""Kling audio_1 references: 0.25 s lead + the exact phrase (cut before the next word's onset) + silence up to whole seconds (>= 5).
usage: make_refs.py vo.wav vo_words.json shots.json outdir
shots.json = {"A": ["FirstWord", "lastword,", 6, 0.0], ...}  (first word, last word as Scribe writes them, clip seconds, search from VO second)
Writes outdir/ref_<K>.wav and outdir/segs.json (vo_a/vo_b = where the phrase sits in the VO, fill = speech share; aim for 80-93 %)."""
import json, subprocess, sys, pathlib, numpy as np
vo, wj, sj, od = sys.argv[1:5]; od = pathlib.Path(od); od.mkdir(parents=True, exist_ok=True)
SR = 48000; LEAD = 0.25
w = json.load(open(wj)); SH = json.load(open(sj))
x = np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',vo,'-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout, np.float32)
T = len(x)/SR; segs = {}
for k, (fw, lw, dur, tmin) in SH.items():
    i0 = next(i for i in range(len(w)) if w[i][2] == fw and w[i][0] >= tmin)
    i1 = next(i for i in range(i0, len(w)) if w[i][2] == lw)
    a = max(0, w[i0][0] - 0.08)
    if i0 > 0: a = max(a, w[i0-1][1] + 0.03)
    nxt = w[i1+1][0] if i1+1 < len(w) else T
    b = min(w[i1][1] + 0.2, nxt - 0.06, T)
    seg = x[int(a*SR):int(b*SR)].copy(); fl = int(.012*SR); seg[:fl] *= np.linspace(0,1,fl); seg[-fl:] *= np.linspace(1,0,fl)
    assert LEAD + len(seg)/SR <= dur - 0.15, (k, 'phrase too long for', dur, 's:', round(LEAD + len(seg)/SR, 2))
    buf = np.zeros(int(dur*SR), np.float32); buf[int(LEAD*SR):int(LEAD*SR)+len(seg)] = seg
    subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ar',str(SR),'-ac','1','-i','-','-c:a','pcm_s16le',str(od/f'ref_{k}.wav')], input=buf.tobytes(), check=True)
    segs[k] = {'vo_a': round(a,3), 'vo_b': round(b,3), 'lead': LEAD, 'duration': dur, 'fill': round(len(seg)/SR/dur,2), 'text': ' '.join(z[2] for z in w[i0:i1+1])}
    print(k, segs[k])
json.dump(segs, open(od/'segs.json','w'), ensure_ascii=False, indent=1)
print('total', sum(s['duration'] for s in segs.values()), 's of Kling')
