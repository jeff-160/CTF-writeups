#!/bin/bash
set -e

IMAGE="xss-insane"
TAG="${1:-latest}"

echo "[*] Building Docker image: $IMAGE:$TAG"
docker build -t "$IMAGE:$TAG" .

echo ""
echo "[*] Build complete: $IMAGE:$TAG"
echo ""
echo "Run options:"
echo "  docker compose up -d                     # using docker-compose.yml"
echo "  FLAG=flag{...} docker compose up -d      # with custom flag"
echo "  docker run -p 3000:3000 -e FLAG=flag{...} $IMAGE:$TAG   # standalone"
