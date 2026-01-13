import base64
import json
import re
from typing import List, Literal, Optional

import requests
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

with open("/data/options.json", "r") as f:
    OPT = json.load(f)

API_KEY = OPT["api_key"]
GH_TOKEN = OPT["github_token"]
OWNER = OPT["owner"]
REPO = OPT["repo"]
BASE_BRANCH = OPT["base_branch"]
PR_LABEL = OPT.get("pr_label", "ai-change")

GH_API = "https://api.github.com"

app = FastAPI(title="Git Bridge API", version="1.0.0")

ALLOWLIST_PATTERNS = [
    r"^configuration\.yaml$",
    r"^automations\.yaml$",
    r"^scripts\.yaml$",
    r"^scenes\.yaml$",
    r"^packages\/[A-Za-z0-9_\-\/]+\.ya?ml$",
    r"^go2rtc\.yaml\.tpl$",
]

DENYLIST_PATTERNS = [
    r"^\.ssh\/",
    r"^.*\.pem$",
    r"^.*\.key$",
    r"^.*\.env$",
    r"^\.optionb_env$",
    r"^\.go2rtc_env$",
    r"^go2rtc\.yaml$",             # rendered output, not in Git
    r"^bin\/ha_git_pull\.sh$",      # protect GitOps script
]

SECRET_CONTENT_PATTERNS = [
    r"Authorization:\s*Bearer\s+[A-Za-z0-9\-_\.]+",
    r"HA_TOKEN\s*=",
    r"RTSP_PASS\s*=",
    r"rtsp:\/\/[^\/\s]+:[^\/\s]+@",
    r"BEGIN\s+PRIVATE\s+KEY",
]

def _auth(x_api_key: Optional[str]):
    if not x_api_key or x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

def _match_any(patterns: List[str], text: str) -> bool:
    return any(re.match(p, text) for p in patterns)

def _validate_path(path: str):
    if _match_any(DENYLIST_PATTERNS, path):
        raise HTTPException(status_code=400, detail=f"Path denied: {path}")
    if not _match_any(ALLOWLIST_PATTERNS, path):
        raise HTTPException(status_code=400, detail=f"Path not allowed: {path}")

def _validate_content(path: str, content: str):
    for pat in SECRET_CONTENT_PATTERNS:
        if re.search(pat, content, flags=re.IGNORECASE):
            raise HTTPException(status_code=400, detail=f"Secret-like content detected in {path}")

def gh_headers():
    return {
        "Authorization": f"Bearer {GH_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

def gh(url: str, method="GET", **kwargs):
    r = requests.request(method, url, headers=gh_headers(), timeout=30, **kwargs)
    if r.status_code >= 400:
        raise HTTPException(status_code=502, detail=f"GitHub error {r.status_code}: {r.text}")
    return r.json() if r.text else {}

def get_ref_sha(branch: str) -> str:
    data = gh(f"{GH_API}/repos/{OWNER}/{REPO}/git/ref/heads/{branch}")
    return data["object"]["sha"]

def create_branch(new_branch: str, from_branch: str) -> None:
    sha = get_ref_sha(from_branch)
    gh(f"{GH_API}/repos/{OWNER}/{REPO}/git/refs", method="POST",
       json={"ref": f"refs/heads/{new_branch}", "sha": sha})

def upsert_file(branch: str, path: str, content: str, message: str) -> None:
    url = f"{GH_API}/repos/{OWNER}/{REPO}/contents/{path}"
    r = requests.get(url, headers=gh_headers(), params={"ref": branch}, timeout=30)
    sha = None
    if r.status_code == 200:
        sha = r.json().get("sha")
    elif r.status_code != 404:
        raise HTTPException(status_code=502, detail=f"GitHub error {r.status_code}: {r.text}")

    payload = {
        "message": message,
        "content": base64.b64encode(content.encode("utf-8")).decode("ascii"),
        "branch": branch,
    }
    if sha:
        payload["sha"] = sha

    gh(url, method="PUT", json=payload)

def open_pr(base: str, head: str, title: str, body: str) -> dict:
    return gh(f"{GH_API}/repos/{OWNER}/{REPO}/pulls", method="POST",
              json={"title": title, "head": head, "base": base, "body": body})

def add_label(pr_number: int, label: str) -> None:
    gh(f"{GH_API}/repos/{OWNER}/{REPO}/issues/{pr_number}/labels", method="POST",
       json={"labels": [label]})

class Change(BaseModel):
    path: str
    action: Literal["upsert"] = "upsert"
    content: str

class ApplyChangeRequest(BaseModel):
    branch_name: str
    commit_message: str
    changes: List[Change]
    pr_title: str
    pr_body: str

class ApplyChangeResponse(BaseModel):
    head_branch: str
    pr_number: int
    pr_url: str

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/repo/file")
def get_file(path: str, ref: str = BASE_BRANCH, x_api_key: Optional[str] = Header(default=None)):
    _auth(x_api_key)
    _validate_path(path)
    data = gh(f"{GH_API}/repos/{OWNER}/{REPO}/contents/{path}", method="GET", params={"ref": ref})
    content_b64 = data.get("content", "")
    content = base64.b64decode(content_b64).decode("utf-8", errors="replace")
    return {"path": path, "ref": ref, "content": content}

@app.post("/repo/apply", response_model=ApplyChangeResponse)
def apply(req: ApplyChangeRequest, x_api_key: Optional[str] = Header(default=None)):
    _auth(x_api_key)

    for ch in req.changes:
        _validate_path(ch.path)
        _validate_content(ch.path, ch.content)

    create_branch(req.branch_name, BASE_BRANCH)

    for ch in req.changes:
        upsert_file(req.branch_name, ch.path, ch.content, req.commit_message)

    pr = open_pr(BASE_BRANCH, req.branch_name, req.pr_title, req.pr_body)
    pr_number = pr["number"]
    pr_url = pr["html_url"]

    try:
        add_label(pr_number, PR_LABEL)
    except Exception:
        pass

    return ApplyChangeResponse(head_branch=req.branch_name, pr_number=pr_number, pr_url=pr_url)
