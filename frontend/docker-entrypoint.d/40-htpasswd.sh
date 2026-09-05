#!/bin/sh
# Write the basic-auth credentials supplied by the environment. Runs before
# nginx starts (nginx:alpine executes /docker-entrypoint.d/*.sh at boot).
set -e
printf '%s\n' "${BASIC_AUTH_HTPASSWD:-}" > /etc/nginx/.htpasswd
chmod 0644 /etc/nginx/.htpasswd
