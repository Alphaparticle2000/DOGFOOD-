# ==============================================================================
# DOGFOOD Frontend — React + Vite, served by nginx
#
# Stage 1 (build):  node:22-alpine  -> npm ci && npm run build  -> /app/dist
# Stage 2 (runtime): nginx:alpine   -> static files only, no node toolchain
#
# Vite variables are baked in at BUILD time (import.meta.env), so they are
# accepted as --build-arg. The runtime entrypoint additionally emits env.js so
# that VITE_* variables set on the platform (e.g. Render) still take effect
# without a rebuild — see docker-entrypoint.sh.
# ==============================================================================

# ---------------------------------------------------------------- build stage
FROM node:22-alpine AS build

WORKDIR /app

# Declared as ARG then re-exported as ENV so `vite build` sees them in process.env.
ARG VITE_SUPABASE_URL=""
ARG VITE_SUPABASE_ANON_KEY=""
ARG VITE_API_URL=""

ENV VITE_SUPABASE_URL=$VITE_SUPABASE_URL \
    VITE_SUPABASE_ANON_KEY=$VITE_SUPABASE_ANON_KEY \
    VITE_API_URL=$VITE_API_URL

# Install dependencies first so Docker can cache this layer across source edits.
COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

# -------------------------------------------------------------- runtime stage
FROM nginx:1.27-alpine AS runtime

# gettext provides envsubst, used to inject the platform-assigned $PORT.
RUN apk add --no-cache gettext \
    && mkdir -p /var/cache/nginx /var/log/nginx

COPY nginx.conf.template /etc/nginx/nginx.conf.template
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

COPY --from=build /app/dist /usr/share/nginx/html

# Render (and most PaaS) inject PORT at runtime; 8080 is the local default.
ENV PORT=8080
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD wget -q --spider http://127.0.0.1:${PORT}/health || exit 1

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
