"""Draft Google Cloud Run speech backend. Not production-ready: require private invocation and validated job permissions."""
import os
import subprocess
import tempfile
from pathlib import Path

import httpx
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field
from google.cloud import speech, texttospeech

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
SUPABASE_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
BUCKET = "student-pronunciation"
MAX_DOWNLOAD = 25 * 1024 * 1024

class Analyze(BaseModel):
    # The path must belong to the authenticated user. Assignment eligibility still needs
    # server-side database verification before exposing this service to students.
    path: str = Field(min_length=4, max_length=300)

async def authorized_user(token: str):
    if not SUPABASE_URL:
        raise HTTPException(503, "Backend not configured")
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"{SUPABASE_URL}/auth/v1/user", headers={
            "Authorization": f"Bearer {token}", "apikey": os.environ.get("SUPABASE_ANON_KEY", "")
        })
    if r.status_code != 200 or not r.json().get("id"):
        raise HTTPException(401, "Invalid login")
    return r.json()["id"]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/transcribe")
async def transcribe(payload: Analyze, authorization: str | None = Header(default=None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Missing bearer token")
    token = authorization.split(" ", 1)[1]
    uid = await authorized_user(token)
    if not payload.path.startswith(uid + "/") or ".." in payload.path or not payload.path.lower().endswith((".mp3", ".mp4")):
        raise HTTPException(403, "Invalid path")
    # TODO: enforce assignment membership, durable quota, replay prevention and rate limits
    # before any real student-facing deployment.
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(
            f"{SUPABASE_URL}/storage/v1/object/authenticated/{BUCKET}/{payload.path}",
            headers={"Authorization": f"Bearer {token}", "apikey": os.environ.get("SUPABASE_ANON_KEY", "")}
        )
    if resp.status_code != 200:
        raise HTTPException(403, "Recording not accessible")
    if len(resp.content) > MAX_DOWNLOAD:
        raise HTTPException(413, "Recording too large")
    with tempfile.TemporaryDirectory() as tempdir:
        src = Path(tempdir) / ("recording.mp4" if payload.path.lower().endswith(".mp4") else "recording.mp3")
        src.write_bytes(resp.content)
        output = Path(tempdir) / "audio.flac"
        # 60 seconds maximum, mono 16kHz; reject invalid input with ffmpeg.
        try:
            subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(src),
                            "-t", "60", "-vn", "-ac", "1", "-ar", "16000", "-c:a", "flac",
                            str(output)], check=True, capture_output=True, timeout=35)
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            raise HTTPException(422, "Invalid or unsupported audio")
        audio = output.read_bytes()
    if len(audio) > 10_000_000:
        raise HTTPException(413, "Audio exceeds synchronous recognition limit")
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        language_code="cmn-Hant-TW",
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        enable_word_time_offsets=True,
    )
    try:
        recognized = client.recognize(config=config, audio=speech.RecognitionAudio(content=audio), timeout=60)
    except Exception:
        raise HTTPException(502, "Speech recognition failed")
    return {"transcript": " ".join(r.alternatives[0].transcript for r in recognized.results if r.alternatives),
            "notice": "Transcription only; not pronunciation, tone or phoneme scoring."}
