import os, hmac, hashlib, base64, joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

MODEL_PATH = "model.pkl"
SIG_PATH = MODEL_PATH + ".sig"

def verify_signature(path: str, sig_path: str, secret: bytes) -> bool:
    h = hmac.new(secret, digestmod=hashlib.sha256)
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    calc = base64.b64encode(h.digest()).decode()
    try:
        with open(sig_path, "r") as f:
            stored = f.read().strip()
    except FileNotFoundError:
        return False
    return hmac.compare_digest(calc, stored)

# Load only after verifying
secret = os.getenv("SIGNING_SECRET", "").encode()
if not secret:
    raise SystemExit("ERROR: set SIGNING_SECRET env var.")

if not verify_signature(MODEL_PATH, SIG_PATH, secret):
    raise SystemExit("ABORT: signature verification FAILED.")

model = joblib.load(MODEL_PATH)

class IrisIn(BaseModel):
    samples: List[List[float]]  # shape: [n, 4]

app = FastAPI(title="Signed Model Inference (Minimal)")

@app.post("/predict")
def predict(inp: IrisIn):
    try:
        preds = model.predict(inp.samples).tolist()
        return {"ok": True, "predictions": preds}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
