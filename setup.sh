#!/bin/bash
# AGENT SECOND BRAIN - VPS SETUP
set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Log function
log() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    error "This script should not be run as root. Please run as a regular user."
    exit 1
fi

# Detect system
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$NAME
    VER=$VERSION_ID
else
    error "Unable to detect Linux distribution"
    exit 1
fi

log "Starting setup for $OS $VER"

# Install required software
log "Installing required software..."

# Install Python 3.11+ and dependencies
log "Installing Python 3.11..."
sudo apt update
sudo apt install -y software-properties-common apt-transport-https ca-certificates curl gnupg lsb-release
curl -fsSL https://packages.sury.org/apt.gpg | sudo gpg --dearmor -o /usr/share/keyrings/sury-apt-keyring.gpg
echo "deb https://packages.sury.org/apt $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/sury-php.list
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3.11-dev python3.11-distutils

# Install Node.js
if ! command -v node &> /dev/null; then
    log "Installing Node.js..."
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt install -y nodejs
fi

# Install uv
if ! command -v uv &> /dev/null; then
    log "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

# Check installed versions
python3.11 --version
node --version
uv --version

# Set up software sources
log "Setting up software sources..."

# Check environment variables
log "Checking environment variables..."

# Install Git
if ! command -v git &> /dev/null; then
    log "Installing Git..."
    sudo apt install -y git
fi

# Create required directories
log "Setting up directory structure..."
mkdir -p vault/goals vault/daily vault/business/crm vault/business/network vault/projects vault/thoughts/ideas vault/thoughts/learnings vault/thoughts/reflections vault/MOC vault/sessions

# Disable interactive mode
export SUDO_PWD=/tmp

# Get secrets from the user
log "Requesting credentials..."

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    cat > .env << EOF
# Telegram Bot Token (get from @BotFather)
TELEGRAM_BOT_TOKEN=

# Deepgram API Key (get from https://console.deepgram.com/)
DEEPGRAM_API_KEY=

# Todoist API Token (get from Settings > Integrations > Developer)
TODOIST_API_KEY=

# Path to your Obsidian vault
VAULT_PATH=/home/khabarovru/vault

# Allowed Telegram user IDs (JSON array format: [123456789])
ALLOWED_USER_IDS=[123456789]
EOF
    warn "Created .env file. Please update with your API tokens."
else
    warn ".env file already exists. Skipping creation."
fi

# Set up virtual environment
log "Setting up Python virtual environment..."
if [ ! -d ".venv" ]; then
    python3.11 -m venv .venv
else
    warn "Virtual environment .venv already exists."
fi

# Install Python dependencies
log "Installing Python dependencies..."
source .venv/bin/activate
pip install --upgrade pip
pip install --no-cache-dir python-telegram-bot deepgram-sdk todoist

# Install Node.js dependencies if exist
log "Installing Node.js dependencies..."
if [ -f package.json ]; then
    npm install
fi

# Ensure script files are executable
chmod +x scripts/*.sh scripts/*.py

# Create cron jobs
log "Setting up cron jobs..."
# Daily processing job
(crontab -l 2>/dev/null; echo "0 21 * * * $(pwd)/scripts/process.sh") | crontab -
# Weekly digest job
(crontab -l 2>/dev/null; echo "0 20 * * 0 $(pwd)/scripts/weekly.py") | crontab -

# Create systemd service
log "Creating systemd service..."
cat > second-brain.service << EOF
[Unit]
Description=Second Brain Agent
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
ExecStart=$(pwd)/.venv/bin/python bot.py
Restart=always
RestartSec=10
Environment=PATH=$(pwd)/.venv/bin:$PATH
Environment=TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN
Environment=DEEPGRAM_API_KEY=$DEEPGRAM_API_KEY
Environment=TODOIST_API_KEY=$TODOIST_API_KEY
Environment=VAULT_PATH=$VAULT_PATH
Environment=ALLOWED_USER_IDS=$ALLOWED_USER_IDS

[Install]
WantedBy=multi-user.target
EOF

# Ensure systemd reads the new service
sudo mv second-brain.service /etc/systemd/system/second-brain.service
sudo systemctl daemon-reload

log "Setup completed successfully!"
log "Next steps:"
log "1. Update .env file with your actual API tokens"
log "2. Start the service: sudo systemctl start second-brain"
log "3. Check status: sudo systemctl status second-brain"
log "4. View logs: sudo journalctl -u second-brain -f"