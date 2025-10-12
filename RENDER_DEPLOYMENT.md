# 🚀 Render Deployment Guide for OdeaDev-AI-TTS

Complete step-by-step guide for deploying to Render.com

---

## 📋 Prerequisites

1. **GitHub account** - Your code must be in a GitHub repository
2. **Render account** - Sign up at https://render.com (free tier available)
3. **MiniMax credentials** - Get from https://platform.minimaxi.com/
   - API Key (JWT token)
   - Group ID

---

## 🚀 Quick Deploy (5 steps)

### Step 1: Push to GitHub

```bash
cd "/Users/odiadev/Desktop/minimax tts"

# Initialize git if not already done
git init
git add .
git commit -m "Initial commit: OdeaDev-AI-TTS service"

# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/odeadev-ai-tts.git
git branch -M main
git push -u origin main
```

### Step 2: Create Web Service on Render

1. Go to https://dashboard.render.com/
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Select the `odeadev-ai-tts` repository

### Step 3: Configure Service Settings

**Basic Settings:**
- **Name**: `odeadev-ai-tts` (or your preferred name)
- **Region**: Oregon (US West) or closest to you
- **Branch**: `main`
- **Runtime**: **Docker**
- **Instance Type**: 
  - **Free** (for testing - sleeps after 15 min inactivity)
  - **Starter** ($7/month - recommended for production)

**Advanced Settings:**
- **Health Check Path**: `/health`
- **Auto-Deploy**: Yes (deploys on every git push)

### Step 4: Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**

**Required:**
```bash
MINIMAX_API_KEY = eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...your-jwt-token
MINIMAX_GROUP_ID = 1933510987994895143
```

**Optional (with defaults):**
```bash
ENFORCE_AUTH = true          # Set to 'false' for testing without auth
DATABASE_URL = sqlite:////data/odeadev_tts.db
PORT = 8000                  # Render auto-sets this
LOG_LEVEL = INFO
```

**Security (auto-generated):**
```bash
SECRET_KEY = [Auto Generate]  # Click "Generate" button
```

### Step 5: Add Persistent Disk (Recommended)

Under **"Disk"** section:
- **Name**: `data`
- **Mount Path**: `/data`
- **Size**: 1 GB (free tier includes 1GB)

This persists your SQLite database across deployments.

---

## 🎯 Deploy & Test

### Deploy

Click **"Create Web Service"** - Render will:
1. Clone your repository
2. Build the Docker image
3. Initialize the database
4. Start the service

**Build time:** ~3-5 minutes

### Get Your Service URL

Once deployed, you'll see:
```
Your service is live at:
https://odeadev-ai-tts.onrender.com
```

### Test Health Check

```bash
curl https://odeadev-ai-tts.onrender.com/health
```

**Expected response:**
```json
{"status": "ok"}
```

### View API Documentation

Open in browser:
```
https://odeadev-ai-tts.onrender.com/docs
```

---

## 🔑 Create Your First User

### Option 1: Using Render Shell (Recommended)

1. In Render dashboard → Your service → **"Shell"** tab
2. Run:
```bash
python -m src.create_admin "Your Name" "your@email.com"
```

3. **SAVE THE API KEY** shown in the output!

### Option 2: Disable Auth for Testing

If you want to test without auth first:

1. Add environment variable: `ENFORCE_AUTH = false`
2. Deploy
3. Test TTS without Authorization header:

```bash
curl -X POST https://odeadev-ai-tts.onrender.com/v1/tts \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello from Render!",
    "voice_name": "nigerian-male"
  }' | jq -r '.audio_base64' | base64 -d > render_test.mp3
```

4. **IMPORTANT:** Set `ENFORCE_AUTH = true` before going to production!

---

## 🧪 Full API Test (with Auth)

### 1. Test with your API key:

```bash
# Set your API key (from create_admin command)
export API_KEY="your-api-key-here"
export RENDER_URL="https://odeadev-ai-tts.onrender.com"

# Check your account
curl -X GET $RENDER_URL/v1/me \
  -H "Authorization: Bearer $API_KEY"

# List voices
curl -X GET $RENDER_URL/v1/voices \
  -H "Authorization: Bearer $API_KEY"

# Generate speech
curl -X POST $RENDER_URL/v1/tts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "text": "Welcome to OdeaDev AI Text to Speech, deployed on Render!",
    "voice_name": "nigerian-male",
    "model": "speech-02-turbo",
    "speed": 1.0,
    "emotion": "happy"
  }' | jq -r '.audio_base64' | base64 -d > welcome.mp3

# Play audio (macOS)
afplay welcome.mp3

# Play audio (Linux)
mpg123 welcome.mp3
```

---

## 👥 Create Customer API Keys (Admin)

```bash
curl -X POST $RENDER_URL/admin/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "name": "Customer Name",
    "email": "customer@example.com",
    "plan": "basic"
  }'
```

**Response includes new API key** - give this to your customer!

---

## 🔌 n8n Webhook Integration Examples

### Example 1: WhatsApp → TTS → Audio Response

**n8n Workflow:**

```
1. Webhook Trigger (WhatsApp message received)
   ↓
2. HTTP Request Node
   POST https://odeadev-ai-tts.onrender.com/v1/tts
   Headers: 
     Authorization: Bearer YOUR_API_KEY
   Body:
     {
       "text": "{{$json.message.text}}",
       "voice_name": "nigerian-male"
     }
   ↓
3. Set Node (convert base64 to file)
   audio_url = "data:audio/mp3;base64," + {{$json.audio_base64}}
   ↓
4. WhatsApp Node (send audio)
   Send audio_url back to user
```

**n8n HTTP Request Configuration:**
```json
{
  "method": "POST",
  "url": "https://odeadev-ai-tts.onrender.com/v1/tts",
  "authentication": "genericCredentialType",
  "genericAuthType": "httpHeaderAuth",
  "httpHeaderAuth": {
    "name": "Authorization",
    "value": "Bearer YOUR_API_KEY"
  },
  "sendBody": true,
  "bodyParameters": {
    "parameters": [
      {
        "name": "text",
        "value": "={{$json.message.text}}"
      },
      {
        "name": "voice_name",
        "value": "nigerian-male"
      }
    ]
  },
  "options": {}
}
```

### Example 2: Telegram Bot with Voice Selection

```
1. Telegram Trigger (bot command /speak)
   ↓
2. Switch Node (check voice preference)
   - If user_country = "NG" → nigerian-male
   - If user_country = "US" → american-male
   - If user_country = "GB" → british-female
   ↓
3. HTTP Request (TTS API)
   ↓
4. Convert Node (base64 → binary)
   ↓
5. Telegram Node (send voice message)
```

### Example 3: Slack → TTS Announcements

```
1. Slack Trigger (new message in #announcements)
   ↓
2. HTTP Request (TTS API)
   POST https://odeadev-ai-tts.onrender.com/v1/tts
   Body: {
     "text": "{{$json.text}}",
     "voice_name": "american-male",
     "emotion": "neutral"
   }
   ↓
3. Upload to S3/Cloud Storage
   ↓
4. Slack Node (share audio link)
```

### Example 4: REST Webhook (Generic)

**Webhook endpoint you can call from anywhere:**

```bash
# Your n8n webhook URL
WEBHOOK_URL="https://your-n8n.com/webhook/tts"

# Call it
curl -X POST $WEBHOOK_URL \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello world",
    "voice": "nigerian-male",
    "user_api_key": "customer-api-key-here"
  }'
```

**n8n workflow receives this and:**
1. Validates user_api_key
2. Calls your TTS API
3. Returns audio_base64 or stores file
4. Sends response back

---

## 📊 Monitoring on Render

### View Logs

Dashboard → Your Service → **"Logs"** tab

**Useful log filters:**
- `ERROR` - See errors only
- `INFO` - General information
- `TTS generation` - Track API calls

### Metrics

Dashboard → Your Service → **"Metrics"** tab

Monitor:
- **CPU usage**
- **Memory usage**
- **Response time**
- **Request count**

### Alerts

Set up alerts for:
- Service down (automatic with health checks)
- High error rate
- High memory usage

---

## 🔄 Continuous Deployment

### Auto-deploy on Git Push

Already enabled! Every time you push to `main`:

```bash
git add .
git commit -m "Update voice settings"
git push origin main
```

Render automatically:
1. Pulls new code
2. Rebuilds Docker image
3. Deploys with zero downtime

### Manual Deploy

Dashboard → Your Service → **"Manual Deploy"** → **"Deploy latest commit"**

---

## 💰 Cost Optimization

### Free Tier Limitations
- **Sleeps after 15 min inactivity**
- **750 hours/month free**
- First request after sleep: ~30 seconds cold start

### Starter Plan ($7/month)
- **No sleep**
- **Always on**
- **512 MB RAM** (suitable for low-moderate traffic)
- Recommended for production

### Pro Plan ($25/month)
- **2 GB RAM**
- **Better performance**
- Suitable for high traffic

### Database Options

**SQLite (Current)**
- ✅ Free
- ✅ Simple
- ⚠️ Limited concurrent writes
- 💡 Good for: <1000 requests/day

**PostgreSQL (Upgrade)**
- ✅ Better performance
- ✅ Concurrent access
- ✅ Managed by Render
- 💰 $7/month
- 💡 Good for: >1000 requests/day

**To switch to PostgreSQL:**
1. Add PostgreSQL database in Render
2. Copy connection string
3. Update `DATABASE_URL` environment variable

---

## 🔒 Production Security Checklist

- [x] `ENFORCE_AUTH = true`
- [x] `SECRET_KEY` auto-generated
- [ ] HTTPS enabled (automatic on Render)
- [ ] API keys rotated regularly
- [ ] Rate limiting enabled (Phase 5 feature)
- [ ] Monitoring alerts configured
- [ ] Backup strategy for database
- [ ] MiniMax API key stored as secret

---

## 🐛 Troubleshooting

### Service Won't Start

**Check logs:**
```
Dashboard → Logs → Look for errors
```

**Common issues:**
- Missing `MINIMAX_API_KEY`
- Missing `MINIMAX_GROUP_ID`
- Invalid Docker configuration

**Solution:** Verify all environment variables are set

### "Insufficient Balance" Error

**Error message:**
```
Insufficient balance in MiniMax account
```

**Solution:** Add credits at https://platform.minimaxi.com/

### Database Errors

**Error:**
```
database is locked
```

**Solution:** Upgrade to PostgreSQL for production

### Slow Response Times

**Free tier:** Service is asleep
**Solution:** Upgrade to Starter plan or use a keep-alive ping

**Keep-alive with cron:**
```bash
# Ping every 10 minutes to keep awake
*/10 * * * * curl https://odeadev-ai-tts.onrender.com/health
```

---

## 📈 Next Steps

1. ✅ **Deploy to Render**
2. ✅ **Create admin user**
3. ✅ **Test TTS endpoint**
4. 📱 **Integrate with n8n/WhatsApp/Telegram**
5. 👥 **Create customer API keys**
6. 📊 **Monitor usage and performance**
7. 💰 **Upgrade plan as needed**

---

## 🆘 Support

- **Render Docs**: https://render.com/docs
- **Project README**: [README.md](README.md)
- **Architecture**: [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)
- **MiniMax**: https://platform.minimaxi.com/

---

**🎉 Your service is now live on Render!**

Share your API endpoint with customers and start generating speech! 🚀
