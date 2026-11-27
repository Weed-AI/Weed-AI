# Pinned to the 1.30 stable line (>= 1.30.7 fixes the Nov 2026 "nginx2root"
# CVEs). Rebuild with `docker compose build --pull reverse-proxy` to pick up
# patch releases; check with `docker exec reverse_proxy nginx -v`.
FROM nginx:1.30
COPY ./nginx.conf /etc/nginx/nginx.conf
