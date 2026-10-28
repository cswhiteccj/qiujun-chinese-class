// Draft integration: authenticated, private student audio upload preparation.
// Requires private Supabase Storage bucket 'student-pronunciation' with MIME and 25MB size limits.
// Deploy ONLY after verifying auth configuration, storage policies, and end-to-end tests.
// This endpoint does not call Google Cloud or grade pronunciation.
import { createClient } from "npm:@supabase/supabase-js@2";

const ALLOWED = new Set(["audio/mpeg", "audio/mp3", "audio/mp4", "video/mp4"]);
const MAX_BYTES = 25 * 1024 * 1024;
const BUCKET = "student-pronunciation";
const json = (value: unknown, status = 200) =>
  new Response(JSON.stringify(value), { status, headers: { "content-type": "application/json", "cache-control": "no-store" } });

Deno.serve(async (req) => {
  if (req.method !== "POST") return json({ error: "Method not allowed" }, 405);
  const auth = req.headers.get("Authorization") ?? "";
  if (!/^Bearer\s+\S+$/.test(auth)) return json({ error: "Login required" }, 401);
  const url = Deno.env.get("SUPABASE_URL");
  const anon = Deno.env.get("SUPABASE_ANON_KEY");
  const adminKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
  if (!url || !anon || !adminKey) return json({ error: "Server not configured" }, 503);
  const userClient = createClient(url, anon, { global: { headers: { Authorization: auth } } });
  const { data: { user }, error: userError } = await userClient.auth.getUser();
  if (userError || !user) return json({ error: "Invalid session" }, 401);
  let body: { contentType?: string; sizeBytes?: number; assignmentId?: string };
  try { body = await req.json(); } catch { return json({ error: "Invalid JSON" }, 400); }
  if (!body || !ALLOWED.has(body.contentType ?? "") || !Number.isSafeInteger(body.sizeBytes)
    || (body.sizeBytes ?? 0) <= 0 || (body.sizeBytes ?? 0) > MAX_BYTES)
    return json({ error: "Unsupported format or size (25MB max)" }, 400);
  // TODO before production: validate assignmentId against authenticated course membership,
  // rate-limit attempts, enforce bucket-level file size/MIME limits and storage retention.
  // Do not expose this endpoint to students until those safeguards are implemented.
  if (!body.assignmentId || !/^[a-zA-Z0-9_-]{1,80}$/.test(body.assignmentId))
    return json({ error: "Invalid assignment ID" }, 400);
  const ext = body.contentType === "audio/mpeg" || body.contentType === "audio/mp3" ? "mp3" : "mp4";
  const path = `${user.id}/${body.assignmentId}/${crypto.randomUUID()}.${ext}`;
  const admin = createClient(url, adminKey);
  const { data, error } = await admin.storage.from(BUCKET).createSignedUploadUrl(path);
  if (error || !data) return json({ error: "Private upload unavailable" }, 503);
  return json({ bucket: BUCKET, path, token: data.token, expiresInSeconds: 7200 });
});
