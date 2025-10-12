# OdeaDev‑AI‑TTS

**Production-ready Python FastAPI service** that wraps the MiniMax T2A API with your own authentication, billing tiers, and user management.

## ✨ Features

- ✅ **User Management** - Create users with API keys and assign billing plans
- ✅ **Authentication** - Secure Bearer token authentication
- ✅ **Quota Management** - Enforce usage limits per plan (free, basic, pro, enterprise)
- ✅ **Voice Management** - Support for multiple voices (Nigerian, American, British, custom)
- ✅ **Usage Tracking** - Log all TTS requests with success/error status
- ✅ **MiniMax Integration** - Seamless proxy to MiniMax Speech API
- ✅ **Auto-generated API Docs** - Interactive Swagger/OpenAPI docs at `/docs`

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and add your MiniMax credentials:

```bash
cp .env.example .env
```

Edit `.env`:
```bash
MINIMAX_API_KEY=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
MINIMAX_GROUP_ID=1933510987994895143
DATABASE_URL=sqlite:///./odeadev_tts.db
SECRET_KEY=your-secret-key-here
```

### 3. Initialize Database

```bash
python -m src.init_db
```

This creates the database tables and seeds default voices.

### 4. Start the Server

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

Server runs on **http://localhost:8000**

---

## 📖 API Usage

### View API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 1. Create a User (Admin)

First, create an admin user manually by modifying the database, OR use enterprise credentials.

```bash
curl -X POST http://localhost:8000/admin/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ADMIN_API_KEY" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "plan": "basic"
  }'
```

**Response** (save the `api_key`!):
```json
{
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "plan": "basic",
    "quota_seconds": 3600,
    "used_seconds": 0,
    "remaining_seconds": 3600,
    "quota_percentage_used": 0,
    "is_active": true,
    "created_at": "2025-10-12T01:00:00"
  },
  "api_key": "nF8x3kR2mP9vL5tQ1wY7hJ6cB4aD0sZ8eU2oK5gM3iN6pW9rT1"
}
```

### 2. List Available Voices

```bash
curl -X GET http://localhost:8000/v1/voices \
  -H "Authorization: Bearer nF8x3kR2mP9vL5tQ1wY7hJ6cB4aD0sZ8eU2oK5gM3iN6pW9rT1"
```

**Response**:
```json
[
  {
    "id": 1,
    "friendly_name": "nigerian-male",
    "language": "en-NG",
    "gender": "male",
    "description": "Nigerian male voice with natural accent",
    "is_cloned": false,
    "is_active": true,
    "created_at": "2025-10-12T01:00:00"
  }
]
```

### 3. Generate Speech

```bash
curl -X POST http://localhost:8000/v1/tts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer nF8x3kR2mP9vL5tQ1wY7hJ6cB4aD0sZ8eU2oK5gM3iN6pW9rT1" \
  -d '{
    "text": "Hello, welcome to OdeaDev AI Text to Speech!",
    "voice_name": "nigerian-male",
    "model": "speech-02-turbo",
    "speed": 1.0,
    "pitch": 0,
    "emotion": "neutral"
  }' | jq -r '.audio_base64' | base64 -d > output.mp3
```

**Response**:
```json
{
  "audio_base64": "SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4Ljc2LjEwMAAA...",
  "duration_seconds": 4.8,
  "sample_rate": 32000,
  "voice_used": "nigerian-male",
  "text_length": 45,
  "remaining_quota": 3595.2
}
```

### 4. Check Your Quota

```bash
curl -X GET http://localhost:8000/v1/me \
  -H "Authorization: Bearer nF8x3kR2mP9vL5tQ1wY7hJ6cB4aD0sZ8eU2oK5gM3iN6pW9rT1"
```

---

## 🏗️ Project Structure

```
.
├── src/
│   ├── __init__.py
│   ├── main.py              # FastAPI app with all endpoints
│   ├── database.py          # SQLAlchemy database connection
│   ├── models.py            # User, Voice, Usage models
│   ├── schemas.py           # Pydantic request/response schemas
│   ├── auth.py              # API key generation/hashing
│   ├── dependencies.py      # Auth middleware
│   ├── minimax_client.py    # MiniMax API client
│   └── init_db.py           # Database initialization script
├── tests/
│   ├── test_auth.py         # Auth tests
│   └── test_structure.py    # Structure tests
├── .env.example             # Environment variables template
├── .gitignore               # Protected files
├── requirements.txt         # Python dependencies
├── planning.md              # Implementation phases
└── README.md                # This file
```

---

## 💰 Billing Plans

| Plan | Price/month | Quota | RPM | Max Streams |
|------|-------------|-------|-----|-------------|
| **Free** | $0 | 600s (10 min) | 10 | 1 |
| **Basic** | $19 | 3600s (60 min) | 30 | 2 |
| **Pro** | $70 | 14400s (240 min) | 60 | 5 |
| **Enterprise** | $180+ | Custom | Custom | Custom |

---

## 🔑 Admin Operations

### Create Voice

```bash
curl -X POST http://localhost:8000/admin/voices \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ADMIN_KEY" \
  -d '{
    "friendly_name": "custom-voice",
    "minimax_voice_id": "voice_id_from_minimax",
    "language": "en-US",
    "gender": "female",
    "description": "Custom cloned voice",
    "is_cloned": true
  }'
```

### Update User Quota

```bash
curl -X PUT http://localhost:8000/admin/users/1/quota \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ADMIN_KEY" \
  -d '{
    "used_seconds": 0
  }'
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/
```

---

## 🚀 Deployment Options

### Render (Recommended for Quick Start)
```bash
# Push to GitHub, then deploy on Render
# Full guide: RENDER_DEPLOYMENT.md
```

**Benefits:**
- ✅ Free tier available
- ✅ Auto-deploy on git push
- ✅ Managed SSL certificates
- ✅ Built-in health checks
- ✅ Persistent disk storage

**Quick deploy:** [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)

### Docker / RunPod
```bash
# Deploy anywhere Docker runs
docker-compose up -d
```

**Full guide:** [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 🔗 Integration Examples

### n8n Workflows
Pre-built integration examples for:
- 📱 WhatsApp voice messages
- 💬 Telegram bots
- 📧 Email to audio conversion
- 🔄 Batch processing
- 📊 Usage analytics

**Full guide:** [N8N_INTEGRATION.md](N8N_INTEGRATION.md)

---

## 📋 Project Status

- [x] **Phase 1**: Project setup ✅
- [x] **Phase 2**: Database models & auth ✅
- [x] **Phase 3**: TTS endpoint & MiniMax integration ✅
- [x] **Phase 4**: Voice management ✅
- [x] **Deployment**: Render + Docker ready ✅
- [x] **Integrations**: n8n examples ✅
- [ ] **Phase 5**: Rate limiting (RPM enforcement)
- [ ] **Phase 6**: Advanced logging
- [ ] **Phase 7**: Voice cloning API

---

## 🔒 Security Notes

1. **Never commit** `.env` file with real credentials
2. API keys are hashed in the database (SHA256)
3. Admin endpoints require enterprise-level credentials
4. MiniMax credentials stored in environment variables only

---

## 📚 Resources

- [MiniMax Platform](https://platform.minimaxi.com/)
- [MiniMax API Documentation](https://platform.minimaxi.com/document)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

**Status**: ✅ **Core functionality complete** | Phases 1-3 implemented

Add MiniMax credits and you're ready to generate speech! 🎉
