// Glucose Glance download helper (Cloudflare Worker)
//
// After a buyer pays with the Stripe Payment Link, Stripe sends them here with
// their Checkout Session ID:   /?session_id=cs_live_...
// This Worker:
//   1. asks Stripe (read-only key) whether that purchase is paid and is Glucose Glance,
//   2. allows MAX_DOWNLOADS downloads within WINDOW_HOURS of the first visit,
//   3. otherwise shows "This link has expired."
//
// Stored in KV per purchase (key "dl:<session id>"): first visit time and download count.
// No email, name or card details are stored. Records delete themselves after RECORD_TTL_DAYS.
//
// Settings (wrangler.jsonc "vars"):  PAYMENT_LINK_ID, MAX_DOWNLOADS, WINDOW_HOURS,
//   START_WITHIN_DAYS, FILE_NAME, SUPPORT_EMAIL, SITE_URL
// Secret (set in the Cloudflare dashboard, never in code): STRIPE_KEY (restricted, read-only)
// KV binding: DL   (holds the file at key "file" and the per-purchase records)

const RECORD_TTL_DAYS = 60;
const SESSION_RE = /^cs_(live|test)_[A-Za-z0-9]{10,200}$/;

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (request.method !== "GET" && request.method !== "HEAD") {
      return new Response("Method not allowed", { status: 405, headers: { Allow: "GET, HEAD" } });
    }
    if (url.pathname === "/robots.txt") {
      return new Response("User-agent: *\nDisallow: /\n", { headers: { "content-type": "text/plain" } });
    }
    if (url.pathname !== "/" && url.pathname !== "/download") {
      return page(env, 404, "Page not found", `<p>This page does not exist.</p>`);
    }

    const sid = url.searchParams.get("session_id") || "";
    if (!SESSION_RE.test(sid)) return expired(env);

    const settings = readSettings(env);
    const key = "dl:" + sid;
    let rec = await env.DL.get(key, "json");

    if (!rec) {
      // First time we see this purchase: confirm it with Stripe.
      const ok = await verifyWithStripe(env, sid, settings);
      if (ok === "error") return tryLater(env);
      if (!ok) return expired(env);
      rec = { first: Date.now(), count: 0 };
      await save(env, key, rec);
    }

    const ageMs = Date.now() - rec.first;
    const windowMs = settings.windowHours * 3600 * 1000;
    const left = settings.maxDownloads - rec.count;
    if (ageMs > windowMs || left <= 0) return expired(env);

    if (url.pathname === "/") {
      const hoursLeft = Math.max(1, Math.ceil((windowMs - ageMs) / 3600000));
      const src = env.SOURCE_URL
        ? `<p class="small">Installer source code: <a href="${esc(env.SOURCE_URL)}">${esc(env.SOURCE_URL)}</a></p>` : "";
      return page(env, 200, "Your Glucose Glance download", `
        <p class="big">Thank you for buying Glucose Glance!</p>
        <p><a class="btn" href="/download?session_id=${encodeURIComponent(sid)}">Download</a></p>
        <ol>
          <li>Tap <b>Download</b> on your Android phone.</li>
          <li>Open the file. If asked, allow installing from this source.</li>
          <li>Open <b>Glucose Glance Installer</b> and follow the steps with pictures.</li>
        </ol>
        <p>Phone and watch on the same Wi-Fi. Keep Bluetooth on.</p>
        <p>Need help? <a href="mailto:${esc(env.SUPPORT_EMAIL)}?subject=Glucose%20Glance">${esc(env.SUPPORT_EMAIL)}</a></p>
        <p class="small">This link works for ${left} more download${left === 1 ? "" : "s"} within the next ${hoursLeft} hour${hoursLeft === 1 ? "" : "s"}. Please keep it private.</p>
        ${src}`);
    }

    // /download
    const file = await env.DL.getWithMetadata("file", "arrayBuffer");
    if (!file || !file.value) return tryLater(env);
    if (request.method === "GET") {
      rec.count += 1;
      await save(env, key, rec);
    }
    const name = (file.metadata && file.metadata.name) || settings.fileName;
    return new Response(request.method === "HEAD" ? null : file.value, {
      headers: {
        "content-type": (file.metadata && file.metadata.type) || "application/octet-stream",
        "content-disposition": `attachment; filename="${name.replace(/"/g, "")}"`,
        "cache-control": "no-store",
        "x-robots-tag": "noindex",
      },
    });
  },
};

function readSettings(env) {
  return {
    paymentLink: env.PAYMENT_LINK_ID,
    maxDownloads: Number(env.MAX_DOWNLOADS || 3),
    windowHours: Number(env.WINDOW_HOURS || 48),
    startWithinDays: Number(env.START_WITHIN_DAYS || 14),
    fileName: env.FILE_NAME || "Glucose-Glance-Installer.apk",
  };
}

// Returns true (good purchase), false (not valid), or "error" (Stripe unreachable).
async function verifyWithStripe(env, sid, s) {
  let res;
  try {
    res = await fetch("https://api.stripe.com/v1/checkout/sessions/" + encodeURIComponent(sid), {
      headers: { Authorization: "Bearer " + env.STRIPE_KEY },
    });
  } catch (e) {
    return "error";
  }
  if (res.status === 404 || res.status === 400) return false;
  if (!res.ok) return "error";
  const cs = await res.json();
  const paid = cs.payment_status === "paid" || cs.payment_status === "no_payment_required";
  const rightProduct = !!s.paymentLink && cs.payment_link === s.paymentLink;
  const complete = cs.status === "complete";
  const recent = typeof cs.created === "number" &&
    Date.now() / 1000 - cs.created <= s.startWithinDays * 86400;
  return paid && rightProduct && complete && recent;
}

async function save(env, key, rec) {
  await env.DL.put(key, JSON.stringify(rec), { expirationTtl: RECORD_TTL_DAYS * 86400 });
}

function expired(env) {
  return page(env, 410, "This link has expired", `
    <p class="big">This link has expired.</p>
    <p>Download links work for a short time after purchase, and only for the person who bought Glucose Glance.</p>
    <p>If you bought Glucose Glance and need help, please email
       <a href="mailto:${esc(env.SUPPORT_EMAIL)}?subject=Glucose%20Glance%20download">${esc(env.SUPPORT_EMAIL)}</a>
       and we will be glad to help.</p>`);
}

function tryLater(env) {
  return page(env, 503, "Please try again", `
    <p class="big">Something went wrong on our side.</p>
    <p>Please try again in a few minutes. Your download has not been used up.
       If it keeps happening, email <a href="mailto:${esc(env.SUPPORT_EMAIL)}">${esc(env.SUPPORT_EMAIL)}</a>.</p>`);
}

function esc(s) {
  return String(s || "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

function page(env, status, title, body) {
  const site = esc(env.SITE_URL || "https://lippyroboticslabs.com/glucose-glance/");
  return new Response(`<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>${esc(title)} · Glucose Glance</title>
<style>
  :root { color-scheme: dark; }
  body { margin: 0; background: #070a24; color: #f4f6ff; font: 20px/1.6 "Atkinson Hyperlegible", system-ui, sans-serif; }
  main { max-width: 640px; margin: 0 auto; padding: 48px 20px; }
  h1 { font-size: 1.5rem; margin: 0 0 24px; color: #8fe9b4; }
  .big { font-size: 1.6rem; font-weight: 700; margin: 0 0 16px; }
  p { color: #dfe3ff; }
  a { color: #8fe9b4; }
  .btn { display: inline-block; margin: 12px 0; padding: 16px 28px; border-radius: 999px; background: #3ddc84; color: #04210f; font-weight: 700; text-decoration: none; }
  .btn:focus-visible, a:focus-visible { outline: 3px solid #ffc83d; outline-offset: 3px; }
  .small, footer { font-size: 0.95rem; color: #9aa3d6; }
  ol { padding-left: 1.4em; color: #dfe3ff; } ol li { margin-bottom: 10px; }
  footer { margin-top: 40px; }
</style></head>
<body><main>
  <h1>Glucose Glance</h1>
  ${body}
  <footer><a href="${site}">Glucose Glance website</a> · Lippy Robotics Labs</footer>
</main></body></html>`, {
    status,
    headers: { "content-type": "text/html; charset=utf-8", "cache-control": "no-store", "x-robots-tag": "noindex", "referrer-policy": "no-referrer" },
  });
}
