# Geld ohne Filter – automatische YouTube Shorts

Kanal: Geld ohne Filter (@geld-ohne-filter), YouTube channel UCZ1H1Yxr83xUg3tlUVecQAg
Metricool blogId: 7395074 (YouTube verbunden). Zeitzone Europe/Berlin.
Stimme: vidIQ voice "Chris" – voiceId iP95p4xoKVk53GoZ742B.

## Pipeline pro Video (alles in gof/)
1. Thema aus topics.md, Fakten per Websuche prüfen (offizielle Quellen bevorzugt: BMAS, BMG, BMF, Arbeitsagentur, Destatis, Verbraucherzentrale, Gesetzestext). Nichts erfinden.
2. Skript Deutsch, 40–65 s, Hook in Satz 1, du-Form, ALLE Zahlen als Wörter ausgeschrieben (TTS), Paragraphen als "Paragraf ...", ein Gedanke pro Satz, eine Zeile = ein Absatz. Letzter Satz: "Folge für mehr Geld ohne Filter."
   Speichern als work/<slug>.txt
3. vidiq_voiceover_generate(script, voiceId) → poll → durationSeconds + audioUrl. MP3 sofort mit curl nach work/<slug>.mp3 laden (*.amazonaws.com ist freigegeben).
4. Spec work/<slug>.py nach Vorbild kit/examples/kk.py: _, S, TOTAL = align(SCRIPT, '<slug>.mp3') liefert echte Satz-Startzeiten S[i] (Fallback ohne MP3: timings(SCRIPT, TOTAL)); Elemente mit A(...) zu S[i] einblenden, Blöcke bei S[nächster Block] ausblenden. Auf dem Bildschirm Ziffern verwenden (nur das Skript schreibt Zahlen als Wörter). Kurze Texte, groß, fit() für lange Wörter.
   Testframes: python3 <slug>.py <dur> f --frames a,b,c → Read prüfen (kein Überlauf, nichts abgeschnitten).
   Render: python3 <slug>.py <dur> <slug>-silent.mp4   (stumm, Länge = dur)
5. Silent-MP4 nach gof/out/ committen + pushen → vidiq_video_upload(url=https://raw.githubusercontent.com/Fatahi-m/wegweiser-media/main/gof/out/<slug>-silent.mp4)
6. vidiq_compose(format vertical, scenes=[{source: videoUrl, type: video, duration: dur}], voiceover={audioUrl}) → poll → videoUrl
7. Cover nach kit/examples/kk_cover.py (Paragraf/Kernzahl groß im Pill) → gof/out/cover-GoF-<slug>.jpg committen.
8. Metricool createScheduledPost (blogId 7395074, provider youtube, youtubeData type "short", madeForKids false, category EDUCATION, privacy public, Titel ≤ 70 Zeichen mit #Shorts, text = Beschreibung mit 4–6 ✅-Punkten + "Keine Beratung, nur Fakten. Stand: <Monat Jahr>" + Quellen + Hashtags, media=[compose videoUrl], videoThumbnailUrl = raw-URL des Covers).
9. topics.md abhaken, posted.md ergänzen, committen.

Fertiges Video: compose-videoUrl mit curl nach gof/out/<slug>.mp4 laden und dem Nutzer mit SendUserFile schicken (für TikTok/Instagram).
