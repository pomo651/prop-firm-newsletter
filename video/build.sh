#!/usr/bin/env bash
# Weekly Funded Tape Short. 1) edit episode.json (items, tags, "say" lines, slug, date range)
# 2) ./build.sh  -> build/ (audio, timeline), cover PNG, final MP4.  Requires: ffmpeg, google-chrome,
#    python3 with: pip install --user --break-system-packages edge-tts playwright numpy
set -euo pipefail
cd "$(dirname "$0")"
python3 make_audio.py          # TTS (cached per line), caption timings, generated music, ducked mix
python3 render.py --preview 2,10,20   # quick frames in build/preview/ for a visual check
python3 render.py              # cover + 30fps frames -> H.264/AAC MP4
