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
| Tolliver | In development · Not yet available · planned $9.99 one-time, not on sale | https://patevan9.github.io/lippyrobotics.github.io/ |
| Tolliver AI | Ongoing research — goal not yet achieved | (no link yet) |
| BreatheFrame | In development · planned free & open source | https://github.com/Patevan9/BreatheFrame |

Lab Articles is intentionally **not** linked from this site. The articles repo and
site are untouched.

## Images — where they come from

- `assets/labs-logo.png`, favicons — resized from the existing Lippy Robotics Labs logo
- `assets/tolliver-icon.png` — the existing Tolliver app icon
- `assets/rollabop/rollabop-wordmark.webp`, `galaxy-ball.webp` — official art from `rollabop-website`
- `assets/rollabop/rollabop-gameplay.mp4` (silent, ~0.6 MB) and `rollabop-tray.webp` —
  cropped from the **official Rollabop portrait trailer** (8.5s–34s), labelled on the page
  as "From the official Rollabop trailer"
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
