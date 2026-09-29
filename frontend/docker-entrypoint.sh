#!/bin/sh
# Entrypoint for the DOGFOOD frontend container.
#
# 1. Renders nginx.conf from the template using the platform-assigned $PORT.
# 2. Emits /usr/share/nginx/html/env.js from any VITE_* variables present in the
#    container environment, then injects the <script> tag into index.html.
#    This exists because Vite inlines import.meta.env at build time, so values
#    that only exist at deploy time (e.g. the backend's Render URL) would
#    otherwise be impossible to change without a rebuild.
# 3. execs nginx in the foreground.

set -eu

PORT="${PORT:-8080}"
export PORT

envsubst '${PORT}' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

ENV_JS=/usr/share/nginx/html/env.js
INDEX=/usr/share/nginx/html/index.html

{
    printf 'window.__DOGFOOD_ENV__ = {\n'
    for pair in $(env | grep -E '^VITE_[A-Za-z0-9_]*=' || true); do
        key="${pair%%=*}"
        value="${pair#*=}"
        # Escape double quotes and backslashes so the generated JS stays valid.
        value=$(printf '%s' "$value" | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g')
        printf '  "%s": "%s",\n' "$key" "$value"
    done
    printf '};\n'
} > "$ENV_JS"

if [ -f "$INDEX" ] && ! grep -q 'env\.js' "$INDEX"; then
    sed -i 's|</head>|<script src="/env.js"></script></head>|' "$INDEX"
fi

exec nginx -g 'daemon off;'
