> **Retired November 24, 2026.** The app became free, so this helper was deleted from Cloudflare (Worker and KV storage). This folder is kept only as a record.

# Glucose Glance download helper (Cloudflare Worker)

Locks the installer download to real purchases.

- Stripe Payment Link (after payment) redirects to `https://glucose-download.<subdomain>.workers.dev/?session_id={CHECKOUT_SESSION_ID}`
- The Worker asks Stripe (read-only restricted key) whether the session is **paid** (or a 100% promo code), **complete**, from the **Glucose Glance Payment Link**, and bought within the last **14 days**.
- Each purchase gets **3 downloads within 48 hours** of first opening the link. After that, or for any wrong/shared/fake link: **"This link has expired."** with the support email.
- KV stores only `{first, count}` per checkout session ID. No email, name or card data. Records delete themselves after 60 days.
- The installer file lives in the same KV namespace under key `file` (KV values can be up to 25 MB, so no R2 / payment card needed).

## Status
Placeholder build. The file is a text placeholder until the real installer is ready. The Stripe Payment Link is NOT pointed here yet.

## Test
`node test/run.mjs` (pretend Stripe and KV, no network).

## Secrets
`STRIPE_KEY` is set only in the Cloudflare dashboard (Workers → glucose-download → Settings → Variables and Secrets). Never commit it, never paste it in chat.
