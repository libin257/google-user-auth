#!/usr/bin/env python3
"""Exchange a Google OAuth authorization code for a user token JSON."""
import argparse
import json
import urllib.parse
import urllib.request
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--code", required=True)
    parser.add_argument("--client-json", default="/root/.openclaw/skills/google-user-auth/google-oauth-client.json")
    parser.add_argument("--output", default="/root/.openclaw/skills/google-user-auth/google-user-token.json")
    parser.add_argument("--redirect-uri", default="http://localhost:8765/")
    parser.add_argument("--scopes", required=True)
    args = parser.parse_args()

    cfg = json.loads(Path(args.client_json).read_text())
    client = cfg.get("installed") or cfg.get("web") or cfg
    body = urllib.parse.urlencode({
        "code": args.code,
        "client_id": client["client_id"],
        "client_secret": client["client_secret"],
        "redirect_uri": args.redirect_uri,
        "grant_type": "authorization_code",
    }).encode()
    request = urllib.request.Request(
        client.get("token_uri", "https://oauth2.googleapis.com/token"),
        data=body,
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        token = json.loads(response.read())
    if not token.get("refresh_token"):
        raise SystemExit("Google response did not contain refresh_token")

    output = {
        "client_id": client["client_id"],
        "client_secret": client["client_secret"],
        "refresh_token": token["refresh_token"],
        "scope": token.get("scope", args.scopes),
        "token_uri": client.get("token_uri", "https://oauth2.googleapis.com/token"),
    }
    path = Path(args.output)
    path.write_text(json.dumps(output, indent=2) + "\n")
    path.chmod(0o600)
    print(f"SAVED={path}")


if __name__ == "__main__":
    main()
