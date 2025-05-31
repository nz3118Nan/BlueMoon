# build docker image
docker build -t blueprint-ai-agent-service .

# run docker container
docker stop blueprint-agent || true && \
docker rm blueprint-agent || true

# Check if .env file exists
if [ -f .env ]; then
    echo "Found .env file, loading environment variables..."
    # Use --env-file option which is safer and more reliable
    docker run -d \
        -p 8000:3000 \
        --name blueprint-agent \
        --add-host=host.docker.internal:host-gateway \
        --env-file localdocker.env \
        blueprint-ai-agent-service
        
else
    echo "No .env file found, running without environment variables"
    docker run -d \
        -p 8000:3000 \
        --name blueprint-agent \
        --add-host=host.docker.internal:host-gateway \
        blueprint-ai-agent-service
fi