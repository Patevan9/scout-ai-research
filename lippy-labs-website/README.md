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
| Rollabop | In closed testing · Android · free-to-play | https://patevan9.github.io/rollabop-website/ (+ `#trailer`) |
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
- `assets/rollabop/rollabop-gameplay.mp4` (silent, ~0.6 MB) and `rollabop-tray.webp` —
  cropped from the **official Rollabop portrait trailer** (8.5s–34s), labelled on the page
  as "Scene from the official Rollabop trailer". Note: that trailer is an animation drawn in
  code (`rollabop-website/src/trailer/`) using recorded ball movements, laid out like the real
  game screen. It is not a screen recording of the game. Swap in a real phone screen
  recording when one is approved.
- Tolliver's face, the Tolliver AI network and the BreatheFrame winter scene are drawn
  in code. The BreatheFrame scene is labelled "Concept illustration, not a screenshot of the app."

When real Rollabop or BreatheFrame screenshots are approved, swap them in.

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
