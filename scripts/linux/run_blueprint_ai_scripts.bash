#!/bin/bash
# Install Git
echo "Installing Git..."
sudo yum install git -y

# Install Python and dependencies
echo "Installing Python and dependencies..."
sudo yum install -y python3 python3-pip python3-devel gcc make libffi-devel openssl-devel

# Install additional Python packages via pip
echo "Installing additional Python packages..."
# Use --ignore-installed to avoid conflicts with system packages
sudo pip3 install --ignore-installed --upgrade pip
# Install specific version of cryptography that's compatible with awscli
sudo pip3 install --ignore-installed "cryptography<40.0.2,>=3.3.2"

# Check if SSH key exists
if [ ! -f ~/.ssh/id_rsa ]; then
    echo "Creating new SSH key..."
    ssh-keygen -t rsa -b 4096 -C "joe.zhounan@gmail.com" -f ~/.ssh/id_rsa -N "" -y
    # Set proper permissions for SSH directory and key
    chmod 700 ~/.ssh
    chmod 600 ~/.ssh/id_rsa
    chmod 644 ~/.ssh/id_rsa.pub

    # global git config
    git config --global user.name "nz3118Nan"
    git config --global user.email "joe.zhounan@gmail.com"

    # Add the key to the SSH agent
    eval "$(ssh-agent -s)"
    ssh-add ~/.ssh/id_rsa

    # show ssh key
    echo "Git installation and SSH key setup completed!"
    echo "Your public SSH key is:"
    cat ~/.ssh/id_rsa.pub
else
    echo "SSH key already exists, skipping creation..."
fi

## copy rsa key file to github
## cat ~/.ssh/id_rsa.pub
## make sure the rsa key file is added to github

## test ssh connection
echo "Testing SSH connection to GitHub..."
ssh -o StrictHostKeyChecking=no -T git@github.com

## docker
sudo yum install docker -y
sudo systemctl start docker
sudo systemctl enable docker

## install docker compose
if ! command -v docker-compose &> /dev/null; then
    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
else
    echo "Docker compose is already installed"
fi

## install tmux 
sudo yum install tmux -y

## install ngrok
### check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "Ngrok could not be found, installing..."
    # Download ngrok
    curl -o ngrok.zip https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.zip
    # Unzip ngrok
    unzip ngrok.zip
    # Move ngrok to /usr/local/bin
    sudo mv ngrok /usr/local/bin/
    # Clean up
    rm ngrok.zip
    # Set permissions
    sudo chmod +x /usr/local/bin/ngrok

    ## configure ngrok
else
    echo "Ngrok is already installed"
fi

ngrok config add-authtoken 2T1fhAA7yjWJ2lPelhg1qoUsBsT_9PrBMCebzX4ubkeEJjPM

## handle ngrok tmux session
echo "Setting up ngrok tunnel..."

# Kill window
sudo tmux kill-server
sudo tmux start-server
tmux kill-server
tmux start-server

# Create new session and start ngrok without entering the session
tmux new-session -d -s ngrok_connection "ngrok tunnel --label edge=edghts_2Z8KxM7YTaKqJ6g6fbK45UwQS21 http://localhost:80"

# git clone https://github.com/langgenius/dify.git to /home/opt/project
if [ ! -d "/opt/project/dify" ]; then
    # if no project folder, mkdir it
    mkdir -p /opt/project/dify
    git clone https://github.com/langgenius/dify.git /opt/project/dify
else
    echo "Dify project already exists"
    # pull the latest code
    cd /opt/project/dify
    git pull
    cd /opt/project
fi

# install dify
cd /opt/project/dify
cd docker

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from example..."
    cp .env.example .env
else
    echo ".env file already exists"
fi

# Check if docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Docker is not running. Starting Docker..."
    sudo systemctl start docker
    sleep 5
fi

# Start dify services
echo "Starting Dify services..."
docker-compose up -d

# Wait for services to start
echo "Waiting for services to start..."
sleep 10

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    echo "Dify services are running successfully!"
    
    # Get the public URL from ngrok
    echo "Getting ngrok public URL..."
    NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"[^"]*"' | cut -d'"' -f4)

    echo "================================================"
    echo "Dify installation is complete!"
    echo "You can access the installation page at:"
    echo "1. Local URL: http://localhost/install"
    echo "2. Public URL: $NGROK_URL/install"
    echo ""
    echo "To view the ngrok tunnel status:"
    echo "tmux attach -t ngrok_connection"
    echo "To detach from the tmux session, press Ctrl+B then D"
    echo ""
    echo "If you need to restart the ngrok tunnel:"
    echo "1. tmux attach -t ngrok_connection"
    echo "2. Press Ctrl+C to stop the current tunnel"
    echo "3. Run: ngrok tunnel --label edge=edghts_2Z8KxM7YTaKqJ6g6fbK45UwQS21 http://localhost:3000"
    echo "4. Press Ctrl+B then D to detach"
    echo "================================================"
else
    echo "Error: Dify services failed to start. Please check the logs:"
    docker-compose logs
    exit 1
fi
