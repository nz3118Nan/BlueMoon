# run docker container
docker stop litellm-proxy || true && \
docker rm litellm-proxy || true

# Check if .env file exists
if [ -f .env ]; then
    echo "Found .env file, loading environment variables..."
    # Use --env-file option which is safer and more reliable
    docker run -d \
        -p 4000:4000 \
        -v $(pwd)/configs/litellm_proxy/config.yaml:/app/config.yaml \
        --name litellm-proxy \
        --add-host=host.docker.internal:host-gateway \
        --env-file localdocker.env \
        ghcr.io/berriai/litellm:main-latest \
        --config /app/config.yaml --detailed_debug
        
else
    echo "No .env file found, running without environment variables"
    docker run -d \
        -p 4000:4000 \
        -v $(pwd)/configs/litellm_proxy/config.yaml:/app/config.yaml \
        --name litellm-proxy \
        --add-host=host.docker.internal:host-gateway \
        ghcr.io/berriai/litellm:main-latest \
        --config /app/config.yaml --detailed_debug
fi