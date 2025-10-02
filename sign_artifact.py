import os, hmac, hashlib, sys, base64

def sign_file(path: str, secret: bytes) -> str:
    h = hmac.new(secret, digestmod=hashlib.sha256)
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return base64.b64encode(h.digest()).decode()

if __name__ == "__main__":
    secret = os.getenv("SIGNING_SECRET", "").encode()
    if not secret:
        raise SystemExit("ERROR: set SIGNING_SECRET env var.")
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python sign_artifact.py <file>")
    sig = sign_file(sys.argv[1], secret)
    with open(sys.argv[1] + ".sig", "w") as f:
        f.write(sig)
    print("Wrote", sys.argv[1] + ".sig")
