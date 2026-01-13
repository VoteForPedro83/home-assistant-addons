from fastapi import FastAPI, Request
import os
import hmac
import hashlib

app = FastAPI()

# Optional: set these later via add-on options if you want signature verification
GITHUB_WEBHOOK_SECRET = os.environ.get("GITHUB_WEBHOOK_SECRET", "")

@app.get("/health")
def health():
    return {"status": "ok"}

def verify_github_signature(body: bytes, signature_header: str) -> bool:
    """
    Verifies GitHub 'X-Hub-Signature-256' header if a secret is set.
    If no secret is configured, we skip verification.
    """
    if not GITHUB_WEBHOOK_SECRET:
        return True

    if not signature_header or not signature_header.startswith("sha256="):
        return False

    expected = hmac.new(
        GITHUB_WEBHOOK_SECRET.encode("utf-8"),
        body,
        hashlib.sha256,
    ).hexdigest()

    received = signature_header.split("=", 1)[1].strip()
    return hmac.compare_digest(expected, received)

@app.post("/github/webhook")
async def github_webhook(request: Request):
    body = await request.body()
    sig = request.headers.get("X-Hub-Signature-256", "")

    if not verify_github_signature(body, sig):
        return {"ok": False, "error": "invalid signature"}

    # For now, just acknowledge receipt.
    # Later you can parse event type and payload to trigger your PR-bot logic.
    event = request.headers.get("X-GitHub-Event", "unknown")
    return {"ok": True, "event": event}
