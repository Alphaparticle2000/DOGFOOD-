#!/bin/bash
# Creates the two DOGFOOD Render services (image runtime) from the local .env.
# Secrets are read from .env and placed only in the HTTP request body.
# Values are extracted with grep (NOT `source`) so shell-special characters
# in the .env can't break parsing.
#
# Render API v1: POST /v1/services. Top-level params: type, name, ownerId,
# image (imagePath), envVars. The env-specific config (env, runtime, region,
# plan, healthCheckPath) goes inside `serviceDetails`.
set -euo pipefail

RENDER_KEY='rnd_nCkdWlCjqBvxtPR7xfYJtLVaci9R'
OWNER='tea-d5f509e3jp1c73blf1ug'
API='https://api.render.com/v1/services'
ENVFILE='/c/Projects/DOGFOOD-/.env'
OUT='/c/Projects/DOGFOOD-'

# --- safe .env reader -------------------------------------------------------
get_env() {
  grep -E "^${1}=" "$ENVFILE" | head -1 | sed "s/^${1}=//"
}
# minimal JSON string escaping (backslash + double-quote)
esc() {
  printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g'
}

SUPABASE_URL="$(esc "$(get_env SUPABASE_URL)")"
SUPABASE_ANON_KEY="$(esc "$(get_env SUPABASE_ANON_KEY)")"
SUPABASE_SERVICE_ROLE_KEY="$(esc "$(get_env SUPABASE_SERVICE_ROLE_KEY)")"
SUPABASE_JWT_SECRET="$(esc "$(get_env SUPABASE_JWT_SECRET)")"
DATABASE_URL="$(esc "$(get_env DATABASE_URL)")"
VITE_SUPABASE_URL="$(esc "$(get_env VITE_SUPABASE_URL)")"
VITE_SUPABASE_ANON_KEY="$(esc "$(get_env VITE_SUPABASE_ANON_KEY)")"

# Predictable default Render domains for the free plan (unique service names).
BACKEND_URL='https://dogfood-backend.onrender.com'
FRONTEND_URL='https://dogfood-frontend.onrender.com'

echo "Creating dogfood-backend ..."
RESP_B=$(curl -sS -X POST "$API" \
  -H "Authorization: Bearer $RENDER_KEY" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d "{
    \"type\": \"web_service\",
    \"name\": \"dogfood-backend\",
    \"ownerId\": \"$OWNER\",
    \"image\": { \"imagePath\": \"docker.io/supremesahil/dogfood-backend:latest\" },
    \"envVars\": [
      { \"key\": \"APP_ENV\", \"value\": \"production\" },
      { \"key\": \"DEBUG\", \"value\": \"false\" },
      { \"key\": \"API_V1_STR\", \"value\": \"/api\" },
      { \"key\": \"BACKEND_HOST\", \"value\": \"0.0.0.0\" },
      { \"key\": \"SUPABASE_URL\", \"value\": \"$SUPABASE_URL\" },
      { \"key\": \"SUPABASE_ANON_KEY\", \"value\": \"$SUPABASE_ANON_KEY\" },
      { \"key\": \"SUPABASE_SERVICE_ROLE_KEY\", \"value\": \"$SUPABASE_SERVICE_ROLE_KEY\" },
      { \"key\": \"SUPABASE_JWT_SECRET\", \"value\": \"$SUPABASE_JWT_SECRET\" },
      { \"key\": \"DATABASE_URL\", \"value\": \"$DATABASE_URL\" },
      { \"key\": \"ALLOWED_ORIGINS\", \"value\": \"$FRONTEND_URL\" }
    ],
    \"serviceDetails\": {
      \"env\": \"image\",
      \"runtime\": \"image\",
      \"region\": \"singapore\",
      \"plan\": \"free\",
      \"healthCheckPath\": \"/health\"
    }
  }")
echo "$RESP_B" > "${OUT}resp_backend.json"

echo "Creating dogfood-frontend ..."
RESP_F=$(curl -sS -X POST "$API" \
  -H "Authorization: Bearer $RENDER_KEY" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d "{
    \"type\": \"web_service\",
    \"name\": \"dogfood-frontend\",
    \"ownerId\": \"$OWNER\",
    \"image\": { \"imagePath\": \"docker.io/supremesahil/dogfood-frontend:latest\" },
    \"envVars\": [
      { \"key\": \"VITE_API_URL\", \"value\": \"$BACKEND_URL\" },
      { \"key\": \"VITE_SUPABASE_URL\", \"value\": \"$VITE_SUPABASE_URL\" },
      { \"key\": \"VITE_SUPABASE_ANON_KEY\", \"value\": \"$VITE_SUPABASE_ANON_KEY\" }
    ],
    \"serviceDetails\": {
      \"env\": \"image\",
      \"runtime\": \"image\",
      \"region\": \"singapore\",
      \"plan\": \"free\",
      \"healthCheckPath\": \"/health\"
    }
  }")
echo "$RESP_F" > "${OUT}resp_frontend.json"

# --- report actual URLs -----------------------------------------------------
B_ID=$(echo "$RESP_B" | grep -o '"id":"[^"]*"' | head -1 | sed 's/"id":"//;s/"//')
F_ID=$(echo "$RESP_F" | grep -o '"id":"[^"]*"' | head -1 | sed 's/"id":"//;s/"//')
B_URL=$(echo "$RESP_B" | grep -o '"url":"[^"]*"' | head -1 | sed 's/"url":"//;s/"//')
F_URL=$(echo "$RESP_F" | grep -o '"url":"[^"]*"' | head -1 | sed 's/"url":"//;s/"//')

echo
echo "Backend  id=$B_ID url=${B_URL:-$BACKEND_URL}"
echo "Frontend id=$F_ID url=${F_URL:-$FRONTEND_URL}"

# If the frontend got a non-predicted URL, patch backend ALLOWED_ORIGINS to match.
if [ -n "$F_URL" ] && [ "$F_URL" != "$FRONTEND_URL" ]; then
  echo "Frontend URL differs from predicted; patching backend ALLOWED_ORIGINS ..."
  curl -sS -X PUT "$API/$B_ID/env-vars" \
    -H "Authorization: Bearer $RENDER_KEY" \
    -H "Accept: application/json" \
    -H "Content-Type: application/json" \
    -d "[{\"key\":\"ALLOWED_ORIGINS\",\"value\":\"$F_URL\"}]" \
    -o "${OUT}resp_backend_envpatch.json"
  echo "  -> wrote resp_backend_envpatch.json"
fi

echo "Done. resp_backend.json / resp_frontend.json written."
