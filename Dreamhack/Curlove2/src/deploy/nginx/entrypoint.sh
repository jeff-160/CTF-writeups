#!/bin/bash
RANDOM_DIR=$(openssl rand -hex 1)
mkdir -p /etc/nginx/${RANDOM_DIR}
echo "CURL_TOKEN=[REDACTED]" > /etc/nginx/${RANDOM_DIR}/curl-token
exec "$@"