# Wegweiser media

Public video hosting for publishing Reels to Instagram @wegweiser.deutschland via vidIQ.

## Posting queue (`queue.json`)
A scheduled task publishes the next item with `"posted": false`, in order, then sets `"posted": true` and the permalink and pushes.

Steps for one run:
1. `git pull`, read `queue.json`, take the first item with `posted == false`. If none: do nothing.
2. vidIQ `vidiq_video_upload` with `url` = item.url → get `videoUrl`.
3. vidIQ `vidiq_instagram_publish_reel` with platformAccountId = item.account, videoUrl, caption = item.caption exactly. Continue with containerId until PUBLISHED (wait ~5 s between calls). Never republish on error.
4. Set posted=true and permalink, commit, push.


## Kurdish queue (`queue-ku.json`)
Same procedure for Instagram @wegweiser_kurdi (account 28280473388298992), run by a separate scheduled task.

## Persian covers v2 (`archive/fa/v2/`, kit `archive/fa/kit/fa_covers.py`)
Designed covers 1080x1920 (navy brand frame, big headline, per-topic illustration, key content inside y=285..1635 for the grid crop).
For a reel without a v2 cover: add a function to `fa_covers.py` modeled on the existing ones (headline from the caption/video, one illustration: rcard, passport, coins, emoji, steps...), register it in JOBS as `<name>` (= file name without `-Reel.mp4`), run `python3 fa_covers.py <name>` → `archive/fa/v2/cover-<name>.jpg`, check it visually, commit.

## Kurdish covers v2 (`archive/ku/v2/`, kit `archive/ku/kit/ku_covers.py`)
Same idea as the Persian kit but in the Kurdish brand (cream, sun, Kurdish-flag waves, green/red/gold); reuses helpers from `fa_covers.py`. Add a function, register it in JOBS as `<name>`, run `python3 ku_covers.py <name>` → `archive/ku/v2/cover-<name>.jpg`.
