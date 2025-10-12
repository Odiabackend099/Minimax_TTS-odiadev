# 🚀 OdeaDev-AI-TTS Quick Start Guide

Get up and running in **5 minutes**.

---

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 2: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit with your credentials
nano .env  # or use your preferred editor
```

**Required values in `.env`:**
```bash
MINIMAX_API_KEY=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...your-jwt-token
MINIMAX_GROUP_ID=1933510987994895143
```

---

## Step 3: Initialize Database

```bash
python -m src.init_db
```

**Output:**
```
Creating database tables...
✅ Database tables created successfully!
Seeding default voices...
  ✅ Added voice: nigerian-male
  ✅ Added voice: american-male
  ✅ Added voice: british-female
✅ Default voices seeded successfully!

🎉 Database initialization complete!
```

---

## Step 4: Create Admin User

```bash
python -m src.create_admin "Your Name" "your@email.com"
```

**Output:**
```
✅ Admin user created successfully!

======================================================================
📝 User Details:
   ID:    1
   Name:  Your Name
   Email: your@email.com
   Plan:  ENTERPRISE
   Quota: 36000s (600 minutes)

🔑 API Key (SAVE THIS - shown only once!):
   nF8x3kR2mP9vL5tQ1wY7hJ6cB4aD0sZ8eU2oK5gM3iN6pW9rT1
======================================================================
```

**⚠️ IMPORTANT:** Save this API key securely! You'll need it for all API requests.

---

## Step 5: Start the Server

```bash
# Option A: Using the start script
./start.sh

# Option B: Direct uvicorn command
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

**Server starts at:** http://localhost:8000

---

## Step 6: Test the API

### View Interactive Docs

Open in browser: **http://localhost:8000/docs**

### Test with cURL

```bash
# Set your API key (replace with yours from Step 4)
export API_KEY="nF8x3kR2mP9vL5tQ1wY7hJ6cB4aD0sZ8eU2oK5gM3iN6pW9rT1"

# Check your account info
curl -X GET http://localhost:8000/v1/me \
  -H "Authorization: Bearer $API_KEY"

# List available voices
curl -X GET http://localhost:8000/v1/voices \
  -H "Authorization: Bearer $API_KEY"

# Generate speech
curl -X POST http://localhost:8000/v1/tts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "text": "Hello! This is OdeaDev AI Text to Speech. Welcome!",
    "voice_name": "nigerian-male",
    "speed": 1.0,
    "emotion": "happy"
  }' | jq -r '.audio_base64' | base64 -d > welcome.mp3

# Play the audio (macOS)
afplay welcome.mp3
```

---

## 🎉 You're Ready!

### What's Next?

1. **Create regular users** via `/admin/users` endpoint
2. **Add custom voices** via `/admin/voices` endpoint
3. **Monitor usage** via `/v1/me` endpoint
4. **Build your app** using the `/v1/tts` endpoint

### Example: Create a Regular User

```bash
curl -X POST http://localhost:8000/admin/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "name": "Client User",
    "email": "client@example.com",
    "plan": "basic"
  }'
```

**Response includes a new API key** for the client to use.

---

## 📚 Documentation

- **Full README:** [README.md](README.md)
- **Planning Document:** [planning.md](planning.md)
- **API Docs:** http://localhost:8000/docs (when server running)

---

## ⚠️ Troubleshooting

### "MINIMAX_API_KEY not provided"
→ Make sure `.env` file exists and has your MiniMax credentials

### "insufficient balance"
→ Add credits to your MiniMax account at https://platform.minimaxi.com/

### "No voices configured"
→ Run `python -m src.init_db` to seed default voices

### Port 8000 already in use
→ Change port: `uvicorn src.main:app --port 8080`

---

## 🔗 Quick Links

- MiniMax Platform: https://platform.minimaxi.com/
- Get API Key: https://platform.minimaxi.com/user-center/basic-information/interface-key
- Add Credits: https://platform.minimaxi.com/recharge

---

**Need help?** Check the full [README.md](README.md) for detailed documentation.
