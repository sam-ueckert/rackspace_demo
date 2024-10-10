#!/usr/bin/env bash

set -euo pipefail

readonly NGINX_CONFIG=/app/.nginx/nginx.conf
readonly NGINX_P="/tmp/nginx.pid"

echo "$@"
nginx -c "$NGINX_CONFIG" -p "$NGINX_P" -g "daemon off;" & $@
