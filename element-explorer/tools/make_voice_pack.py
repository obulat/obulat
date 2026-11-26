#!/usr/bin/env python3
"""Generate the Element Explorer voice pack: one MP3 per name, fact, molecule and home item.

  node tools/export_texts.mjs                    # 1. list the texts
  python3 tools/make_voice_pack.py --engine edge # 2. make audio/ (see VOICES.md)

Engines:
  edge   Microsoft neural voices through the free `edge-tts` package (pip install edge-tts).
         Most natural for Russian and Turkish. Unofficial endpoint, personal use only.
  say    macOS built-in voices (Milena/Yuri, Yelda/Cem). No install, more robotic.
  piper  Piper models on your Mac (pip install piper-tts; models in ./piper-models).
Needs ffmpeg for say/piper (brew install ffmpeg).

Options: --langs ru,tr,en   --kinds name,fact,sci,mol,home   --force (redo existing files)
Russian stress: put corrections in tools/overrides.json, e.g. {"name/ru/8": "Кислоро́д"}.
"""
import argparse, asyncio, json, os, re, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOICES = {
    'edge':  {'en': 'en-US-AnaNeural', 'ru': 'ru-RU-SvetlanaNeural', 'tr': 'tr-TR-EmelNeural'},
    'say':   {'en': 'Samantha', 'ru': 'Milena', 'tr': 'Yelda'},
    'piper': {'en': 'en_US-amy-medium', 'ru': 'ru_RU-irina-medium', 'tr': 'tr_TR-fahrettin-medium'},
}

def to_mp3(src, dst):
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', src, '-ac', '1', '-codec:a', 'libmp3lame', '-q:a', '5', dst], check=True)

async def edge(text, voice, dst, rate):
    import edge_tts
    for attempt in range(4):
        try:
            await edge_tts.Communicate(text, voice, rate=rate).save(dst); return
        except Exception as e:
            if attempt == 3: raise
            await asyncio.sleep(2 * (attempt + 1))

def say(text, voice, dst, rate):
    with tempfile.TemporaryDirectory() as d:
        aiff = os.path.join(d, 'a.aiff')
        subprocess.run(['say', '-v', voice, '-r', str(rate), '-o', aiff, text], check=True)
        to_mp3(aiff, dst)

def piper(text, voice, dst, rate):
    model = os.path.join(ROOT, 'piper-models', voice + '.onnx')
    with tempfile.TemporaryDirectory() as d:
        wav = os.path.join(d, 'a.wav')
        subprocess.run([sys.executable, '-m', 'piper', '-m', model, '--length-scale', str(rate), '-f', wav, '--', text], check=True)
        to_mp3(wav, dst)

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--engine', choices=VOICES, default='edge')
    ap.add_argument('--langs', default='ru,tr,en')
    ap.add_argument('--kinds', default='name,fact,sci,mol,home')
    ap.add_argument('--voice', action='append', default=[], help='override, e.g. --voice ru=ru-RU-DmitryNeural')
    ap.add_argument('--force', action='store_true')
    a = ap.parse_args()
    texts = json.load(open(os.path.join(ROOT, 'tools', 'texts.json'), encoding='utf8'))
    ov = os.path.join(ROOT, 'tools', 'overrides.json')
    if os.path.exists(ov): texts.update(json.load(open(ov, encoding='utf8')))
    voices = dict(VOICES[a.engine]); voices.update(dict(v.split('=', 1) for v in a.voice))
    langs, kinds = a.langs.split(','), a.kinds.split(',')
    man_path = os.path.join(ROOT, 'audio', 'manifest.json')
    manifest = json.load(open(man_path)) if os.path.exists(man_path) else {}
    todo = [(k, t) for k, t in texts.items() if k.split('/')[1] in langs and k.split('/')[0] in kinds]
    print(f'{len(todo)} clips with engine {a.engine}')
    for i, (key, text) in enumerate(todo, 1):
        kind, lang, ident = key.split('/')
        rel = f"{lang}/{kind}-{re.sub(r'[^A-Za-z0-9]', '_', ident)}.mp3"
        dst = os.path.join(ROOT, 'audio', rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if a.force or not os.path.exists(dst):
            short = kind in ('name', 'home')   # single words: a little slower for young readers
            if a.engine == 'edge': asyncio.run(edge(text, voices[lang], dst, '-15%' if short else '-5%'))
            elif a.engine == 'say': say(text, voices[lang], dst, 140 if short else 165)
            else: piper(text, voices[lang], dst, 1.2 if short else 1.05)
        manifest[key] = rel
        if i % 25 == 0 or i == len(todo):
            json.dump(manifest, open(man_path, 'w'), ensure_ascii=False, indent=0)
            print(f'  {i}/{len(todo)}')
    print('Done. Run tools/build.sh, then open index.html.')

if __name__ == '__main__':
    main()
