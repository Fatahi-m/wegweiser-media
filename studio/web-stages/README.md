# web-stages – cinematic HTML/Playwright video pipeline (Nov 2026)

Second renderer, used for the app promo, the § 25 series, the business ad, the passport/BAMF/news videos.
Look: dark navy (fa) / dark green (ku, `body.ku`) background with rays, stars, gold headlines, glass rows, phone mockups.
The older Python renderers (batch2/kgen.py, pgen.py) are still valid for the classic info-reel style.

## Files
- `render.js` – `STAGE=file.html node render.js <dir> <from_s> <to_s> <out.mp4> '<SC json>'` → 30 fps JPEG frames piped to x264 (crf 18).
- `snap2.js` – `STAGE=file.html node snap2.js <dir> 3 8.5 20` → writes `f-<t>.png` preview frames (look at them before rendering).
- `shot1.js` – `node shot1.js <dir> cover.html out.jpg` (static cover pages).
- `k25-head.css` – shared head: fonts, background layers, `.hl .w` word reveal, `.g` gold text, `.num`, `.pill`, `.warn`, `.bub`, `.logo`, phone `.pw/.ph/.scr`.
- `k25-body.html`, `biz-body.html` – body templates (`__CLS__`, `__SC__`, …) used to generate the stage files.
- Stage files (each exposes `window.render(T)` and `window.SC = [[start,end],…]` per scene):
  - `k25*.html` – "کدوم ۲۵؟" (§ 25 types), fa/ku, `-tt` = TikTok variant
  - `k252-*.html` – "ژنو یا سوبسیدیر؟" (§ 25 Abs. 2). Generic engine: elements with `data-t` (seconds relative to scene start) and `data-a` = pop | rise | pillx | card.
  - `biz*.html` – business/event listing ad (fa/ku), `cov-biz-*.html` covers
  - `cine.html` (#fa / #ku) – app promo; `pass*`, `letter*`, `news*` – passport colours, BAMF letter after home trip, weekly news
  - `stage*.html` – classic promo stage; `cover-*.html` – covers; `fbcover-ku.html` – Facebook cover 1640×624
- `sh.rnnn` – RNNoise model for `arnndn`. `music.wav` – vidIQ-generated royalty-free bed (106 s; loop with `-stream_loop 1` for longer videos).
- Fonts: Vazirmatn (Persian/Kurdish), Inter (Latin) – both OFL. Logos: `logo-fa.png`, `logo-ku.png` (compass logo, Nov 2026); `logo.png` = old signpost (do not use any more).
- Website screenshots (`s-*.png`, `ku/s-*.png`) are NOT in the repo (too big): make full-page screenshots of wegweiser-news.de pages at 412 px width (deviceScaleFactor 2) when a phone mockup needs them.

## Workflow
1. Timing: `ffmpeg -i voice.wav -af silencedetect=n=-35dB:d=0.12 -f null -` (finer: -32dB/0.12). If the user sends 2 WAV parts, play them in time order (file timestamp) and offset part 2 by part1 + 0.25 s.
   Estimate sentence positions by character share, then snap to the real pauses.
2. Write SC (scene windows) + per-element `data-t`. Preview with snap2.js, check overflow/bidi, fix.
3. Voice chain: `highpass=f=80,arnndn=m=sh.rnnn:mix=0.6,equalizer=f=200:t=q:w=1:g=1.5,equalizer=f=3200:t=q:w=1:g=2,highshelf=f=9000:g=1.5,deesser=i=0.35,acompressor=threshold=-20dB:ratio=3,loudnorm=I=-15,apad=pad_dur=1.3`
4. Music: volume 0.30, `sidechaincompress=threshold=0.03:ratio=6` keyed by the voice, amix (normalize=0), `loudnorm=I=-14`, fade out last ~1.9 s.
5. Render in chunks, concat, mux audio. **The container may only have 2 CPUs: run at most 2 render.js in parallel** (7 in parallel crashed with screenshot timeouts on 15.11).
6. TikTok variant: same render, only the last scenes differ (`body.tt`: no logo, no URL, no site screenshot; show the paragraph big instead). Re-render only the tail chunk.
7. Cover = a frame from the opening scene (paragraph big on a MUSTER card) or a dedicated cover page.

## Pitfalls
- A CSS class name used twice (e.g. `.pp` = passport in pass.html AND small passport icon) → elements stacked at one position. Scope with `#s5 .pp{position:relative}`.
- RTL: keep Latin brand names in ONE span ("Wegweiser News"); "BAMF" + "یش" in separate spans renders apart.
- `.row` with long text: give `.tx` `flex:1;min-width:0` and keep `.k` small, otherwise text runs out of the row.
