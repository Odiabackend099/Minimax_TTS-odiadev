# ✅ Render Deployment Checklist

Complete checklist to deploy OdeaDev-AI-TTS to Render.com

---

## 📋 Pre-Deployment

### 1. Verify Local Setup Works

- [ ] `uvicorn src.main:app --reload` runs without errors
- [ ] Health check responds: `curl http://localhost:8000/health`
- [ ] API docs load: http://localhost:8000/docs
- [ ] Database initialized: `odeadev_tts.db` file exists
- [ ] At least one admin user created

### 2. MiniMax Account Ready

- [ ] MiniMax account created at https://platform.minimaxi.com/
- [ ] Credits added to account (minimum $5 recommended)
- [ ] API Key (JWT token) copied
- [ ] Group ID copied
- [ ] Test voice ID confirmed

### 3. GitHub Repository

- [ ] GitHub account created
- [ ] New repository created (public or private)
- [ ] Git initialized in project folder
- [ ] All files committed
- [ ] Pushed to GitHub main branch

**Quick commands:**
```bash
cd "/Users/odiadev/Desktop/minimax tts"
git init
git add .
git commit -m "Initial commit: OdeaDev-AI-TTS"
git remote add origin https://github.com/YOUR_USERNAME/odeadev-ai-tts.git
git branch -M main
git push -u origin main
```

---

## 🚀 Render Setup

### 4. Create Render Account

- [ ] Go to https://render.com
- [ ] Sign up (use GitHub OAuth for easy integration)
- [ ] Verify email address
- [ ] Dashboard accessible

### 5. Create Web Service

- [ ] Click "New +" → "Web Service"
- [ ] Connect GitHub account
- [ ] Select `odeadev-ai-tts` repository
- [ ] Click "Connect"

### 6. Configure Service Settings

**Basic Settings:**
- [ ] **Name**: `odeadev-ai-tts` (or your preferred name)
- [ ] **Region**: Oregon (or closest to your users)
- [ ] **Branch**: `main`
- [ ] **Runtime**: **Docker** ⚠️ IMPORTANT!

**Instance Type:**
- [ ] **Free** (for testing - sleeps after 15 min)
- [ ] **Starter** ($7/month - recommended for production)

**Advanced Settings:**
- [ ] **Health Check Path**: `/health`
- [ ] **Auto-Deploy**: Yes

### 7. Add Environment Variables

Click "Advanced" → "Add Environment Variable"

**Required (Set manually):**
- [ ] `MINIMAX_API_KEY` = `your-jwt-token-here`
- [ ] `MINIMAX_GROUP_ID` = `1933510987994895143`

**Security (Auto-generate):**
- [ ] `SECRET_KEY` = Click "Generate"

**Optional (Good defaults):**
- [ ] `ENFORCE_AUTH` = `true` (set `false` for testing without auth)
- [ ] `DATABASE_URL` = `sqlite:////data/odeadev_tts.db`
- [ ] `LOG_LEVEL` = `INFO`

### 8. Add Persistent Disk

- [ ] Scroll to "Disk" section
- [ ] Click "Add Disk"
- [ ] **Name**: `data`
- [ ] **Mount Path**: `/data`
- [ ] **Size**: 1 GB (free)

**Why?** Persists your SQLite database across deployments.

---

## 🎬 Deploy

### 9. Start Deployment

- [ ] Click "Create Web Service"
- [ ] Wait for build (3-5 minutes)
- [ ] Check logs for errors
- [ ] Wait for "Your service is live" message

**Build process:**
1. ✅ Clone repository
2. ✅ Build Docker image
3. ✅ Initialize database
4. ✅ Start Uvicorn server

### 10. Verify Deployment

- [ ] Service URL shown: `https://odeadev-ai-tts.onrender.com`
- [ ] Status shows "Live" (green)
- [ ] No errors in logs

---

## 🧪 Testing

### 11. Test Health Check

```bash
curl https://odeadev-ai-tts.onrender.com/health
```

**Expected:**
```json
{"status": "ok"}
```

- [ ] Health check returns 200 OK
- [ ] Response shows `{"status": "ok"}`

### 12. View API Documentation

- [ ] Open: https://odeadev-ai-tts.onrender.com/docs
- [ ] Swagger UI loads
- [ ] All endpoints visible
- [ ] Try "Expand Operations"

### 13. Create Admin User

**Option A: Using Render Shell**
1. [ ] Dashboard → Your Service → "Shell" tab
2. [ ] Run: `python -m src.create_admin "Your Name" "your@email.com"`
3. [ ] **SAVE THE API KEY!** (shown only once)

**Option B: Disable Auth Temporarily**
1. [ ] Set `ENFORCE_AUTH = false` in environment variables
2. [ ] Test TTS without auth (see below)
3. [ ] **RE-ENABLE:** Set `ENFORCE_AUTH = true` before production!

### 14. Test TTS Endpoint

**With Auth (Production):**
```bash
# Replace with your API key from step 13
export API_KEY="your-api-key-here"

curl -X POST https://odeadev-ai-tts.onrender.com/v1/tts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "text": "Hello from Render! This is OdeaDev AI TTS.",
    "voice_name": "nigerian-male"
  }' | jq -r '.audio_base64' | base64 -d > test.mp3
```

**Without Auth (Testing only):**
```bash
curl -X POST https://odeadev-ai-tts.onrender.com/v1/tts \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Testing without auth",
    "voice_name": "nigerian-male"
  }' | jq -r '.audio_base64' | base64 -d > test.mp3
```

**Verify:**
- [ ] Command completes without errors
- [ ] `test.mp3` file created
- [ ] Audio file plays correctly: `afplay test.mp3` (macOS) or `mpg123 test.mp3` (Linux)

### 15. Test User Info Endpoint

```bash
curl -X GET https://odeadev-ai-tts.onrender.com/v1/me \
  -H "Authorization: Bearer $API_KEY"
```

**Expected:**
```json
{
  "id": 1,
  "name": "Your Name",
  "email": "your@email.com",
  "plan": "enterprise",
  "quota_seconds": 36000,
  "used_seconds": 4.8,
  "remaining_seconds": 35995.2,
  "quota_percentage_used": 0.01,
  "is_active": true,
  "created_at": "2025-01-12T02:30:00"
}
```

- [ ] Returns user details
- [ ] Shows correct quota and usage
- [ ] `is_active` is `true`

### 16. Test Voice Listing

```bash
curl -X GET https://odeadev-ai-tts.onrender.com/v1/voices \
  -H "Authorization: Bearer $API_KEY"
```

**Expected:**
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
    "created_at": "2025-01-12T02:30:00"
  }
]
```

- [ ] Returns array of voices
- [ ] At least 3 default voices present
- [ ] All voices show `is_active: true`

---

## 👥 Production Setup

### 17. Create Customer API Keys

```bash
curl -X POST https://odeadev-ai-tts.onrender.com/admin/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "name": "Test Customer",
    "email": "customer@example.com",
    "plan": "basic"
  }'
```

**Response includes:**
```json
{
  "user": { ... },
  "api_key": "customer-api-key-here"
}
```

- [ ] Customer user created
- [ ] API key received
- [ ] Save customer API key securely
- [ ] Test with customer key

### 18. Configure Production Settings

- [ ] `ENFORCE_AUTH` = `true` ✅
- [ ] Admin API key stored securely (password manager)
- [ ] Customer API keys documented
- [ ] Billing plans configured

### 19. Set Up Monitoring

**Render Dashboard:**
- [ ] Check "Metrics" tab
- [ ] Enable email alerts (Settings → Notifications)
- [ ] Set up alerts for:
  - Service down
  - High error rate
  - High memory usage

**External Monitoring (Optional):**
- [ ] Set up UptimeRobot: https://uptimerobot.com
- [ ] Monitor health endpoint every 5 minutes
- [ ] Get notified if service goes down

### 20. Backup Strategy

- [ ] Document backup procedure
- [ ] Schedule regular database backups
- [ ] Store backups securely (S3, Dropbox, etc.)

**Quick backup via Render Shell:**
```bash
# In Render Shell
sqlite3 /data/odeadev_tts.db .dump > backup.sql
# Copy output and save locally
```

---

## 🔗 Integration

### 21. n8n Integration (Optional)

If using n8n workflows:
- [ ] Read [N8N_INTEGRATION.md](N8N_INTEGRATION.md)
- [ ] Set up n8n webhook
- [ ] Configure HTTP Request nodes
- [ ] Add OdeaDev API key to n8n credentials
- [ ] Test WhatsApp/Telegram integrations

### 22. Custom Domain (Optional)

**Render Custom Domain:**
1. [ ] Go to Settings → Custom Domain
2. [ ] Add your domain: `tts.yourdomain.com`
3. [ ] Add CNAME record in your DNS:
   - Name: `tts`
   - Value: `odeadev-ai-tts.onrender.com`
4. [ ] Wait for SSL certificate (automatic)

---

## 📊 Post-Deployment

### 23. Performance Optimization

- [ ] Monitor response times in Render Metrics
- [ ] Upgrade to Starter plan if using Free tier
- [ ] Consider PostgreSQL if >1000 requests/day

### 24. Documentation

- [ ] Document your service URL
- [ ] Create API key management process
- [ ] Write customer onboarding guide
- [ ] Update team documentation

### 25. Marketing & Launch

- [ ] Announce service to customers
- [ ] Share API documentation
- [ ] Provide example code snippets
- [ ] Offer free trial periods

---

## 🐛 Troubleshooting

### Common Issues Checklist

**Service won't start:**
- [ ] Check logs for errors
- [ ] Verify all environment variables set
- [ ] Ensure `MINIMAX_API_KEY` is valid
- [ ] Check Docker build logs

**Database errors:**
- [ ] Verify persistent disk is attached
- [ ] Check disk space usage
- [ ] Ensure mount path is `/data`

**Authentication errors:**
- [ ] Verify `Authorization: Bearer TOKEN` format
- [ ] Check API key is correct
- [ ] Ensure user is active in database

**MiniMax API errors:**
- [ ] Check MiniMax account balance
- [ ] Verify API key and Group ID
- [ ] Test MiniMax API directly

**Slow response:**
- [ ] Free tier may be sleeping (upgrade to Starter)
- [ ] Check MiniMax API response time
- [ ] Monitor Render metrics

---

## ✅ Final Checklist

Before going live:

- [ ] ✅ Service deployed and accessible
- [ ] ✅ Health check passing
- [ ] ✅ Admin user created with API key saved
- [ ] ✅ At least one test customer created
- [ ] ✅ TTS endpoint tested successfully
- [ ] ✅ Audio output plays correctly
- [ ] ✅ `ENFORCE_AUTH = true` enabled
- [ ] ✅ Monitoring alerts configured
- [ ] ✅ Backup strategy documented
- [ ] ✅ Customer documentation prepared
- [ ] ✅ MiniMax account funded
- [ ] ✅ DNS configured (if using custom domain)

---

## 🎉 Launch!

Your OdeaDev-AI-TTS service is now live on Render!

**Next steps:**
1. Share API documentation with customers
2. Create customer API keys
3. Monitor usage and performance
4. Scale as needed

**Service URL:**
```
https://odeadev-ai-tts.onrender.com
```

**API Docs:**
```
https://odeadev-ai-tts.onrender.com/docs
```

---

## 📞 Support Resources

- **Render Docs**: https://render.com/docs
- **Project README**: [README.md](README.md)
- **Render Deployment**: [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)
- **n8n Integration**: [N8N_INTEGRATION.md](N8N_INTEGRATION.md)
- **MiniMax Platform**: https://platform.minimaxi.com/

---

**Total time to deploy:** ~20 minutes  
**Status:** 🚀 **READY FOR PRODUCTION**
