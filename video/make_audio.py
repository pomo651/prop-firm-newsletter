"""TTS per segment (edge-tts, word timings) -> voice.wav + timeline.json; synth music -> music.wav; mix -> mix.wav"""
import asyncio, json, subprocess, re, sys, os, wave
import numpy as np
import edge_tts
HERE = os.path.dirname(os.path.abspath(__file__)); B = os.path.join(HERE, "build"); os.makedirs(B, exist_ok=True)
ep = json.load(open(os.path.join(HERE, "episode.json")))
SR = 48000; GAP = 0.45; LEAD = 0.25
segs = [("hook", ep["hook"]["say"])] + [(f"item{i+1}", it["say"]) for i, it in enumerate(ep["items"])] + [("outro", ep["outro"]["say"])]

async def tts(text, path):
    cache = path + ".words.json"
    if os.path.exists(cache) and os.path.exists(path) and json.load(open(cache))["text"] == text + ep["voice"] + ep["rate"]:
        return [tuple(w) for w in json.load(open(cache))["words"]]
    w = await _tts(text, path)
    json.dump({"text": text + ep["voice"] + ep["rate"], "words": w}, open(cache, "w"))
    return w

async def _tts(text, path):
    for attempt in range(10):
        try:
            c = edge_tts.Communicate(text, ep["voice"], rate=ep["rate"], boundary="WordBoundary")
            words = []
            with open(path, "wb") as f:
                async for ch in c.stream():
                    if ch["type"] == "audio": f.write(ch["data"])
                    elif ch["type"] == "WordBoundary": words.append((ch["offset"]/1e7, (ch["offset"]+ch["duration"])/1e7, ch["text"]))
            return words
        except Exception as ex:
            print("retry", attempt, ex); await asyncio.sleep(3 + attempt*2)
    raise SystemExit("TTS failed")

def to_pcm(mp3):
    raw = subprocess.run(["ffmpeg","-v","error","-i",mp3,"-ac","1","-ar",str(SR),"-f","s16le","-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.int16).astype(np.float32)/32768

def phrases(text, words, t0):
    """Map word boundaries back onto the script text, then cut caption phrases."""
    pos, cur = [], 0
    for (s, e, w) in words:
        first = w.split()[0]
        i = text.find(first, cur)
        if i < 0: i = cur
        pos.append(i); cur = i + len(first)
    # tokens of script text with char index
    toks = [(m.start(), m.group()) for m in re.finditer(r"\S+", text)]
    def time_at(ci):
        best = None
        for k, p in enumerate(pos):
            if p <= ci: best = k
        return words[best][0] if best is not None else words[0][0]
    out, chunk, start_ci = [], [], None
    for k, (ci, tok) in enumerate(toks):
        if not chunk: start_ci = ci
        chunk.append(tok)
        txt = " ".join(chunk)
        brk = tok[-1] in ".,:;!?" or len(txt) >= 22 or k == len(toks)-1
        if len(txt) < 9 and k != len(toks)-1 and tok[-1] not in ".:!?": brk = False
        if brk:
            out.append({"text": txt.rstrip(",;"), "start": round(t0 + time_at(start_ci), 3)}); chunk = []
    # merge orphan fragments (e.g. "links.") into the previous caption
    merged = []
    for c in out:
        if merged and len(c["text"]) < 9 and not merged[-1]["text"].endswith((".", "!", "?", ":")) and len(merged[-1]["text"]) + len(c["text"]) <= 32:
            merged[-1]["text"] += " " + c["text"]
        else:
            merged.append(c)
    return merged

async def main():
    timeline, voice, t = {"segments": [], "captions": []}, [], LEAD
    voice.append(np.zeros(int(LEAD*SR), np.float32))
    for name, text in segs:
        mp3 = os.path.join(B, f"{name}.mp3")
        words = await tts(text, mp3)
        pcm = to_pcm(mp3); dur = len(pcm)/SR
        caps = phrases(text, words, t)
        last_end = t + words[-1][1]
        for j, c in enumerate(caps):
            c["end"] = round(caps[j+1]["start"] if j+1 < len(caps) else last_end + 0.25, 3)
        timeline["captions"] += caps
        timeline["segments"].append({"name": name, "start": round(t,3), "end": round(t+dur+GAP,3)})
        voice += [pcm, np.zeros(int(GAP*SR), np.float32)]
        t += dur + GAP
    tail = 1.2
    voice.append(np.zeros(int(tail*SR), np.float32)); t += tail
    timeline["segments"][-1]["end"] = round(t, 3)
    timeline["duration"] = round(t, 3)
    v = np.concatenate(voice)
    json.dump(timeline, open(os.path.join(B, "timeline.json"), "w"), indent=1)
    write_wav(os.path.join(B, "voice.wav"), v)
    m = music(len(v)/SR)
    write_wav(os.path.join(B, "music.wav"), m)
    # duck music under voice with sidechain compression, then mix and normalise
    subprocess.run(["ffmpeg","-v","error","-y","-i",os.path.join(B,"voice.wav"),"-i",os.path.join(B,"music.wav"),"-filter_complex",
        "[1:a]volume=0.22[m];[0:a]asplit=2[v][sc];[m][sc]sidechaincompress=threshold=0.02:ratio=8:attack=20:release=400[md];"
        "[v][md]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[out]",
        "-map","[out]","-ar",str(SR),"-ac","2",os.path.join(B,"mix.wav")], check=True)
    print("duration", t, "captions", len(timeline["captions"]))

def write_wav(path, x):
    x = np.clip(x, -1, 1); w = wave.open(path, "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((x*32767).astype(np.int16).tobytes()); w.close()

def music(dur):
    """Original, self-generated loop: 118 BPM, I-V-vi-IV in C, soft pad + pluck + kick + hats."""
    bpm = 118; beat = 60/bpm; n = int(dur*SR); t = np.arange(n)/SR; out = np.zeros(n, np.float32)
    chords = [[60,64,67],[55,59,62],[57,60,64],[53,57,60]]
    f = lambda m: 440*2**((m-69)/12)
    bar = 4*beat
    for b in range(int(dur/bar)+1):
        ch = chords[b % 4]; s = int(b*bar*SR); e = min(n, int((b+1)*bar*SR))
        if s >= n: break
        tt = t[s:e]-b*bar
        env = np.minimum(1, tt/0.3)*np.minimum(1, (bar-tt)/0.3)
        pad = sum(np.sin(2*np.pi*f(m)*tt)+0.3*np.sin(2*np.pi*2*f(m)*tt) for m in ch)/len(ch)
        out[s:e] += 0.18*pad*env
        bass = np.sin(2*np.pi*f(ch[0]-24)*tt)*np.exp(-((tt % beat))*3)
        out[s:e] += 0.25*bass
        for k in range(8):  # eighth-note plucks arpeggio
            ps = s+int(k*beat/2*SR); pe = min(e, ps+int(0.25*SR))
            if ps >= e: break
            pt = np.arange(pe-ps)/SR; m = ch[k % 3]+12
            out[ps:pe] += 0.10*np.sin(2*np.pi*f(m)*pt)*np.exp(-pt*14)
    for k in range(int(dur/beat)+1):  # kick each beat, hat on off-beats
        ks = int(k*beat*SR); ke = min(n, ks+int(0.18*SR))
        if ks >= n: break
        kt = np.arange(ke-ks)/SR
        out[ks:ke] += 0.45*np.sin(2*np.pi*(50+90*np.exp(-kt*30))*kt)*np.exp(-kt*18)
        hs = int((k+0.5)*beat*SR); he = min(n, hs+int(0.05*SR))
        if hs < n:
            rng = np.random.default_rng(k); out[hs:he] += 0.05*rng.standard_normal(he-hs)*np.exp(-np.arange(he-hs)/SR*80)
    fade = np.minimum(1, t/1.5)*np.minimum(1, (dur-t)/2.0)
    out *= fade
    return out/np.max(np.abs(out))*0.8

asyncio.run(main())
