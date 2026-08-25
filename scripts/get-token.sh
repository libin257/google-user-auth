#!/usr/bin/env bash
set -euo pipefail

GOOGLE_SCOPE="${1:-https://www.googleapis.com/auth/analytics.readonly}"
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
GOOGLE_USER_AUTH_ROOT=$(cd "${SCRIPT_DIR}/.." && pwd)
TOKEN_JSON="${GOOGLE_USER_AUTH_ROOT}/google-user-token.json"

[[ -f "${TOKEN_JSON}" ]] || { echo "Missing ${TOKEN_JSON}" >&2; exit 1; }

client_id=$(jq -er '.client_id' "${TOKEN_JSON}")
client_secret=$(jq -er '.client_secret' "${TOKEN_JSON}")
refresh_token=$(jq -er '.refresh_token' "${TOKEN_JSON}")
token_uri=$(jq -er '.token_uri // "https://oauth2.googleapis.com/token"' "${TOKEN_JSON}")

curl -fsS -X POST "${token_uri}" \
  --data-urlencode "client_id=${client_id}" \
  --data-urlencode "client_secret=${client_secret}" \
  --data-urlencode "refresh_token=${refresh_token}" \
  --data-urlencode "grant_type=refresh_token" \
  | jq -er '.access_token | select(length > 0)'
