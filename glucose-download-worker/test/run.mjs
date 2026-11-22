// Local tests with a pretend Stripe and pretend KV. No network, no real keys.
// Run: node test/run.mjs
import worker from "../src/index.js";
import assert from "node:assert/strict";

const LINK = "plink_TEST";
const now = () => Math.floor(Date.now() / 1000);
const sessions = {
  cs_live_GOODGOODGOOD1: { payment_status: "paid", status: "complete", payment_link: LINK, created: now() },
  cs_live_FREEPROMOCODE: { payment_status: "no_payment_required", status: "complete", payment_link: LINK, created: now() },
  cs_live_UNPAIDUNPAID1: { payment_status: "unpaid", status: "open", payment_link: LINK, created: now() },
  cs_live_DONATIONLINK1: { payment_status: "paid", status: "complete", payment_link: "plink_OTHER", created: now() },
  cs_live_OLDPURCHASE01: { payment_status: "paid", status: "complete", payment_link: LINK, created: now() - 30 * 86400 },
};
let stripeDown = false, stripeCalls = 0;
globalThis.fetch = async (url, opts) => {
  stripeCalls++;
  assert.equal(opts.headers.Authorization, "Bearer sk_fake");
  if (stripeDown) throw new Error("network");
  const id = decodeURIComponent(url.split("/").pop());
  const s = sessions[id];
  return s ? new Response(JSON.stringify(s), { status: 200 }) : new Response("{}", { status: 404 });
};

function kv() {
  const m = new Map();
  return {
    m,
    async get(k, t) { const v = m.get(k); return v == null ? null : t === "json" ? JSON.parse(v.value) : v.value; },
    async getWithMetadata(k) { const v = m.get(k); return v ? { value: v.value, metadata: v.metadata } : { value: null, metadata: null }; },
    async put(k, value, o = {}) { m.set(k, { value, metadata: o.metadata }); },
  };
}
const env = { DL: kv(), STRIPE_KEY: "sk_fake", PAYMENT_LINK_ID: LINK, MAX_DOWNLOADS: "3", WINDOW_HOURS: "48",
  START_WITHIN_DAYS: "14", SUPPORT_EMAIL: "lippyroboticslabs@gmail.com", SITE_URL: "https://lippyroboticslabs.com/glucose-glance/" };
const fileBytes = new TextEncoder().encode("PLACEHOLDER").buffer;
await env.DL.put("file", fileBytes, { metadata: { name: "Glucose-Glance-Installer-PLACEHOLDER.txt", type: "text/plain" } });

const get = (p, method = "GET") => worker.fetch(new Request("https://x.workers.dev" + p, { method }), env);
const text = async (r) => await r.text();
let pass = 0; const t = async (name, fn) => { await fn(); pass++; console.log("ok  -", name); };

await t("no session id -> expired", async () => { const r = await get("/"); assert.equal(r.status, 410); assert.match(await text(r), /This link has expired/); });
await t("garbage session id -> expired, Stripe not called", async () => { const c = stripeCalls; const r = await get("/?session_id=<script>"); assert.equal(r.status, 410); assert.equal(stripeCalls, c); });
await t("unknown session -> expired", async () => { assert.equal((await get("/?session_id=cs_live_NOTREALNOTREAL")).status, 410); });
await t("unpaid -> expired", async () => { assert.equal((await get("/?session_id=cs_live_UNPAIDUNPAID1")).status, 410); });
await t("other product (donation link) -> expired", async () => { assert.equal((await get("/?session_id=cs_live_DONATIONLINK1")).status, 410); });
await t("purchase older than 14 days, never used -> expired", async () => { assert.equal((await get("/?session_id=cs_live_OLDPURCHASE01")).status, 410); });
await t("Stripe unreachable -> try later (503), nothing used up", async () => {
  stripeDown = true; const r = await get("/?session_id=cs_live_GOODGOODGOOD1"); stripeDown = false;
  assert.equal(r.status, 503); assert.equal(env.DL.m.has("dl:cs_live_GOODGOODGOOD1"), false); });
await t("good purchase -> landing page says 3 downloads", async () => { const r = await get("/?session_id=cs_live_GOODGOODGOOD1"); assert.equal(r.status, 200); assert.match(await text(r), /3 more downloads/); ; });
await t("landing page visits do not use downloads; Stripe asked only once", async () => { const c = stripeCalls; await get("/?session_id=cs_live_GOODGOODGOOD1"); assert.equal(stripeCalls, c); assert.match(await text(await get("/?session_id=cs_live_GOODGOODGOOD1")), /3 more downloads/); });
await t("HEAD request does not use a download", async () => { await get("/download?session_id=cs_live_GOODGOODGOOD1", "HEAD"); assert.match(await text(await get("/?session_id=cs_live_GOODGOODGOOD1")), /3 more downloads/); });
await t("download 1..3 give the file", async () => {
  for (let i = 1; i <= 3; i++) { const r = await get("/download?session_id=cs_live_GOODGOODGOOD1"); assert.equal(r.status, 200);
    assert.match(r.headers.get("content-disposition"), /PLACEHOLDER/); assert.equal(await r.text(), "PLACEHOLDER"); } });
await t("4th download -> expired", async () => { assert.equal((await get("/download?session_id=cs_live_GOODGOODGOOD1")).status, 410); assert.equal((await get("/?session_id=cs_live_GOODGOODGOOD1")).status, 410); });
await t("after 48 hours -> expired even with downloads left", async () => {
  await get("/?session_id=cs_live_FREEPROMOCODE");
  const k = "dl:cs_live_FREEPROMOCODE"; const rec = JSON.parse(env.DL.m.get(k).value); rec.first -= 49 * 3600 * 1000; await env.DL.put(k, JSON.stringify(rec));
  assert.equal((await get("/download?session_id=cs_live_FREEPROMOCODE")).status, 410); });
await t("record stores no personal data", async () => { const rec = JSON.parse(env.DL.m.get("dl:cs_live_GOODGOODGOOD1").value); assert.deepEqual(Object.keys(rec).sort(), ["count", "first"]); });
await t("pages are not indexed and not cached", async () => { const r = await get("/"); assert.equal(r.headers.get("x-robots-tag"), "noindex"); assert.equal(r.headers.get("cache-control"), "no-store"); });
console.log(`\n${pass} tests passed`);
