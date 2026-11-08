// Meta Conversions API (CAPI) — Netlify Function
// Rota pública: POST /api/capi
// Variáveis (Netlify → Site configuration → Environment variables):
//   META_PIXEL_ID        (obrigatória) ID do Pixel/dataset
//   META_CAPI_TOKEN      (obrigatória, SECRETA) token de acesso da Conversions API
//   META_GRAPH_VERSION   (opcional) padrão v23.0
//   META_TEST_EVENT_CODE (opcional) código do "Testar eventos" do Gerenciador de Eventos
//   CAPI_ALLOWED_ORIGINS (opcional) origens permitidas, separadas por vírgula

import { createHash } from "node:crypto";

export const config = { path: "/api/capi" };

const ALLOWED_EVENTS = new Set(["Lead"]);
const json = (obj, status = 200) =>
  new Response(JSON.stringify(obj), { status, headers: { "content-type": "application/json", "cache-control": "no-store" } });

const sha256 = (v) => createHash("sha256").update(v).digest("hex");
const clean = (v, max = 200) => (typeof v === "string" ? v.trim().slice(0, max) : "");

function normPhone(raw) {
  let d = clean(raw, 40).replace(/\D/g, "");
  if (d.length < 10) return "";
  if (d.length <= 11) d = "55" + d; // número BR sem DDI
  return d;
}
function normName(raw) {
  return clean(raw, 80)
    .toLowerCase()
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .replace(/[^a-z\s'-]/g, "")
    .trim();
}

export default async (req) => {
  if (req.method !== "POST") return json({ ok: false, error: "method_not_allowed" }, 405);

  const pixelId = process.env.META_PIXEL_ID;
  const token = process.env.META_CAPI_TOKEN;
  if (!pixelId || !token) return json({ ok: false, error: "not_configured" }, 200);

  // Só aceita chamadas vindas do próprio site
  const origin = req.headers.get("origin") || "";
  const allowed = (process.env.CAPI_ALLOWED_ORIGINS || "")
    .split(",").map((s) => s.trim()).filter(Boolean);
  const selfOrigin = new URL(req.url).origin;
  if (origin && origin !== selfOrigin && !allowed.includes(origin)) return json({ ok: false, error: "forbidden_origin" }, 403);

  let body;
  try {
    const text = await req.text();
    if (text.length > 8000) return json({ ok: false, error: "payload_too_large" }, 413);
    body = JSON.parse(text);
  } catch {
    return json({ ok: false, error: "invalid_json" }, 400);
  }

  const eventName = clean(body.event_name, 40);
  if (!ALLOWED_EVENTS.has(eventName)) return json({ ok: false, error: "event_not_allowed" }, 400);
  const eventId = clean(body.event_id, 100);
  if (!eventId) return json({ ok: false, error: "missing_event_id" }, 400);

  const u = body.user || {};
  const phone = normPhone(u.phone);
  const fullName = normName(u.name);
  const [first, ...rest] = fullName.split(/\s+/).filter(Boolean);
  const last = rest.length ? rest[rest.length - 1] : "";

  const fbclid = clean(body.fbclid, 300);
  let fbc = clean(body.fbc, 400);
  if (!fbc && fbclid) fbc = `fb.1.${Date.now()}.${fbclid}`;

  const userData = {
    client_ip_address:
      req.headers.get("x-nf-client-connection-ip") ||
      (req.headers.get("x-forwarded-for") || "").split(",")[0].trim() ||
      undefined,
    client_user_agent: req.headers.get("user-agent") || undefined,
  };
  if (phone) { userData.ph = [sha256(phone)]; userData.external_id = [sha256(phone)]; }
  if (first) userData.fn = [sha256(first)];
  if (last) userData.ln = [sha256(last)];
  userData.country = [sha256("br")];
  const fbp = clean(body.fbp, 200);
  if (fbp) userData.fbp = fbp;
  if (fbc) userData.fbc = fbc;

  const c = body.custom || {};
  const customData = {};
  if (clean(c.content_name)) customData.content_name = clean(c.content_name);
  if (clean(c.content_category)) customData.content_category = clean(c.content_category);
  for (const k of ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term"]) {
    if (clean(c[k])) customData[k] = clean(c[k]);
  }

  const event = {
    event_name: eventName,
    event_time: Math.floor(Date.now() / 1000),
    event_id: eventId, // mesmo ID do Pixel no navegador → deduplicação
    action_source: "website",
    event_source_url: clean(body.event_source_url, 500) || selfOrigin,
    user_data: userData,
    custom_data: customData,
  };

  const payload = { data: [event] };
  if (process.env.META_TEST_EVENT_CODE) payload.test_event_code = process.env.META_TEST_EVENT_CODE;

  const version = process.env.META_GRAPH_VERSION || "v23.0";
  const url = `https://graph.facebook.com/${version}/${encodeURIComponent(pixelId)}/events?access_token=${encodeURIComponent(token)}`;

  try {
    const r = await fetch(url, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(payload) });
    const out = await r.json().catch(() => ({}));
    if (!r.ok) {
      console.error("CAPI erro", r.status, JSON.stringify(out?.error || out));
      return json({ ok: false, error: "meta_error", status: r.status, message: out?.error?.message }, 502);
    }
    return json({ ok: true, events_received: out.events_received, fbtrace_id: out.fbtrace_id });
  } catch (e) {
    console.error("CAPI falha de rede", e?.message);
    return json({ ok: false, error: "network_error" }, 502);
  }
};
