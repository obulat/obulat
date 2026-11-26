# Voices for Element Explorer

The app picks a voice for every name and sentence in this order:

1. **Your own recording** (Grown-ups panel → Recording mode). Kept on that device only.
2. **The voice pack**: MP3 files in `audio/`, listed in `audio/manifest.json`.
3. **The Claude voice**, where the page runs inside Claude and the option is on.
4. **The device voice** (Web Speech API), as a fallback.

Device voices for Russian and Turkish are weak on iPad, and Safari often hides
downloaded "Enhanced" voices from web pages. So the voice pack is the best fix.

## Make a voice pack on your Mac (about 10 minutes)

```sh
cd element-explorer
brew install ffmpeg            # only needed for the say / piper engines
python3 -m venv .venv && source .venv/bin/activate
pip install edge-tts
node tools/export_texts.mjs    # writes tools/texts.json (1,035 texts)
python3 tools/make_voice_pack.py --engine edge
sh tools/build.sh              # rebuilds index.html
```

This writes about 1,000 small MP3s, roughly 15–25 MB in total. To start smaller,
add `--kinds name,home` for just the element names and home words.

### Which engine?

| Engine | Quality (ru / tr) | Cost and setup | Notes |
|---|---|---|---|
| `edge` (Microsoft neural: Svetlana, Emel, Ana) | Best of the free options | Free, `pip install edge-tts` | Unofficial endpoint. Fine for family use; it sometimes fails, so just rerun it (finished files are skipped). |
| `say` (macOS: Milena, Yelda) | OK, a bit robotic | Nothing to install | Download better versions first in System Settings → Accessibility → Spoken Content → System Voice → Manage Voices. |
| `piper` (Irina, Fahrettin) | OK | `pip install piper-tts` and download the models into `piper-models/` | Fully offline, open source. |

Other voices: `--voice ru=ru-RU-DmitryNeural --voice tr=tr-TR-AhmetNeural` (male voices).
If you want a legitimately licensed version of the same Microsoft voices, the
Azure Speech free tier (500,000 characters a month) covers this pack many times over.

For a **cloned family voice**, Chatterbox Multilingual (MIT licence, supports
Russian and Turkish) can learn a voice from a short sample. It needs more Python
setup and isn't wired into the script yet.

### Russian stress

Neural voices sometimes put stress on the wrong syllable. Listen to the names, and
put fixes in `tools/overrides.json` with an acute accent (U+0301) after the vowel:

```json
{ "name/ru/8": "Кислоро́д" }
```

Then run the script again with `--force --kinds name --langs ru`.

## Record your own voice

Open the standalone app (`index.html`, from a web address or as a file), go to
Grown-ups → Voices → Recording mode, open an element and tap **Record name** or
**Record fact**. Recordings stay in that browser on that device and take priority
over everything else. In the published Claude page, recording isn't available
because the page can't use the microphone.

## Use it offline on the iPad

Host the `element-explorer` folder anywhere with HTTPS (for example GitHub Pages),
open it in Safari, then Share → Add to Home Screen. The app caches itself, and
Grown-ups → "Save voices for offline use" downloads the whole voice pack.
