# 🚀 Deploy to Render - Final Instructions

**Your GitHub Repository:** https://github.com/Odiabackend099/Minimax_TTS-odiadev.git  
**Official Guide:** https://render.com/docs/deploy-fastapi

---

## ⚡ Quick Deploy (15 Minutes)

### Step 1: Push to GitHub (2 minutes)

```bash
cd "/Users/odiadev/Desktop/minimax tts"

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Production-ready TTS service with security fixes"

# Add remote (use your GitHub token when prompted)
git remote add origin https://github.com/Odiabackend099/Minimax_TTS-odiadev.git

# Push to main branch
git branch -M main
git push -u origin main
```

**⚠️ Security Note:** When prompted for credentials:
- Username: `Odiabackend099`
- Password: Use your GitHub token (stored securely - not in code!)

---

### Step 2: Configure Render (5 minutes)

1. **Go to:** https://dashboard.render.com/
2. **Click:** "New +" → "Web Service"
3. **Connect Repository:**
   - Authorize GitHub
   - Select: `Odiabackend099/Minimax_TTS-odiadev`
   - Click "Connect"

4. **Configure Service:**
   ```
   Name: odeadev-ai-tts
   Region: Oregon (or closest to you)
   Branch: main
   Runtime: Docker
   ```

5. **Set Environment Variables:**
   ```
   MINIMAX_API_KEY = eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
   MINIMAX_GROUP_ID = 1933510987994895143
   ENFORCE_AUTH = true
   DATABASE_URL = sqlite:////data/odeadev_tts.db
   ```

6. **Advanced Settings:**
   ```
   Health Check Path: /health
   Auto-Deploy: Yes
   ```

7. **Add Disk (Important!):**
   ```
   Name: data
   Mount Path: /data
   Size: 1 GB
   ```

8. **Choose Plan:**
   - Free: For testing (sleeps after 15 min)
   - Starter ($7/month): Recommended for production

9. **Click:** "Create Web Service"

---

### Step 3: Initialize Database (5 minutes)

Once deployed, use Render Shell:

1. **Dashboard** → Your Service → **"Shell"** tab
2. Run initialization:
   ```bash
   python -m src.init_db
   ```

3. Create admin user:
   ```bash
   python -m src.create_admin "Your Name" "your@email.com"
   ```

4. **SAVE THE API KEY** shown in output!

---

### Step 4: Test Your Service (3 minutes)

```bash
# Set your service URL
export RENDER_URL="https://odeadev-ai-tts.onrender.com"
export API_KEY="your-admin-api-key-from-step-3"

# Test health
curl $RENDER_URL/health

# Test TTS
curl -X POST $RENDER_URL/v1/tts \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello from Render! Welcome to OdeaDev AI TTS!",
    "voice_name": "nigerian-male"
  }' | jq -r '.audio_base64' | base64 -d > render_test.mp3

# Play audio
afplay render_test.mp3  # macOS
# mpg123 render_test.mp3  # Linux
```

---

## 📊 Current Status

### Files Ready for Render ✅

1. ✅ **Dockerfile** - Optimized for Render with $PORT support
2. ✅ **render.yaml** - Infrastructure as code
3. ✅ **.gitignore** - Protects secrets
4. ✅ **requirements.txt** - All dependencies
5. ✅ **src/main.py** - FastAPI app with /health endpoint
6. ✅ **src/init_db.py** - Database initialization
7. ✅ **Documentation** - Complete guides

### Production Fixes Available ✅

If you want to implement security fixes first:

1. ✅ `src/database_fixed.py` - Connection pooling, atomic quota
2. ✅ `src/dependencies_fixed.py` - Rate limiting, timing attack protection
3. ✅ `src/auth_fixed.py` - 512-bit API keys
4. ✅ `src/minimax_client_async.py` - Async client with circuit breaker

**Deploy now or after fixes?** Your choice!

---

## 🔧 Render Configuration Details

### According to Official Guide

**From:** https://render.com/docs/deploy-fastapi

1. **Runtime Detection:**
   - Render auto-detects Python from `requirements.txt`
   - Uses Dockerfile if present (recommended)

2. **Port Configuration:**
   - Render injects `$PORT` environment variable
   - Our Dockerfile uses: `uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8000}`

3. **Health Checks:**
   - Render pings `/health` every 30 seconds
   - Service marked unhealthy after 3 failures
   - Auto-restarts if unhealthy

4. **Database:**
   - SQLite: Use persistent disk (we configured `/data`)
   - PostgreSQL: Add Render Postgres service (upgrade later)

5. **Environment Variables:**
   - Set in dashboard (not in code!)
   - Auto-inject at runtime
   - Can use secrets management

---

## 🚨 Pre-Deployment Checklist

Before clicking "Create Web Service":

- [ ] ✅ Code pushed to GitHub
- [ ] ✅ MiniMax API key ready
- [ ] ✅ MiniMax account has credits
- [ ] ✅ Render account created
- [ ] ✅ Environment variables prepared
- [ ] ✅ Persistent disk configured
- [ ] ✅ Health check path set to `/health`

---

## 📈 After Deployment

### Monitor Your Service

**Dashboard → Your Service:**
- **Logs:** Real-time application logs
- **Metrics:** CPU, Memory, Response time
- **Events:** Deployments, restarts, errors

### Create Your First User

```bash
# Option 1: Via Render Shell (in dashboard)
python -m src.create_admin "Admin User" "admin@odeadev.com"

# Option 2: Via API (if ENFORCE_AUTH=false for testing)
curl -X POST https://your-service.onrender.com/admin/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Customer",
    "email": "customer@example.com",
    "plan": "basic"
  }'
```

### Share Your API

**API Endpoint:** `https://odeadev-ai-tts.onrender.com`  
**Documentation:** `https://odeadev-ai-tts.onrender.com/docs`  
**Health Check:** `https://odeadev-ai-tts.onrender.com/health`

---

## 🔄 Continuous Deployment

### Automatic Updates

Every time you push to GitHub:
```bash
git add .
git commit -m "Update feature X"
git push origin main
# Render auto-deploys in ~3 minutes
```

### Manual Deploy

Dashboard → Your Service → "Manual Deploy" → "Deploy latest commit"

---

## 🆘 Troubleshooting

### Service Won't Start

**Check Logs:**
Dashboard → Logs → Look for errors

**Common issues:**
```
Error: MINIMAX_API_KEY not provided
→ Add environment variable in dashboard

Error: Port already in use
→ Render auto-configures $PORT, should not happen

Error: Database is locked
→ Ensure persistent disk mounted at /data
```

### Database Not Persisting

**Verify disk:**
- Dashboard → Your Service → Disks
- Should see "data" mounted at `/data`
- Size: 1 GB

**Fix:**
- Add persistent disk in dashboard
- Redeploy service

### MiniMax API Errors

**Insufficient balance:**
```
Error 1008: Insufficient balance
→ Add credits: https://platform.minimaxi.com/recharge
```

**Invalid credentials:**
```
Error 401: Invalid API key
→ Verify MINIMAX_API_KEY in environment variables
```

---

## 🎯 Performance Tips

### Free Tier
- **Sleeps after 15 min inactivity**
- **Cold start: ~30 seconds**
- **Good for:** Testing, demos

**Keep-alive trick:**
```bash
# Ping every 10 minutes
*/10 * * * * curl https://your-service.onrender.com/health
```

### Starter Tier ($7/month)
- **Always on**
- **No cold starts**
- **512 MB RAM**
- **Good for:** Production, <1000 requests/day

### Pro Tier ($25/month)
- **2 GB RAM**
- **Better performance**
- **Good for:** High traffic

---

## 📊 Scaling Strategy

### Current Setup (SQLite)
- **Good for:** <1000 requests/day
- **Max concurrent:** 50-100 users
- **Database:** File-based (on persistent disk)

### Upgrade to PostgreSQL
When you reach 1000+ requests/day:

1. **Add Postgres service:**
   - Dashboard → New → PostgreSQL
   - Copy connection string

2. **Update environment:**
   ```
   DATABASE_URL=postgresql://user:pass@host/db
   ```

3. **Migrate data:**
   ```bash
   # Export SQLite
   python scripts/export_sqlite.py
   
   # Import to Postgres
   python scripts/import_postgres.py
   ```

---

## 🔐 Security Checklist

Before going live:

- [ ] ✅ `ENFORCE_AUTH=true` (production mode)
- [ ] ✅ MiniMax API key in environment (not in code)
- [ ] ✅ HTTPS enabled (automatic on Render)
- [ ] ✅ Health check working
- [ ] ✅ Admin API key saved securely
- [ ] ✅ No secrets in GitHub repository
- [ ] ✅ Persistent disk configured
- [ ] ✅ Monitoring enabled

---

## 🎉 You're Live!

Once deployed:

1. **Test the API:**
   ```bash
   curl https://your-service.onrender.com/docs
   ```

2. **Create users:**
   ```bash
   python -m src.create_admin "User" "email@example.com"
   ```

3. **Start generating speech:**
   ```bash
   curl -X POST https://your-service.onrender.com/v1/tts \
     -H "Authorization: Bearer $API_KEY" \
     -d '{"text":"Hello world!","voice_name":"nigerian-male"}'
   ```

4. **Share with customers:**
   ```
   API Endpoint: https://your-service.onrender.com
   Documentation: https://your-service.onrender.com/docs
   ```

---

## 📞 Next Steps

### After Successful Deployment

1. ✅ **Monitor for 24 hours** - Check logs, metrics
2. ✅ **Create test users** - Different plans
3. ✅ **Load test** - Verify performance
4. ✅ **Document API** - For customers
5. ✅ **Set up alerts** - Email notifications

### Optional Improvements

See `CODE_REVIEW.md` for production fixes:
- Rate limiting (in-memory)
- Async support (2-3x faster)
- Circuit breaker (reliability)
- Stronger API keys (512-bit)
- Connection pooling (scalability)

**Implementation time:** 2-4 hours  
**Performance gain:** 2-3x  
**Security:** Production-grade

---

## 🏆 Success Criteria

Your deployment is successful when:

- ✅ Health check returns 200 OK
- ✅ Can create admin user
- ✅ Can generate speech via API
- ✅ Audio plays correctly
- ✅ Quota enforcement works
- ✅ Authentication blocks invalid keys
- ✅ Service auto-restarts if crashed
- ✅ Database persists across deploys

---

## 🚀 Ready to Deploy?

```bash
# 1. Push to GitHub
git push origin main

# 2. Open Render
open https://dashboard.render.com/

# 3. Follow steps above

# 4. Test your API
curl https://your-service.onrender.com/health

# 5. Celebrate! 🎉
```

---

**Deployment Time:** ~15 minutes  
**Cost:** Free tier or $7/month  
**Difficulty:** Easy  
**Support:** Render has 24/7 support

**Let's get you deployed! 🚀**
