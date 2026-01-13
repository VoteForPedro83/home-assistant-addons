from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="Git Bridge (PR Bot)")

@app.get("/")
def root():
    return {"status": "ok", "service": "git-bridge"}

@app.get("/health")
def health():
    return JSONResponse({"healthy": True})
