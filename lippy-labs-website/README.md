# Lippy Robotics Labs — Main Website (draft, not published)

The studio's front door: **Big ideas. Small screens. Real enjoyment.**

One page, in this order:

1. **Hero** — mission, metallic gear logo, quick links to each project
2. **Rollabop** (featured, first priority) — walnut / brass / glass, real gameplay loop
3. **Tolliver** — the companion; expressive eyes that follow the pointer
4. **Tolliver AI** — the research ambition (honest "not achieved yet" note)
5. **BreatheFrame** — animated *concept illustration* with a pause/play button
6. **What we believe** — enjoyment without pressure, fair value, privacy, accessibility
7. **The Story Behind the Lab** — Patrick's story, in his own voice
8. **Explore, connect, support** — project sites, Discord, Facebook, email, donate

`index.html` is the whole site (inline CSS + one small script, no build step).

## Project statuses shown (keep these accurate)

| Project | Status on the page | Links to |
|---|---|---|
| Rollabop | In closed testing · Android · free-to-play | https://patevan9.github.io/rollabop-website/ |
| Rollabop beta (step 1) | Join the Google Group first | https://groups.google.com/g/rollabop-beta-testers |
| Rollabop beta (step 2) | Then opt in / install, if eligible | https://play.google.com/apps/testing/com.lippyrobotics.rollabop |
| Tolliver | In development · Not yet available · planned $9.99 one-time, not on sale | Discord (see note below) |
| Tolliver AI | Ongoing research — goal not yet achieved | (no link yet) |
| BreatheFrame | In development · planned free & open source | https://github.com/Patevan9/BreatheFrame |

**Tolliver website not linked (on purpose):** the current Tolliver site still presents the app as
purchasable and downloadable. Until that site is corrected, this homepage sends Tolliver visitors to
Discord instead. The only Tolliver-site link left is the Stripe donate page
(`lippyrobotics.github.io/donate.html`) — note its menu still includes "Download".

Lab Articles is intentionally **not** linked from this site. The articles repo and
site are untouched.

## Images — where they come from

- `assets/labs-logo.png`, favicons — resized from the existing Lippy Robotics Labs logo
- `assets/tolliver-icon.png` — the existing Tolliver app icon
- `assets/rollabop/rollabop-wordmark.webp`, `galaxy-ball.webp` — official art from `rollabop-website`
- **Rollabop gameplay: none yet, on purpose.** Rule: anything shown as Rollabop gameplay must
  come from a real recording of the running game. The earlier clip came from the official
  trailer, which is a code-drawn recreation, so it was removed (along with its still image and
  the "Watch the trailer" link). The phone frame now shows the Galaxy Ball art and
  "Real gameplay footage coming soon".
- Tolliver's face, the Tolliver AI network and the BreatheFrame winter scene are drawn
  in code. The BreatheFrame scene is labelled "Concept illustration, not a screenshot of the app."

### Adding the real Rollabop gameplay video

1. On the Galaxy Fold 7 (folded, portrait), open Quick Settings, then **Screen recorder**
   (sound: none). Play 20-40 seconds: balls settling, a drag through the pile, a match.
2. Send the video file. It gets trimmed, cropped to the tray, made silent and compressed
   to under 1 MB as `assets/rollabop/rollabop-gameplay.mp4`, with a still frame from the
   same recording saved as `assets/rollabop/rollabop-gameplay-poster.webp`.
3. In `index.html`, replace the `<div class="rb-soon">` block with the `<video>` block written
   in the comment right above it, and change the caption to
   "Real gameplay, recorded on a Galaxy Fold 7". The page script already plays it only
   while visible and shows controls when reduced motion is on.

When real BreatheFrame screenshots exist, they can replace the concept illustration.

## Motion & accessibility

- All animation stops under the phone/computer "reduce motion" setting
- Animations and the video pause when scrolled off-screen (saves battery)
- BreatheFrame has its own Pause / Bring it to life button
- Large text (18px base), high contrast, skip link, focus rings, 48px+ touch targets

## Publishing (only when Patrick approves)

Recommended home: **https://patevan9.github.io/** (the `Patevan9/patevan9.github.io` repo).
Copy `index.html` and `assets/` into that repo's root. **Never touch `app-ads.txt` or
`.nojekyll`** — AdMob needs `app-ads.txt`.

---

Lippy Robotics Labs
Copyright © 2026 Patrick Evan Lippy. All rights reserved.
