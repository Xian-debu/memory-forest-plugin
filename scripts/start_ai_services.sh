#!/bin/bash
# Start AI services in background

SCRIPT_DIR="/root/.claude/scripts"
LOG_DIR="/tmp/ai-services"
mkdir -p "$LOG_DIR"

# Source API keys
source ~/.bashrc

echo "=== Starting AI Services ==="

# Start n8n container if not running
if ! docker ps --filter name=n8n --format '{{.Names}}' | grep -q n8n; then
    echo "Starting n8n container..."
    docker start n8n 2>/dev/null || docker run -d \
        --name n8n \
        -p 5678:5678 \
        -v n8n_data:/home/node/.n8n \
        -e N8N_SECURE_COOKIE=false \
        -e N8N_HOST=localhost \
        -e WEBHOOK_URL=http://localhost:5678 \
        -e ANTHROPIC_BASE_URL="$ANTHROPIC_BASE_URL" \
        -e ANTHROPIC_AUTH_TOKEN="$ANTHROPIC_AUTH_TOKEN" \
        n8nio/n8n:latest
else
    echo "n8n container already running"
fi

# Start AI Webhook Server in background
if pgrep -f "ai_webhook_server.py" > /dev/null; then
    echo "AI Webhook Server already running"
else
    echo "Starting AI Webhook Server on port 8899..."
    nohup python3 "$SCRIPT_DIR/ai_webhook_server.py" > "$LOG_DIR/webhook.log" 2>&1 &
    echo "  PID: $!, Log: $LOG_DIR/webhook.log"
fi

echo ""
echo "=== Services ==="
echo "  n8n UI:    http://localhost:5678"
echo "  AI Webhook: http://localhost:8899"
echo "  API Keys:  $([ -n "$ANTHROPIC_AUTH_TOKEN" ] && echo "LOADED" || echo "MISSING")"
