# Signed & Verified Model Deployment (Minimal)

Flow:
1) Train a tiny classifier and save `model.pkl`
2) Create signature `model.pkl.sig` using a secret key (HMAC-SHA256)
3) The API server verifies signature BEFORE loading the model

Env:
  export SIGNING_SECRET="change_this_in_real_life"

Run:
  pip install -r requirements.txt
  python train_model.py
  python sign_artifact.py model.pkl
  python serve.py   # -> http://127.0.0.1:8000/docs
