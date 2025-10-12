#!/bin/bash
# Quick start script for OdeaDev-AI-TTS

set -e

echo "🚀 Starting OdeaDev-AI-TTS..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating from .env.example..."
    cp .env.example .env
    echo "✅ Created .env file. Please edit it with your MiniMax credentials."
    echo ""
    echo "Required variables:"
    echo "  - MINIMAX_API_KEY"
    echo "  - MINIMAX_GROUP_ID"
    echo ""
    read -p "Press Enter after editing .env to continue..."
fi

# Check if database exists
if [ ! -f odeadev_tts.db ]; then
    echo "📦 Database not found. Initializing..."
    python -m src.init_db
    echo ""
fi

# Start server
echo "🎙️  Starting FastAPI server..."
echo "📚 API docs will be available at: http://localhost:8000/docs"
echo ""

uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
