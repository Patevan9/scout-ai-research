# Lippy Robotics Labs — Main Website

The studio's front door: one page that shows every app, highlights what's in
production (**Tolliver AI**), and links out to each project's own website.

- `index.html` — the whole site (inline CSS + a tiny script, no build step)
- `assets/` — Labs logo, favicons, Tolliver and Rollabop app icons

## Where each button goes

| Project | Status shown | Links to |
|---|---|---|
| Tolliver | In production | https://patevan9.github.io/lippyrobotics.github.io/ (+ Download, What's new, Support, FAQ, Privacy) |
| Rollabop | Coming to Android | https://patevan9.github.io/rollabop-website/ |
| BreatheFrame | In development | https://github.com/Patevan9/BreatheFrame |
| Lab Articles | Updated regularly | https://patevan9.github.io/lippy-articles/ |

Contact: lippyroboticslabs@gmail.com, Discord, Facebook (same links as the Tolliver site).

## Putting it live (recommended)

The best home is the account's root site, **https://patevan9.github.io/**,
because that address is short and every other project already lives under it.

1. Copy `index.html` and the `assets/` folder into the root of the
   `Patevan9/patevan9.github.io` repo.
2. **Leave `app-ads.txt` and `.nojekyll` exactly as they are** — AdMob needs
   `app-ads.txt` at the root. The new files sit next to it without touching it.
3. Commit to `main`. GitHub Pages republishes in a minute or two.

## Changing things later

- **Rollabop launches on Google Play:** in `index.html`, change the Rollabop
  pill from `class="pill soon">Coming to Android` to
  `class="pill live">Available now` and add the Play Store link as a button.
- **New app:** copy one `<article class="card">…</article>` block in the
  "Apps & projects" section and edit the name, text, icon and links.
- **Colours:** all in the `:root { … }` block at the top of the `<style>`.

---

Lippy Robotics Labs
Copyright © 2026 Patrick Evan Lippy. All rights reserved.
