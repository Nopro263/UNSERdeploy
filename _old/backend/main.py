from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Any
import os

import deployment

import hashlib
import hmac

def verify_signature(payload_body, secret_token, signature_header):
    """Verify that the payload was sent from GitHub by validating SHA256.

    Raise and return 403 if not authorized.

    Args:
        payload_body: original request body to verify (request.body())
        secret_token: GitHub app webhook token (WEBHOOK_SECRET)
        signature_header: header received from GitHub (x-hub-signature-256)
    """
    if not signature_header:
        raise HTTPException(status_code=403, detail="x-hub-signature-256 header is missing!")
    hash_object = hmac.new(secret_token.encode('utf-8'), msg=payload_body, digestmod=hashlib.sha256)
    expected_signature = "sha256=" + hash_object.hexdigest()
    if not hmac.compare_digest(expected_signature, signature_header):
        raise HTTPException(status_code=403, detail="Request signatures didn't match!")

class PushBody(BaseModel):
    after: str
    base_ref: str
    before: str
    commits: list # we can ignore this
    compare: str
    created: bool
    deleted: bool
    forced: bool
    head_commit: Any
    pusher: Any
    ref: str
    repository: Any



app = FastAPI()

os.environ["SECRET"]

@app.post("/{project:str}/webhook")
async def webhook(project: str, body: PushBody, request: Request):
    verify_signature(await request.body(), os.environ["SECRET"], request.headers.get("x-hub-signature-256"))

    print(project, body)

@app.get("/create/{project:str}")
async def create(project: str, url: str):
    deployment.create_deployment(project, url)