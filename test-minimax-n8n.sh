#!/bin/bash

# Minimax TTS n8n Workflow Test Script
# This script tests your n8n webhook endpoint

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🎙️  Minimax TTS n8n Workflow Tester"
echo "===================================="
echo ""

# Configuration
N8N_WEBHOOK_URL="${N8N_WEBHOOK_URL:-http://localhost:5678/webhook/minimax-tts}"

echo "Webhook URL: $N8N_WEBHOOK_URL"
echo ""

# Test 1: Basic Text-to-Speech
echo "${YELLOW}Test 1: Basic Text-to-Speech${NC}"
echo "--------------------------------"

RESPONSE=$(curl -s -X POST "$N8N_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, this is a test of Minimax TTS integration with n8n!"
  }')

if echo "$RESPONSE" | grep -q '"success":true'; then
    echo -e "${GREEN}✓ Test 1 PASSED${NC}"
    echo "Duration: $(echo "$RESPONSE" | grep -o '"duration_ms":[0-9]*' | cut -d':' -f2) ms"

    # Save audio to file
    AUDIO_BASE64=$(echo "$RESPONSE" | grep -o '"audio_base64":"[^"]*' | cut -d'"' -f4)
    if [ ! -z "$AUDIO_BASE64" ]; then
        echo "$AUDIO_BASE64" | base64 -d > test1_output.mp3 2>/dev/null
        echo "Audio saved to: test1_output.mp3"
    fi
else
    echo -e "${RED}✗ Test 1 FAILED${NC}"
    echo "Response: $RESPONSE"
fi

echo ""
echo ""

# Test 2: Custom Voice Settings
echo "${YELLOW}Test 2: Custom Voice Settings${NC}"
echo "--------------------------------"

RESPONSE=$(curl -s -X POST "$N8N_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "This test uses custom voice settings with faster speed and happy emotion.",
    "voiceId": "moss_audio_141d8c4c-a6f8-11f0-84c1-0ec6fa858d82",
    "speed": 1.3,
    "emotion": "happy",
    "model": "speech-02-hd"
  }')

if echo "$RESPONSE" | grep -q '"success":true'; then
    echo -e "${GREEN}✓ Test 2 PASSED${NC}"
    echo "Voice ID: $(echo "$RESPONSE" | grep -o '"voice_id":"[^"]*' | cut -d'"' -f4)"

    # Save audio to file
    AUDIO_BASE64=$(echo "$RESPONSE" | grep -o '"audio_base64":"[^"]*' | cut -d'"' -f4)
    if [ ! -z "$AUDIO_BASE64" ]; then
        echo "$AUDIO_BASE64" | base64 -d > test2_output.mp3 2>/dev/null
        echo "Audio saved to: test2_output.mp3"
    fi
else
    echo -e "${RED}✗ Test 2 FAILED${NC}"
    echo "Response: $RESPONSE"
fi

echo ""
echo ""

# Test 3: Long Text
echo "${YELLOW}Test 3: Long Text Processing${NC}"
echo "--------------------------------"

RESPONSE=$(curl -s -X POST "$N8N_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "This is a longer text to test the capabilities of the Minimax text-to-speech engine. It should handle multiple sentences with proper intonation and pacing. The quality should remain consistent throughout the entire audio output.",
    "speed": 1.0,
    "emotion": "neutral"
  }')

if echo "$RESPONSE" | grep -q '"success":true'; then
    echo -e "${GREEN}✓ Test 3 PASSED${NC}"
    echo "Duration: $(echo "$RESPONSE" | grep -o '"duration_ms":[0-9]*' | cut -d':' -f2) ms"

    # Save audio to file
    AUDIO_BASE64=$(echo "$RESPONSE" | grep -o '"audio_base64":"[^"]*' | cut -d'"' -f4)
    if [ ! -z "$AUDIO_BASE64" ]; then
        echo "$AUDIO_BASE64" | base64 -d > test3_output.mp3 2>/dev/null
        echo "Audio saved to: test3_output.mp3"
    fi
else
    echo -e "${RED}✗ Test 3 FAILED${NC}"
    echo "Response: $RESPONSE"
fi

echo ""
echo ""

# Summary
echo "===================================="
echo "Test Summary"
echo "===================================="
echo ""
echo "Generated audio files:"
echo "  - test1_output.mp3 (basic test)"
echo "  - test2_output.mp3 (custom settings)"
echo "  - test3_output.mp3 (long text)"
echo ""
echo "To play audio files:"
echo "  macOS:  afplay test1_output.mp3"
echo "  Linux:  mpg123 test1_output.mp3"
echo "  Windows: start test1_output.mp3"
echo ""
echo "🎉 Testing complete!"
