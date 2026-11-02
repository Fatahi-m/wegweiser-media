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
