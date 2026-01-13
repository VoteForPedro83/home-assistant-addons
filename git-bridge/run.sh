#!/usr/bin/env sh
set -eu

python3 - <<'PY'
import json, pathlib, sys
p = pathlib.Path("/data/options.json")
if not p.exists():
    print("Missing /data/options.json", file=sys.stderr)
    sys.exit(1)
opts = json.loads(p.read_text())
required = ["api_key","github_token","owner","repo","base_branch"]
missing = [k for k in required if not opts.get(k)]
if missing:
    print(f"Missing required options: {missing}", file=sys.stderr)
    sys.exit(1)
PY

exec uvicorn app:app --host 0.0.0.0 --port 8080
