"""Scribe (es, word timestamps). usage: scribe.py file [out_words.json]  -> prints text + gaps > 0.25 s
out_words.json = [[start, end, text], ...]: the format every other tool uses (subtitles, cuts, refs, QA)."""
import sys, json, subprocess, _keys
f = sys.argv[1]
r = subprocess.run(['curl','-s','-X','POST','https://api.elevenlabs.io/v1/speech-to-text','-H',f'xi-api-key: {_keys.eleven()}',
     '-F','model_id=scribe_v1','-F','language_code=es','-F','timestamps_granularity=word','-F',f'file=@{f}'],capture_output=True,text=True).stdout
d = json.loads(r); w = [x for x in d['words'] if x['type']=='word']
if len(sys.argv) > 2: json.dump([[x['start'],x['end'],x['text']] for x in w], open(sys.argv[2],'w'), ensure_ascii=False)
print(d['text'])
print('gaps:', ' '.join(f"{w[i]['end']:.2f}+{w[i+1]['start']-w[i]['end']:.2f}({w[i]['text']})" for i in range(len(w)-1) if w[i+1]['start']-w[i]['end']>0.25))
