docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t lukbit/trans-api \
  -f api.Dockerfile \
  --push .
