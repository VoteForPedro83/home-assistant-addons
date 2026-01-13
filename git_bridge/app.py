from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="Git Bridge (PR Bot)", version="1.0.3")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/webhook")
async def webhook(payload: dict):
    return JSONResponse({"received": True, "keys": list(payload.keys())})
