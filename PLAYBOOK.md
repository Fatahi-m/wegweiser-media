# PLAYBOOK – Wegweiser Farsi + Wegweiser Kurdi (read this first, every agent)

This file is the shared knowledge of all Wegweiser agents (topic, comment, video, story, law watch, weekly report, posting).
It was extracted from the long chat in which the user and Claude built the pages, videos and workflow.
The original code from that chat is in `studio/` (renderers, specs, covers, stories, alignment tool, scripts, knowledge base).

## Setup for any agent that renders video/images with the original code
```bash
cp -r <repo>/studio /home/claude/wegweiser        # paths in the code are hard-coded to /home/claude/wegweiser
sudo mkdir -p /usr/share/fonts/opentype/inter && sudo cp /home/claude/wegweiser/fonts_sys/inter/*.otf /usr/share/fonts/opentype/inter/ 2>/dev/null || true
mkdir -p /home/claude/wegweiser/out
```
Render outputs from /home/claude/wegweiser/out back into the repo (reels/, reels-ku/, archive/*/v2/ covers, stories/).
Save every new script also in `studio/v7/<name>.txt` and every new spec in `studio/batch2/` and commit them, so the next run can reuse them.

## UPDATES AFTER 23.10.2026 (these override the original handoff below; where they differ from the newer section "UPDATES 23.10.–15.11.2026", the newer section wins)
- **Two versions of every video (since 12.11):** Instagram version (logo + handle + website) and TikTok version (no logo, no URL, no website screenshot; content visible from frame 0). The Instagram version goes into the posting queue; the TikTok version is sent to the user.
- **Names/handles (15.11.2026):** Persian page = "Wegweiser Farsi", @wegweiser_farsi (Instagram + TikTok, formerly @wegweiser.deutschland). Kurdish page = "Wegweiser Kurdi", @wegweiser_kurdi (Instagram + TikTok, formerly @wegweiser_kurdi.de). Never show the old handles in new videos, covers or stories. In the code, replace any hard-coded old handle.
- **Logo:** Wegweiser compass logo (based on the old TikTok sun-compass), one shape in two colourways: Persian navy/gold (`brand/logo-farsi-navy.png`), Kurdish Kurdistan sun with red/white/green ring (`brand/logo-kurdi-green.png`, `brand/logo-kurdi-main.png`). Replaces the older signpost logos in studio/aof and studio/brand_k.
- **Style:** the classic info-reel style of these renderers. No stock footage/photos in the background. No yellow highlight boxes on text (the user finds them ugly). Names on illustrated ID/residence cards must be clearly fake (MUSTERMANN etc.) — TikTok restricts videos that look like real cards.
- **Opening (28.10.2026):** every video starts with the cover image as frame 0 (slow zoom), not with a blank/animated screen — TikTok drop-off at second 0–1 was the problem.
- **Calls to action (28.10.2026):** no mid-video follow/like ask any more; keep the follow/like/comment request at the END only (plus the hook at the start). Ask a specific comment question at the end.
- **Length:** normal reels around 60 s; the series "one residence, one video" must NOT be under 1 minute (user, Nov 2026, see section below).
- **Covers:** paragraph (e.g. § 26 Abs. 3) written BIG so viewers see at a glance which paragraph it is about. v2 cover kits: `archive/fa/kit/fa_covers.py`, `archive/ku/kit/ku_covers.py` (see README.md).
- **Posting:** Instagram posts at 14:00 and 18:00 (2 per page per day) from `queue.json` (Persian) / `queue-ku.json` (Kurdish) by the posting tasks. TikTok and Facebook: the user posts himself.
- **Audio:** the user makes the voice in Google AI Studio (Gemini TTS) and emails the WAV to himself with subject fa-1 / fa-2 / ku-1 / ku-2; the video agent picks it up. Use his audio as is.
- **Every video:** source on screen, logo + handle, info 100 % correct and current.
- **Shared files in this repo:** `drafts/<date>/` (scripts from the topic agent), `comments/topic-requests.md` + `comments/handled.json` (comment agent), `reports/insights.md` (weekly report lessons), `laws/updates-*.md` (law watch), `stories/<date>/`.
- **Knowledge base:** `studio/kb/wissen.html` holds the verified facts (cards). Agents read it before answering/writing; when a new fact is verified, update the matching card (keep the date and source).

## More lessons from the WEGWEISER chat (the user's main working chat, Oct–Nov 2026)
- **Cover intro (how it was done, 26.10):** render the reel, then overlay the cover for the first sentence (~8 s) with a gentle zoom and fade out:
  `ffmpeg -y -i reel.mp4 -loop 1 -t 8.2 -i cover.jpg -filter_complex "[1]scale=1080:1920,zoompan=z='1+0.00018*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,format=yuva420p,fade=t=out:st=7.9:d=0.3:alpha=1[cv];[0][cv]overlay=0:0:enable='lte(t,8.2)'[v]" -map "[v]" -map 0:a -c:v libx264 -crf 20 -preset medium -c:a aac -b:a 192k out.mp4`
  (set -t / st to the end of the first sentence). Keep the zoom gentle (0.00018 per frame).
- **Reply-to-comment videos:** start with «پرسیاری ئێوە لە کۆمێنت: …» / «سؤال شما توی کامنت: …» and show the comment in a bubble (bubble() in batch2/ks_253.py / ks_255.py) WITHOUT the commenter's name.
- **On-screen text:** never add text the user did not approve; if he changed the wording when recording the audio, put HIS wording on screen.
- **Sync:** timing comes only from silences (no speech-to-text). Always check test frames; tell the user once "please check the sync" when something was unusual.
- **Captions:** hook line, short explanation (✅ points allowed), source line, short "general info" note, save/share ask, hashtags (Kurdish e.g. #کوردانی_ئەڵمانیا #wegweiser_kurdi; Persian e.g. #ایرانیان_آلمان #wegweiser_farsi).
- **Reposts:** the user does not want other pages to repost his videos; if a page wants to share, only Instagram Collab (logo kept, tagged, no edits).
- **Re-uploading a fixed video:** wait 2–3 days so TikTok does not treat it as a duplicate, and use a new caption.
- **What performs best (Oct):** "money you are entitled to but don't know about" (Kinderzuschlag, Einstiegsgeld, 5 kinds of Jobcenter help) and residence types one by one. Kurdish page grows faster and asks many residence-law questions. Word-of-the-day / 5-Kalame series are weak (max once a week).
- **Delivery to his PC (when the computer is linked):** Kurdish outputs to Videos\Kurdi\, covers to Videos\Covers\; verify with a directory listing after writing.

## UPDATES 23.10.–15.11.2026 from the main chat (website + videos + brand)
Source: the user's main working chat (Claude session 01EyyHQKB5GXYHEq3Txdddrp). Older parts of that chat were only available as summaries, so for 23.10–10.11 the lists below are reconstructed from the delivered files and the website git log. No follower names, DMs or private cases are recorded here (public repo).

### Brand / accounts (status 15.11.2026)
- **Logo (decided 15.11):** compass logo, same shape in two colourways. Vector files: `brand/wegweiser-logo-farsi.svg` (navy/gold compass rose, red/white needle) and `brand/wegweiser-logo-kurdi.svg` (Kurdistan sun with 21 rays, red/green needle, red-white-green ring). Generator + PNG/icon export: `studio/logo/` (`r.js` profile pictures 1080², `icons.js` app icons). The user chose "one shape, two colours" over one neutral logo.
- **Handles (15.11):** Wegweiser Farsi @wegweiser_farsi, Wegweiser Kurdi @wegweiser_kurdi (Instagram + TikTok). Old handles are dead links.
- **Facebook page "Wegweiser Kurdî"** created 14.11 (category News & media website; cover = `studio/web-stages/fbcover-ku.html` → 1640×624, text kept in the centre, bottom-centre free for the profile picture). It is connected to vidIQ (platformAccountId 1413479338521331, canPublish). The user prefers **Instagram auto-share to Facebook** (Accounts Center → Kontoübergreifendes Teilen) instead of posting via vidIQ, because vidIQ needs a public video URL.
- **Website:** www.wegweiser-news.de (repo Fatahi-m/wegweiser-news, Next.js 15, Vercel; DNS at INWX). Contact e-mail kontakt@wegweiser-news.de works (verified 14.11 – it received the Meta verification code).
- **Impressum/stores:** a paid business-address service is used for Impressum, App Store/Play Store and social media (address is in the site's Impressum). Gewerbe registration uses a different address – never put the private address anywhere.

### Website (Fatahi-m/wegweiser-news) – what exists now
- Locales `fa` (navy) and `ku` (green) + a German info page `/de`. Content: `content/{fa,ku}/*.md` (frontmatter: title, summary, date, image `/img/topic/<topic>.jpg`, category news|guide|deport, kb, lead, badge, kicker, sources). Article URL `/{l}/article/{slug}`.
- Tools: Wohngeld + Kinderzuschlag calculators (`/{l}/rechner/wohngeld|kinderzuschlag`), Fristenrechner (Widerspruch/Klage, holidays of all Länder, .ics reminder), Zahltermine (payment dates), **"Was steht auf deiner Karte?"** (`/{l}/karte`, 45 entries, eAT card design, infos on duration/work/travel/family/NE/Einbürgerung), interactive forms with PDF download (pdf-lib, in the browser: Anmeldung Berlin, Jobcenter Anlagen KDU/VM/MEB/EK, Veränderungsmitteilung, KG45, Unterhaltsvorschuss, Kita-Gutschein, Integrationskurs …), "Voraussetzungen & Unterlagen" guides, "Eure Fragen" (Q&A), Arbeit & Ausbildung page, Städte (counselling by city), quiz, Über uns (bio of the author – link to it from posts: `wegweiser-news.de/ku/about`, `/fa/about`).
- PWA with install popup; push (OneSignal) is **hidden for now** (to be repaired). Vercel Web Analytics (cookieless).
- 15.11: header/footer/app icons switched to the compass logo (`public/brand/logo-{fa,ku}.svg`, `public/icons/*`), social links switched to the new handles (`lib/i18n.js`).
- Writing rules for site content: Persian colloquial ("umgangssprachlich"); Kurdish «ئیقامەی دائیمی», Gregorian month names (جانیوەری, فێبریوەری …); planned laws get «⚠️ هنوز قانون نشده» / «⚠️ هێشتا نەبووە بە یاسا»; every news item with sources.
- **Open:** Google Search Console (waiting for the meta-tag code), Google Play via PWABuilder (package `de.wegweisernews.app`, needs assetlinks.json in `public/.well-known`), business/events directory (promised in the ad, not built yet – see below).

### Videos made 23.10.–15.11.2026 (do not suggest again)
- 23.10: § 31 Trennung (fa) / Jiabunawa (ku); Salha (fa)
- 24.10: § 25 Abs. 1 (fa+ku), § 25a (ku), Rente (fa+ku), Karte (ku), Mehrbedarf (fa)
- 25.10: Widerruf (fa+ku), Safar/travel (fa+ku), § 26 Abs. 4 (ku)
- 26.10: § 26 Abs. 3 (fa+ku, v2 with cover intro), Einladung/Verpflichtungserklärung (fa+ku)
- 29.10: § 26 Abs. 4 (fa), Fiktionsbescheinigung (ku)
- 01.11: Krankenkasse (fa+ku)
- 05.–06.11: Schwarzarbeit (ku), § 25b types (ku)
- 09.–12.11: website promo (fa+ku), "5 types of residence" part 1+2 (fa+ku), app promo cinematic (fa+ku, also with music), "Ap" classic reel (fa+ku), **passport colours** (fa+ku)
- 13.11: **BAMF letter after a trip home** (fa+ku), **weekly news 13.11** (fa; hook = AfD motion on citizenship, Drucksache 21/9077 – only a motion, not law)
- 14.11: **"کدوم ۲۵؟ / کام ٢٥؟"** – overview of § 25 Abs. 1–5, 25a/25b, Gestattung, Duldung, §§ 22/23/24 (fa+ku), script `studio/v7/p25-arten.txt`, `k25-arten.txt`; **business/event listing ad** (fa+ku, cinematic; first **50** listings free, send to kontakt@wegweiser-news.de)
- 15.11: **series part 2 "ژنو یا سوبسیدیر؟ / جنێڤ یان سوبسیدیێر؟"** (§ 25 Abs. 2, ~1:55, fa+ku), scripts `studio/v7/p252-genf-subsidiaer.txt`, `k252-genf-subsidiaer.txt`
- Other channels in the same period: Geld ohne Filter "Krankenkasse"; @durchgerechnet_de episode 1.
- Every video since 12.11 comes in two versions: Instagram (logo + website) and **TikTok** (no logo, no URL, no website screenshot; content visible from frame 0).

### Series "one residence, one video" (continues)
Part 1 = § 25 overview (done), part 2 = Genf vs subsidiär (done). Next: 3 = § 25 Abs. 3 + Abs. 5 (Abschiebungsverbot / Ausreise unmöglich), 4 = 25a + 25b, 5 = Gestattung vs Duldung (60a–60d), 6 = §§ 22/23/24, 7 = from § 25 to NE and passport (26/9/9a), 8 = Fiktionsbescheinigung (§ 81). Each ends with "details in the web app (link in bio)" + a comment question ("which type are you?"). The user wants these **not under 1 minute**.

### New verified facts / laws (status 13.–15.11.2026)
- **How to tell Flüchtling vs subsidiär:** card Anmerkungen "§ 25 Abs. 2 S. 1 **1. Alt.**" = Flüchtling (GFK), "**2. Alt.**" = subsidiär; BAMF Bescheid "Flüchtlingseigenschaft wird zuerkannt" vs "subsidiärer Schutzstatus wird zuerkannt". Card duration no longer tells them apart (both 3 years since 27.02.2024).
- Flüchtling: blue Reiseausweis (all countries except the home country); privileged Familiennachzug if applied within 3 months (no income/housing requirement); NE after 3 years + C1, or 5 years + A2 + mostly self-supporting. Subsidiär: usually must use the national passport, grey Reiseausweis für Ausländer only if a passport is unobtainable; Familiennachzug suspended until 23.07.2027 except hardship; NE after 5 years with the normal § 9 conditions (B1, work …). Both: work fully allowed, Wohnsitzauflage § 12a for the first 3 years, asylum-procedure time counts for Einbürgerung.
- **From 01.01.2027:** Mindestlohn 14.60 €, Minijob cap 633 €; Kindergeld without application (law passed; 2nd+ child from March 2027, 1st child at the earliest Nov 2027; only if a parent works in Germany and the IBAN is known); Krankengeld only 60 % net (67 % with children) if the job ends during sick leave (GKV-Beitragssatzstabilisierungsgesetz); Deutschlandticket 66.80 €; average Zusatzbeitrag 2.9 %.
- ⚠️ **Planned, not law (13.11):** Wohngeld cut from 01.01.2027 (heating component halved, ~381,000 households could lose it); per the bill, an application that **arrives by 31.12.2026** keeps the December amount. Grundsicherungsgeld 2027 likely a Nullrunde (563 €), not decided. Kindergeld 267 € (2027) only a draft.
- Integrationskurs budget for 2027 roughly halved (enrol now if entitled). Jobcenter money for January arrives around 30.12; December money end of November.
- **"Buy now, pay later" (Klarna/PayPal):** EU Consumer Credit Directive 2023/2225 applies from **20.11.2026** – many BNPL purchases count as credit, creditworthiness check, clear pre-contract info, 14-day withdrawal, duty to offer help when instalments can't be paid. German implementing law not yet verified.
- Police warning: WhatsApp account theft via fake "vote for my friend" links – never share the WhatsApp code.

### Trend research (vidIQ, week 06.–13.11.2026)
Top performers around our niche: "what changes from 2027" lists (German: Minijob, tax-free employer benefits 2M views, Steuerbescheid digital, Mütterrente), "BNPL becomes credit on 20.11" (1.1M), Rundfunkbeitrag data matching (1.5M), Arabic "biggest mistake in Germany – frying oil in the sink" (3.4M) and Pfand (981k), Persian migrant-life comedy skits (1.3M). Simple text-on-screen lists and direct-to-camera explainers win. No strong Kurdish competitor found → gap for us. Idea list given to the user: BNPL 20.11 (most urgent), 2027 changes (already made), Rundfunkbeitrag letter, "3 everyday mistakes that cost a fine", a skit with his own face (best fix for TikTok "non-original" flags).

### Social / platform lessons (Nov 2026)
- **TikTok restriction "Nicht originale Inhalte … QR-Code-Inhalte" at 00:00:** likely logo/URL/screenshot + AI voice. Use the TikTok variant, label "KI-generierter Inhalt", don't set video language to Deutsch (Persian page: Persian/English; Kurdish: Arabic was chosen), turn auto-captions off, consider his own face for the first 2–3 s, don't re-upload identical files (wait 2–3 days, new caption). Work with Artists: apply; skip like-based contests.
- **Reposting/theft:** several Facebook pages re-upload our videos and cover logo/handle with stickers (one profile had 30+ videos). Reporting path that works: on the Facebook reel "…" → Find support or report → **Report as unlawful → Intellectual property → Copyright → Continue → Germany, Yes (rights owner)** → form on help.meta.com (up to 30 URLs separated by spaces, original = TikTok/Instagram profile links, e-mail verified by code). Report filed 14.11 (11 URLs). One form for all URLs. Take screenshots first.
- Answer to the reposting: a Kurdish carousel (10 slides, 1080×1350) + 6 stories (1080×1920) "they take our videos – but who answers your questions?" – respectful, names no page, no profession insulted, links the bio page. Code: `studio/carousel/` (`build.py` slides, `story.html`, `shot*.js`).
- Facebook page posting: post 1–2 videos per day, not all at once.

### Business / events directory (promised in the 14.11 ad)
- Free listing for the **first 50** businesses or event organisers (later: basic entry free forever, paid extras such as featured spot, more photos, promotion in reels/stories – charge only under a registered Gewerbe with invoices).
- Data to send: name + type, city/address (events: date/time), phone/site/Instagram, photo/logo/poster, a few lines. Publish only what the sender sent; add a sentence to the Datenschutz page.
- **Not built yet** on the website: section "کسب‌وکارها و برنامه‌ها" with city + category filter and auto-expiry of past events.

### Code added to this repo (15.11.2026)
- `studio/web-stages/` – cinematic HTML/Playwright renderer, all stage/cover files of Nov 2026, audio chain (see its README).
- `studio/carousel/` – carousel/story generator (Kurdish "who answers your questions" post).
- `studio/logo/` + `brand/wegweiser-logo-{farsi,kurdi}.svg` – the compass logo.
- `studio/v7/`: `p25-arten.txt`, `k25-arten.txt`, `p252-genf-subsidiaer.txt`, `k252-genf-subsidiaer.txt`, `kbiz-ad.txt`, `pbiz-ad-post.txt`, `klarna-bnpl-teaser.txt`, `k-news-1311-teaser.txt`, `p2027-aenderungen.txt`.

### Open (status 15.11.2026)
1. Series part 3 (§ 25 Abs. 3 + 5) script fa + ku.
2. BNPL 20.11 video (scripts ready, no audio) + website article (verify the German implementing law first).
3. Business/events directory on the website.
4. Search Console meta tag, Google Play listing (texts fa/ku/de, feature graphic 1024×500, screenshots).
5. Einbürgerung YouTube video: audio for blocks 17–74 missing.
6. Step-by-step online-application walkthroughs (Einbürgerung/NE/Verpflichtungserklärung) with MUSTER data – planned, never submit anything.
7. "About us" carousel (two designs rejected; waiting for references) – the 15.11 carousel partly covers it.

## Original handoff (status 23.10.2026) — still valid unless the update section above says otherwise

---

## 0. In short: what you do for the user every day
1. **Comment and DM replies** for his two pages (Persian and Kurdish Sorani). He sends screenshots; you write the replies, ready to copy.
2. **Short videos (Reels/TikTok):**
   - You research the topic and verify every fact.
   - You write a TTS script.
   - He records the audio in AI Studio and sends a WAV.
   - You align the audio, render the video and the cover, and send both together with a caption.
3. **Knowledge base ("Wissensbank"):** add every newly verified fact and every new answer **immediately and in full detail**. STANDING RULE, the user's words: «هر اطلاعاتی که بهت میدم جدید هست زود به بانک اطلاعاتی که ساختیم اضافه کن با جزئیات کامل خیلی مهمه» ("Any new information I give you, add it right away to the knowledge base we built, with full details. Very important.")
4. Occasionally: stories (JPG), video ideas and topic lists, lesson review for his Kurdish German-learning app (see §10).
5. After every larger step, update this handoff and the zip.

---

## 1. Who / channels / numbers
- **The user:** Sozialarbeiter with 8 years of experience with German offices (Jobcenter, Jobcoach, Buchhaltung). Lives in Germany. Writes in Persian.
- **Persian page:** "Wegweiser Deutschland", @wegweiser.deutschland (TikTok + Instagram).
  - Navy blue design, compass logo.
  - TikTok created around 15.10.2026. In the week 14–20 Oct: 539k views, 18.1k likes, 9.5k shares, 926 comments, 5k profile views (weak).
  - Einstiegsgeld video: 77.9k views, 2,655 saves, 2,200 shares.
- **Kurdish page:** "Wegweiser.Kurdî", @wegweiser_kurdi.de (TikTok + Instagram).
  - Cream / red / green design with a sun logo. Every Kurdish video shows the logo and the handle.
- **YouTube:** "Geld ohne Filter" (@Geld-ohne-Filter), German finance Shorts with the vidIQ voice "Chris". Has been dormant lately.
- **What works:**
  - "Hidden money" topics that many people are entitled to (Einstiegsgeld, Kinderzuschlag, 5 kinds of Jobcenter help).
  - Residence types explained one by one ("what's on your card?").
- **What doesn't work:** niche topics. Example: § 16c self-employment got only 1,000 views in 2 hours.
- **Plans:**
  - Lives once or twice a week (the knowledge base is meant for this).
  - Creator Rewards (account must be 30 days old, 10k followers).
  - Later sponsoring.
  - His own German app (§10).

---

## 2. Standing rules (all of them; do not break any)
### Content
- Information must be **correct, current and sourced**. Check the current status before writing anything (web search; lxgesetze.de and gesetze-im-internet.de partly work; buzer is often blocked). Show the source on screen in every video.
- When in doubt, mark it as "unverified" and do **not** put it in the video.
- Never mention WAB-Akademie (until the user says so).
- Dates are always Gregorian (e.g. 04.03.2028 or "مانگی ١١"). **Never** use Kurdish/Arabic month names (شوبات, ئادار, حوزەیران …). In Persian too, write "جولای ۲۰۲۷", not Persian solar months.
- Use the new names:
  - **Grundsicherungsgeld** (replaced Bürgergeld on 01.07.2026; mention "formerly Bürgergeld" when it helps).
  - "ئیقامەی دائیمی" (never "هەمیشەیی").
  - German office names stay German (Jobcenter, Ausländerbehörde, Familienkasse …).
- The user does **not** want other pages to repost his videos. Followers should share from his page.

### Comment replies (TikTok/Instagram)
- **At most 150 characters per reply**, each in its own code block so it can be copied.
- **Language:** reply in the language of the comment.
  - Kurdish Sorani in Arabic script, even if the comment is in Latin script or in Badini.
  - Persian (Iranian or Afghan Dari, plain colloquial style).
  - German if the comment is in German.
- **Style:** handwritten, plain, short, friendly.
  - No emojis, no bold, no lists, no headings.
  - Not formal ("not like an email").
  - Must not sound like an AI.
  - Just explain and finish.
- Show the name of the commenter above each reply so the user knows which reply belongs where.
- **If there is no video on the topic yet:** "به زودی ویدیو می‌ذاریم" / "بەم زووانە ڤیدیۆی لەسەر دادەنێین" ("we'll post a video on it soon").
- **When something is unclear** (e.g. only "25 Abs. 2"): give a short, useful answer, or ask exactly one question back.
- **Example (Persian):** `توی Bescheid از BAMF ببین: اگه نوشته Flüchtlingseigenschaft یعنی پناهندگی کامل، اگه subsidiärer Schutz یعنی حمایت تکمیلی.` ("Look at your BAMF Bescheid: Flüchtlingseigenschaft means full refugee status, subsidiärer Schutz means subsidiary protection.")
- **Example (Kurdish):** `بەڵێ دەبێت، هەمان ڤیزایە. بۆ خوشک، برا یان هەر خزم و هاوڕێیەک هەمان ڕێگایە، تەنها بەڵگەی خزمایەتی جیاوازە.` ("Yes, it's the same visa. Sister, brother or any relative or friend goes the same way; only the proof of relationship differs.")

### DM replies
- **Useful and concise, neither too short nor too long.** The user's words: «اینجوری خیلی طولانی ننویس مفید و مختصر نه کوتاه و نه زیاد بشینی تومار بنویسی» ("Don't write it this long. Useful and to the point, not too short and not so much that you sit and write a scroll.")
- A good DM reply has 4–8 lines in a code block. Under it, add at most 2–4 short lines of explanation **in Persian** for the user (what you assumed, what the risk is).
- **Read precisely!** The user got angry when I misread a message: I took a question about salary to be about residence, and I took Sozialamt to be the Jobcenter. Before answering, work out:
  - Who is asking?
  - What is their status (Duldung / Gestattung / residence title)?
  - Who pays them (Jobcenter / Sozialamt / nobody)?
  - Where do they live (Heim or own flat)?

  Ask if anything is unclear.
- **Sensitive cases** (criminal charges, deportation, child-related accusations): no assessment of the facts. Point to a lawyer, Flüchtlingsrat, Eilantrag and similar. Keep it short and empathetic. Never give tips on evading the authorities.
- If the user writes "this is someone else / he sent a voice message", treat it as a new case. Don't mix cases.
- If the user pastes in a reply he already sent, don't repeat what's in it. Only add what's new or corrected.

### Videos (both pages)
- **Fixed structure:**
  - 0–3 s: hook (question or promise, ideally money or "many don't know").
  - 3–6 s: short follow/like ask ("فالو کن و لایک کن، تا این اطلاعات به همه برسه" / "فۆڵۆمان بکە و لایکێک بکە، با ئەم زانیارییە بگاتە هەمووان").
  - Middle: content.
  - **Mid-video save/like ask** that makes clear the video isn't over ("یه نکته‌ی خیلی مهم مونده! این ویدیو رو سیو کن و لایک کن، تا بهت بگم …" / "خاڵێکی گرینگ ماوە! سەیڤی ئەم ڤیدیۆیە بکە و لایکێک بکە، تا پێت بڵێم …").
  - End: a **specific comment question** ("حالا تو بگو: … کامنت کن!" / "ئێستا تۆ بڵێ: … لە کۆمێنت بنووسە!").
- **At least 1 minute long.** Typical length is 75–115 s.
- No face, never the user himself. Only text on screen plus TTS voice.
- **Captions are short:** hook (2–3 sentences), comment question, "منبع/سەرچاوە: …", 4–5 hashtags. Not the full video text.
- **Covers (eye-catching):**
  - For residence types: the paragraph in big type at the top (e.g. "§ 25 Abs. 2") → personal question → promise in red/gold → remark box ("ANMERKUNGEN/REMARKS" like on the eAT card) → green chip with an attractive number.
  - For money topics: the big amount at the top ("تا ۵۰۰۰ یورو").

---

## 3. Script format (TTS) – important
- **One paragraph per line**, inside a code block (the user copies it straight into AI Studio).
- **German words in Latin script.** Write paragraphs out as words: "Paragraf fünfundzwanzig Absatz zwei", "Paragraf sechzehn c SGB zwei", "A zwei", "B1" (the voice says "B eins").
- **All numbers in the script are words** (Persian: "دویست و نود و هفت یورو"; Kurdish: "پێنج هەزار یۆرۆ"). On screen, use digits.
- Typically 9–12 paragraphs:
  1. hook
  2. follow ask
  3–5. content
  6. mid-video save ask
  7–10. content
  11. comment question
- **Save every script immediately as `v7/<name>.txt`** (one paragraph per line). Alignment needs exactly this text. Lost scripts cannot be aligned.
- **Persian register:** colloquial Iranian ("میشه، می‌گیری، بهت میگم"), with the German terms kept.
- **Kurdish register:** Sorani, clear. Terms: "ئیقامە، ئیقامەی دائیمی، جنسیە، Duldung، Jobcenter".
- **AI Studio note (since 22.10.2026):**
  - The new TTS models (Gemini 3.x Flash TTS) read instructions in the text box **aloud**. Put the style in the separate **Style** field (short, in English, e.g. `warm, clear, energetic`), or use `gemini-2.5-flash-preview-tts`.
  - Voices: a female and a male voice that he likes (for the app: Ludo/Sola/Jori/Knox).
  - The old instruction was: "Read … in natural Central Kurdish (Sorani) / Iranian Persian … every Latin-letter word is German, native German pronunciation …".
- **When a WAV arrives without a name** (e.g. "Generated_Audio_…wav" + "farsi"): align it against all open scripts and take the one with the **lowest cost** (adp.py prints the cost).

---

## 4. Video pipeline (technical)
All paths are under `/home/claude/wegweiser`. Outputs go to `out/`.

1. **Copy the WAV** to `v7/<name>.wav`.
2. **Alignment:** `python3 tools/adp.py v7/<name>.wav v7/<name>.txt`
   - Prints the cost and the start times of each paragraph, plus the end of the audio.
   - It uses dynamic programming over the pauses (ffmpeg silencedetect, d=0.12) with cost log(dur/expected)² − 2·gap.
   - Then look at the finer pauses for the timings of the items inside each scene:
     `ffmpeg -i X.wav -af silencedetect=n=-35dB:d=0.2 -f null - 2>&1 | grep silence_end`
3. **Audio prep:** `ffmpeg -y -i v7/X.wav -af "loudnorm=I=-14:TP=-1.5:LRA=11,apad=whole_dur=TOTAL" -ar 48000 -ac 2 v7/X_v.wav`
   - TOTAL = outro_t + 6 s.
   - outro_t = end of the last paragraph + 0.3 s.
4. **Write the spec:**
   - Kurdish: `batch2/ks_<name>.py`
   - Persian: `batch2/ps_<name>.py`
   - Copy the most recent examples: `ks_besuch.py`, `ks_16c.py`, `ks_255s.py`, `ps_252.py`, `ps_besuch.py`, `ps_2223.py`.
5. **Render test frames:**
   - Kurdish: `cd batch2 && python3 kgen.py ks_X ../v7/X_v.wav ../out/tX.mp4 --frames 5,20,…`
   - Persian: `python3 pgen.py ps_X …`
   - Merge the frames into a contact sheet and **look at it** (Read the JPG).
   - Check for bidi errors, overflow and empty scenes, then delete the test frames.
6. **Full render:** same command without `--frames`, writing to `out/Kurdi-<Thema>-Reel.mp4` or `out/Wegweiser-<Thema>-Reel.mp4`.
7. **Cover:** a small script (`cov<name>.py`) that copies the first 7 lines of `cov6k.py` (Kurdish) or `cov6p.py` (Persian) and makes one `cov(...)` call. **Look at it.**
8. **Send the MP4 and the cover** (SendUserFile), then write the caption in a code block.
9. **Add a "Done" line to the handoff and re-zip.**

### Spec format
```python
SPEC = {"source": "§§ 25 Abs. 2, 26 AufenthG", "topic": "اقامت 25.2",
 "footer": "…" (Kurdish only),
 "scenes": [ [item, item, ...], ... ],          # one scene per paragraph
 "timing": [ ([start item1, start item2, ...], end_of_scene), ... ],
 "outro_t": 103.3, "total": 109.3, "outro": ("question", "comment")}
```
**Kurdish items (kgen):**
- `("title", text, size, color)`
- `("text", text, size, color)`
- `("chip", text, bg, fg, size, latin=True/False)`
- `("card", "§ 16c SGB II", "Kurdish meaning")`
- `("row", text, 1|2|"ok"|"no"|"info", "Latin sub")`
- `("bigfa", "تا ٥٠٠٠ یۆرۆ", color, size)`
- `("img", remark("§ 25 ABS. 5 AUFENTHG"))`

Colours: INK, GREEN, KRED, SUN, W_ = white.

**Persian items (pgen/reel):**
- `("title", t, size, color)`, `("text", …)`
- `("chip", t, bg, fg, size, True)` (latin)
- `("card", de, fa)`
- `("row", t, icon, latin_sub)`
- `("big", "۳ سال", GOLD, 150)`
- `("img", remark(...))` with `from kremark import remark`

Colours: GOLD, GREEN, RED, WHITE, NAVY_D.

### Bidi / layout pitfalls (learned the hard way)
- Latin plus digits inside RTL text gets scrambled ("ئیقامەی 25 Abs. 5ت" → "Abs. 5 25"). Put paragraphs in their own Latin chip (`latin=True`) or in a card/sub.
- A row must **not start with a Latin word** followed by Persian (e.g. "Aufnahmezusage از BAMF" gets reversed). Start with Persian or Kurdish and put the German in the sub.
- A Persian card meaning must not end in a Latin word ("مثلاً برای Ortskräfte" breaks).
- "·" between Persian/Kurdish digits looks like ۰/٠. Use "،" or ":".
- In Persian, write "۲۸۰ یورو", not "€ 280" (it gets reversed).
- Row subs (the second line) are **Latin only** (Persian/Kurdish there shows as boxes).
- A header topic that is too long overlaps the handle. Keep topics short ("اقامت 25.2", "ڤیزای سەردان").
- Max ~5 items per scene (3–4 rows).

---

## 5. Knowledge base ("Wegweiser Wissensbank")
- **File:** `kb/wissen.html` (in the zip). It is a private artifact in the **old** account (https://claude.ai/artifact/U8qR812EPiPX5jLX82zKCQ, version 18).
- **IMPORTANT for the new account:** the old artifact is not accessible from here. **Republish `kb/wissen.html` as a new artifact** (Artifact tool, publish, icon "book"), give the user the new link, and from then on always update the new one. Change it with Artifact `edits` (old_str/new_str) on the same `file_path`. Afterwards check the script syntax with `node --check` (extract the script part).
- **Structure:**
  - In the script there is a data array `D` of cards (currently 46). Card fields:
    `{id, t (Persian title), law, cat (aufenthalt|duldung|ne|pass|reise|geld|arbeit|verfahren), k (search terms, Latin+German), one (one sentence), what, who:[…], dur, ne, pass, travel, tips:[…], src:[[label,url],…], c:"date of last check"}`
  - Highlighting: `<span class='yes'>…</span>` (green) and `<span class='non'>…</span>` (red).
  - Search normalises Persian/Arabic letters, digits, § and Abs.
- **Rule:** after every new video, every newly verified fact and every important DM/comment answer, update the matching card or create a new one.
  - Record cases as a tip ("کیس Rebar (21.10.2026): …").
  - Note the source and the date.
  - Mark uncertain points as "بررسی نشده" (unverified).

---

## 6. Verified facts (status Oct 2026) – the most important ones, including corrections
**Residence (AufenthG)**
- **§ 25 Abs. 2 subsidiär:**
  - Since 27.02.2024 (Rückführungsverbesserungsgesetz) the permit is issued for **3 years** (§ 26 Abs. 1 S. 2). Before that it was 1 + 2 years. → **CORRECTION:** older videos ("Karte" Persian, Kurdish 25.2) still say 1 year. A correction comment for pinning was suggested.
  - The duration of the card therefore no longer tells Flüchtling and subsidiär apart. Only the BAMF Bescheid, or "(3 AsylG)"/"(4 AsylG)" or "1. Alt"/"2. Alt" on the card, does.
- **Familiennachzug for subsidiär** suspended 24.07.2025–23.07.2027; only §§ 22/23 Härtefall (§ 36a Abs. 1 S. 4).
- **NE § 26 Abs. 4** (subsidiär, 25.3, 25b, 22, 23 …): § 9 Abs. 2 → 5 years, B1, LiD, 60 months of pension contributions, Lebensunterhalt, housing. Gestattung years count (asylum procedure, § 26 Abs. 4 S. 3); Duldung years don't.
- **NE § 26 Abs. 3** (Flüchtling/25.1): 5 years (asylum procedure counts) + A2 + mostly self-supporting + LiD; or 3 years + C1. Resettlement 23 Abs. 4: fast route.
- **§ 25 Abs. 3:** at least 1 year. Einbürgerung only via NE first (25.3 is on the exclusion list of § 10 StAG).
- **§ 25 Abs. 5:** after 18 months of Duldung "soll", if it's not the person's own fault (identity, passport efforts). The first permit is up to 6 months until 18 months of lawful stay, later up to 3 years. Work is allowed.
- **§ 25a:**
  - Under 27 at application.
  - 12 months of Duldung (or § 104c).
  - 3 years uninterrupted in Germany.
  - 3 years of school, or a school-leaving certificate or Ausbildung.
  - Parents (Abs. 2) with their own Lebensunterhalt.
  - Grundsicherungsgeld during school/Ausbildung is not a problem.
- **§ 25b:**
  - **Duldung only** (not Gestattung).
  - 6 years, or 4 with a minor child (Duldung, Gestattung and AE all count).
  - Mostly self-supporting (a small top-up is OK).
  - A2 oral, LiD.
  - Children go to school.
  - Identity clarified, or every reasonable effort made.
  - Permits up to 2 years.
  - Travel home is OK (no protection status).
  - Einbürgerung 5 years after 25b. NE via § 26 Abs. 4 (Gestattung counts; some offices wrongly count only the 25b years).
- **§ 25b Abs. 4** (spouse/children): no 6-year rule, but A2/LiD/Lebensunterhalt.
  - **If the spouse still has a pending asylum procedure (Gestattung):** under § 10 Abs. 1 a residence title is only possible with a "gesetzlicher Anspruch", and Abs. 4 is "soll", so it usually only works after the procedure ends (§ 10 Abs. 3). Withdrawing the application only with a lawyer.
- **§ 60d Beschäftigungsduldung:**
  - Entry by 31.12.2022.
  - 12 months of Duldung (60b doesn't count).
  - 12 months of work subject to social insurance, at least 20 h/week.
  - Lebensunterhalt, A2 oral, identity, no crimes, children at school.
  - Runs 30 months → § 25b Abs. 6.
- **§ 28:**
  - Groups: spouse of a German (A1 needed, both 18+); minor child of a German; parent of a German minor with custody. For child and parent there is no income requirement (Abs. 1 S. 2); for the spouse "soll in der Regel".
  - NE Abs. 2 after 3 years: family life continues, B1, no grounds for expulsion. **No 60 months of pension contributions.** Lebensunterhalt usually required (BVerwG).
  - Einbürgerung of the spouse: **§ 9 StAG** after 3 years' residence + 2 years of marriage, B1, test, Lebensunterhalt.
  - § 31 after 3 years of marriage cohabitation in Germany.
- **§ 22 vs § 23 Abs. 2 (Afghans):**
  - § 22 has only Satz 1/2, no Absätze. S. 2 = BMI political interest (Ortskräfte).
  - **§ 22 is on the exclusion list of § 10 Abs. 1 Nr. 2 StAG** (NE first, but the years count). § 23 Abs. 1/2 are **not** on it (only 23a), so Einbürgerung is possible directly.
  - The full list: 16a, 16b, 16d, 16e, 16f, 17, 18f, 19, 19b, 19e, 20, 20a, 22, 23a, 24, 25 Abs. 3–5, 104c.
- **§ 24 Ukraine:** extended automatically to **04.03.2028** (EU 2026/1912; 9th amendment of UkraineAufenthÜV, Bundesrat 25.09.2026). Ukrainian men of military age newly entered from 05.08.2026 must prove lawful exit.
  - 18a/18b require no German by law, but a recognised qualification.
  - Warning: someone who gives up § 24 for a work permit can hardly go back.
- **§ 16d** (Anerkennung): Familiennachzug is possible but hard (income for the whole family). After passing → § 18a. The spouse of a Fachkraft doesn't need A1.
- **§ 18c NE:** Fachkraft 3 years + 36 months; German degree/Ausbildung **2 years with an 18a/18b title after graduating** (work during studies doesn't count) + 24 months; Blue Card 21 months (B1) / 27 months (A1).
- **Visit visa (Schengen C):**
  - Up to 90 days in any 180; fee 90 €; applied for at the embassy/VFS in the home country.
  - Verpflichtungserklärung (§§ 66–68) at the Ausländerbehörde (pay slips, rental contract).
  - Travel health insurance with at least 30,000 € cover. This is the **coverage amount, not the premium** (commenters misread it).
  - Bank statements for the last 3 months even with a Verpflichtungserklärung.
  - Main reason for refusal: doubt that they will return.
  - Apply at most 6 months ahead. Same visa for siblings and friends.
- **Familienasyl after GEAS (from 12.06.2026):**
  - § 26 AsylG Familienasyl **abolished**. Each person is examined individually; if rejected, family membership is checked under Art. 23 VO 2024/1347, leading to a dependent residence title (akzessorisch).
  - The family must have existed **before entry into the EU**. BAMF no longer grants Familienasyl even in old pending cases.
  - Exact § 25 title and duration not yet confirmed.
- **Gestattung + Spurwechsel § 10 Abs. 3 S. 4/5:**
  - Entry before 29.03.2023; only for 18a/18b/19c Abs. 2.
  - Withdrawal of the asylum application is irreversible → lawyer.
- **Fiktionsbescheinigung § 81 Abs. 4:** if the extension was applied for in time, the title continues. Untätigkeitsklage after 3 months (§ 75 VwGO).

**Money / benefits**
- **Grundsicherungsgeld** replaced Bürgergeld on 01.07.2026.
- **§ 16b Einstiegsgeld:** apply before the first working day; job subject to social insurance; up to 24 months; discretionary.
- **§ 16c SGB II:** grant **up to 5,000 €** (Zuschuss) plus loans for equipment (not rent or running costs), only for full-time self-employment.
  - Steps: Businessplan → Tragfähigkeitsbescheinigung (IHK/HWK/advisor) → apply **before** buying anything.
  - Discretionary benefit. Plus coaching (Abs. 2) and Einstiegsgeld.
  - The residence title must allow self-employment (Duldung/Gestattung usually doesn't).
- **Kinderzuschlag:** up to 297 €/child/month (unchanged in 2026).
  - Minimum gross income: 900 € for couples, 600 € for single parents. Requires Kindergeld.
  - Can be combined with Wohngeld, but **not** with Grundsicherungsgeld. 6-month approval periods. KiZ-Lotse calculator. Brings BuT and Kita fee exemption with it.
  - The **Persian page already has a KiZ video**. Don't suggest it again.
- **§ 2 Abs. 3 AufenthG:** Kindergeld, KiZ, Elterngeld etc. do not count as public funds for residence purposes; **Wohngeld does count**.
- **Kindergeld with Duldung/Gestattung:** usually none (§ 62 Abs. 2 EStG; among the Duldung types only § 60d).
- **Wohngeld:** § 3 Abs. 5 WoGG allows Duldung and Gestattung in principle; excluded while receiving AsylbLG (§ 7 WoGG); priority check if it would cover the need. In a Heim, Wohngeld usually doesn't help (no rent).
- **AsylbLG with work:**
  - § 7 Abs. 3: 25 % of earned income is not counted (cap ½ of Regelbedarf level 1, about 200 €). Werbungskosten are deducted.
  - BuT under the AsylbLG. After 36 months Analogleistungen (§ 2 AsylbLG, SGB XII rules, 30 % allowance).
  - People working while in a Heim often have to pay Heim fees (check them).
  - With their own flat, rent becomes part of the need and Wohngeld becomes possible. Get the Mietobergrenze from the Sozialamt first.
- **Nebenkostenabrechnung:** 12-month deadline (§ 556 Abs. 3 BGB); pay "unter Vorbehalt"; Mieterverein.
- **Kündigung of a rental contract:** 3 months, in writing.

**Creator Rewards (TikTok):** 10k followers, 100k views in 30 days, account at least 30 days old, videos over 1 minute. About 0.5–2 $ per 1,000 qualified views (For You feed, more than 5 s, unique). Viewer location matters a lot.

---

## 7. Completed videos (both pages) – do not suggest again
**Persian (Wegweiser Deutschland):**
- Kinderzuschlag
- Jobcenter letter
- Steuer 2022
- Einbürgerung (voice)
- Niederlassung (voice)
- Aufenthalt 25-1-2-3
- 25-5-a-b
- Karte (what's on your card, 20.10)
- Einstiegsgeld (20.10)
- 5 Komak Jobcenter (21.10)
- Beschäftigungsduldung (21.10)
- 22 vs 23 (22.10)
- 16c Selbstständig (22.10)
- Besuchsvisum (22.10)
- 25.2 subsidiär (22.10)
- the "5 Kalame" and "Termin" series (weak)

**Kurdish (Wegweiser.Kurdî):**
- Einbürgerung
- Kinderzuschlag
- 25.3 (Daimi)
- 25.5
- 25.2 subsidiär (says "1 year" – outdated)
- Behinderung-Daimi
- AsylG 3 vs 4
- Ausbildungsduldung (reply)
- Steuer2022
- Safar 1/2/3 (travel)
- Aufenthalt 25-1-2-3
- 25-5-a-b
- Pass (reply)
- Spurwechsel
- Salakan (which years count)
- 25b Abs. 4
- Duldung types
- Einstiegsgeld
- 5 Yarmati Jobcenter
- Beschäftigungsduldung
- Series "one residence, one video": 25a, 25b, 25.5
- 16c Selbstständig
- Besuchsvisum

**Stories:** DM rules (Kurdish + Persian), heart story (Kurdish), polls, etc.

## 8. Open tasks / backlog (priority)
1. **Persian § 28:** script `v7/p28.txt` is ready and waiting for audio. Cover: "§ 28" big, "فقط ۳ سال تا اقامت دائم!" ("only 3 years to permanent residence!").
2. **Kurdish series "یەک ئیقامە، یەک ڤیدیۆ"** still open: 25.1, 26.4, 26.3, 16g, 19d, 31, 28, Fiktionsbescheinigung, 24. The scripts were written only in chat on 21.10 and are **lost**, so rewrite them (same pattern as `v7/k25a.txt`, `v7/k255.txt`).
   - **24 must say 04.03.2028.**
   - § 28 for Kurdish: the Persian `p28.txt` as a template.
3. **Persian and Kurdish Chancenkarte:** scripts were written earlier, but the texts are lost. Rewrite and check the current status first (as of 19.10: 6 points, A1/B2, 1,091 €/month blocked account).
4. **Pinned comments** for the correction "subsidiär 3 years since 27.02.2024" under the Persian "Karte" video and the Kurdish 25.2 video (suggested to the user; check whether he did it).
5. **Topics from the comments:**
   - 18b/Blue Card for Kurdish (On Road).
   - § 28 (Persian + Kurdish; Ahmed Agha, Blume25o).
   - Persian "5 mistakes with the Jobcenter".
   - Rundfunkbeitrag exemption (first suggestion for "hidden money").
   - Unterhaltsvorschuss.
   - Mehrbedarf.
   - Rentenerstattung.
   - Fiktionsbescheinigung/Untätigkeitsklage.
   - Schufa/Inkasso/P-Konto.
   - Kündigung/Krankschreibung.
6. **Old idea lists** (Arbeit & Arbeitsrecht, full topic pool, deep-dive pool 2) are in `docs/Handoff-alt-18-22Okt.md`.
7. **Unverified:** exact Art. 23 residence title after GEAS; § 32 Kindernachzug; § 33a Unterhalt.

## 11. Setup in a new session
```bash
mkdir -p /home/claude/wegweiser && cd /home/claude/wegweiser && unzip -o <path>/Wegweiser-Projekt-Komplett.zip
# Inter font (Latin text in Persian reels):
sudo mkdir -p /usr/share/fonts/opentype/inter && sudo cp fonts_sys/inter/*.otf /usr/share/fonts/opentype/inter/   # if not present
# DejaVu Sans Mono (remark box) usually exists: /usr/share/fonts/truetype/dejavu/
# Vazirmatn is included under fontdl/vz/fonts/ttf/ (Persian). Kurdish uses the same fonts (see batch2/kbase.py).
pip install pillow --break-system-packages   # if missing; PIL needs RAQM (libraqm) for Arabic shaping
which ffmpeg  # needed
```
- The paths are hard-coded to `/home/claude/wegweiser` (`sys.path.insert` in batch2, tax2, wohngeld). **Unzip exactly there.**
- Alignment tool: `tools/adp.py`.
- Quick test: `cd batch2 && python3 kgen.py ks_besuch ../v7/kbesuch.wav ../out/t.mp4 --frames 5`. WAVs are not in the zip (too large), so test with any WAV, or render a cover only (`python3 covkb.py`).
- Logos: `brand_k/Kurdi-Profilbild.jpg` (Kurdish), `aof/wegweiser-deutschland-logo.png` (Persian).
- **Zip contents:**
  - `batch2/` (all specs/renderers/covers/stories), `tax2/render.py` (base), `wohngeld/` (icons), `covers/`, `kv4/`, `aof/`, `brand/`, `brand_k/`, `riester/`, `sparen/`, `sparbuch/`
  - `fontdl/vz`, `fonts_sys/inter`
  - `kb/wissen.html`
  - `v7/*.txt` (all scripts)
  - `tools/adp.py`
  - `docs/` (old handoff)
- After every change: append a line to this file and re-zip:
  `cd /home/claude/wegweiser && zip -qr out/Wegweiser-Projekt-Komplett.zip <dirs> -x "*.wav" "*.mp4" "*__pycache__*"`.

