# 🚀 OdeaDev-AI-TTS - START HERE

**Welcome!** Your production-ready Text-to-Speech API service is complete.

---

## 🎯 What You Have

A **full-featured TTS service** that:
- ✅ Wraps MiniMax API with your own authentication
- ✅ Manages users with API keys and billing plans
- ✅ Enforces quotas (Free, Basic, Pro, Enterprise)
- ✅ Tracks usage and analytics
- ✅ Supports multiple voices (Nigerian, American, British)
- ✅ Ready to deploy to Render.com, RunPod, or Docker
- ✅ Includes n8n integration examples

**Your MiniMax Credentials:**
```
API Key: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
Group ID: 1933510987994895143
Default Voice: moss_audio_141d8c4c-a6f8-11f0-84c1-0ec6fa858d82
```

---

## 🚀 Quick Start Guide (Choose Your Path)

### Option 1: Deploy to Render (Fastest - 20 minutes)
**Best for:** Quick production launch, testing, MVP

```bash
1. Follow: RENDER_CHECKLIST.md
2. Push to GitHub
3. Deploy on Render.com
4. Set environment variables
5. Test API
```

**Result:** Live API at `https://your-service.onrender.com`

👉 **[Start Here: RENDER_CHECKLIST.md](RENDER_CHECKLIST.md)**

---

### Option 2: Run Locally (5 minutes)
**Best for:** Development, testing, customization

```bash
1. Follow: QUICKSTART.md
2. pip install -r requirements.txt
3. Configure .env file
4. python -m src.init_db
5. uvicorn src.main:app --reload
```

**Result:** API running at `http://localhost:8000`

👉 **[Start Here: QUICKSTART.md](QUICKSTART.md)**

---

### Option 3: Docker Deployment (Advanced)
**Best for:** Custom infrastructure, RunPod, AWS

```bash
1. Follow: DEPLOYMENT.md
2. docker-compose up -d
3. Configure environment
4. Monitor logs
```

**Result:** Containerized service ready for production

👉 **[Start Here: DEPLOYMENT.md](DEPLOYMENT.md)**

---

## 📚 Full Documentation Index

### Getting Started
- 📖 **[README.md](README.md)** - Complete project overview
- ⚡ **[QUICKSTART.md](QUICKSTART.md)** - Local setup in 5 minutes
- ✅ **[RENDER_CHECKLIST.md](RENDER_CHECKLIST.md)** - Deploy to Render step-by-step

### Deployment Guides
- 🚀 **[RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)** - Render.com complete guide
- 🐳 **[DEPLOYMENT.md](DEPLOYMENT.md)** - Docker, RunPod, cloud providers
- 📋 **[docker-compose.yml](docker-compose.yml)** - Docker orchestration
- 🏗️ **[Dockerfile](Dockerfile)** - Container definition
- ⚙️ **[render.yaml](render.yaml)** - Render infrastructure-as-code

### Integration & Automation
- 🔗 **[N8N_INTEGRATION.md](N8N_INTEGRATION.md)** - n8n workflow examples
  - WhatsApp voice bot
  - Telegram commands
  - Email to audio
  - Batch processing
  - Usage analytics

### Technical Documentation
- 🏛️ **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Architecture & design
- 📋 **[planning.md](planning.md)** - Implementation roadmap & phases

### Configuration
- 🔧 **[.env.example](.env.example)** - Environment variables template
- 📦 **[requirements.txt](requirements.txt)** - Python dependencies

---

## 🎯 Common Use Cases

### 1. Deploy API for Customers
```
Goal: Sell TTS as a service
Path: RENDER_CHECKLIST.md → Create customer API keys
Time: 20 minutes
```

### 2. WhatsApp Voice Bot
```
Goal: Auto-reply to WhatsApp messages with voice
Path: RENDER_DEPLOYMENT.md → N8N_INTEGRATION.md (WhatsApp section)
Time: 30 minutes
```

### 3. Telegram Voice Commands
```
Goal: /speak command generates audio
Path: N8N_INTEGRATION.md (Telegram section)
Time: 15 minutes
```

### 4. Custom Voice Integration
```
Goal: Add your own cloned voices
Path: README.md (Admin endpoints) → POST /admin/voices
Time: 5 minutes
```

### 5. Local Development
```
Goal: Customize and test changes
Path: QUICKSTART.md → modify src/main.py
Time: 5 minutes setup
```

---

## ⚡ Quick Commands Reference

### Local Development
```bash
# Install
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your credentials

# Initialize
python -m src.init_db
python -m src.create_admin "Name" "email@example.com"

# Run
uvicorn src.main:app --reload

# Test
curl http://localhost:8000/health
```

### Docker
```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Testing API
```bash
# Set your API key
export API_KEY="your-api-key-here"
export API_URL="https://your-service.onrender.com"

# Test health
curl $API_URL/health

# Generate speech
curl -X POST $API_URL/v1/tts \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello world","voice_name":"nigerian-male"}' \
  | jq -r '.audio_base64' | base64 -d > audio.mp3
```

---

## 🔑 Important Files

### Must Configure Before Deploy
```
.env                    # Your MiniMax credentials (create from .env.example)
```

### Auto-Configured on Deploy
```
odeadev_tts.db         # SQLite database (auto-created)
/data/                 # Persistent storage (Render disk mount)
```

### Don't Commit to Git
```
.env                   # Contains secrets
*.db                   # Database files
__pycache__/          # Python cache
node_modules/         # Legacy Node.js files
```

---

## ❗ Before You Deploy

### Required
1. ✅ MiniMax account with credits: https://platform.minimaxi.com/
2. ✅ GitHub account (for Render deployment)
3. ✅ Render.com account (free tier available)

### Recommended
1. 📝 Read `RENDER_CHECKLIST.md` completely
2. 🔐 Use a password manager for API keys
3. 📊 Set up monitoring alerts
4. 💾 Plan backup strategy

### Optional
1. 🌐 Custom domain for your API
2. 🔗 n8n account for automation
3. 📱 WhatsApp/Telegram accounts for bots

---

## 🆘 Need Help?

### Quick Troubleshooting

**"Insufficient balance"**
→ Add credits: https://platform.minimaxi.com/recharge

**"Invalid API key"**
→ Check Authorization header: `Bearer YOUR_KEY`

**"Service won't start"**
→ Check environment variables in Render dashboard

**"Database errors"**
→ Ensure persistent disk is attached in Render

### Documentation
- 📖 [README.md](README.md) - Main documentation
- ❓ [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) - Deployment help
- 🐛 Troubleshooting sections in each guide

### Resources
- Render Docs: https://render.com/docs
- MiniMax Platform: https://platform.minimaxi.com/
- FastAPI Docs: https://fastapi.tiangolo.com/

---

## 🎉 What's Next?

### Immediate Next Steps (Pick One)

**For Production Launch:**
1. Open `RENDER_CHECKLIST.md`
2. Follow each step
3. Deploy in 20 minutes
4. Start serving customers

**For Local Testing:**
1. Open `QUICKSTART.md`
2. Run locally in 5 minutes
3. Test all features
4. Customize as needed

**For Integration:**
1. Deploy first (Render or local)
2. Open `N8N_INTEGRATION.md`
3. Build your first workflow
4. Connect WhatsApp/Telegram

### Future Enhancements (Optional)

- [ ] Add rate limiting (Phase 5)
- [ ] Implement voice cloning
- [ ] Switch to PostgreSQL
- [ ] Add usage dashboard
- [ ] Integrate payment processing
- [ ] Add webhook notifications

---

## 📊 Project Status

✅ **PRODUCTION READY**

- ✅ Core API complete (Phases 1-4)
- ✅ Authentication & authorization
- ✅ Quota management
- ✅ Usage tracking
- ✅ Multiple deployment options
- ✅ Integration examples
- ✅ Comprehensive documentation

**Ready to deploy and start generating revenue!**

---

## 🚀 Choose Your Path Now

**Quick deploy?** → [RENDER_CHECKLIST.md](RENDER_CHECKLIST.md)  
**Local testing?** → [QUICKSTART.md](QUICKSTART.md)  
**Need overview?** → [README.md](README.md)

---

**Your Text-to-Speech API service is ready. Let's deploy it! 🎙️**
