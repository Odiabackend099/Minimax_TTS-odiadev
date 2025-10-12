# 🚀 Deployment Guide for OdeaDev-AI-TTS

Complete deployment instructions for production environments.

---

## 🐳 Docker Deployment (Recommended)

### Quick Start with Docker Compose

```bash
# 1. Build and start
docker-compose up -d

# 2. Check logs
docker-compose logs -f

# 3. Stop
docker-compose down
```

### Manual Docker Build

```bash
# Build image
docker build -t odeadev-ai-tts:latest .

# Run container
docker run -d \
  --name odeadev-tts \
  -p 8000:8000 \
  -e MINIMAX_API_KEY="your-key" \
  -e MINIMAX_GROUP_ID="your-group-id" \
  -v $(pwd)/data:/data \
  odeadev-ai-tts:latest

# View logs
docker logs -f odeadev-tts
```

---

## ☁️ RunPod Deployment

### Method 1: Docker Image (Recommended)

1. **Build and push your image:**

```bash
# Build
docker build -t your-dockerhub-username/odeadev-tts:latest .

# Login to Docker Hub
docker login

# Push
docker push your-dockerhub-username/odeadev-tts:latest
```

2. **Deploy on RunPod:**
   - Go to RunPod.io → Deploy
   - Select "Deploy a Custom Docker Image"
   - Image name: `your-dockerhub-username/odeadev-tts:latest`
   - Container disk: 5GB minimum
   - Expose HTTP port: 8000
   - Environment variables:
     ```
     MINIMAX_API_KEY=your-key-here
     MINIMAX_GROUP_ID=your-group-id
     DATABASE_URL=sqlite:////data/odeadev_tts.db
     ```

3. **Create admin user:**
```bash
# SSH into pod
runpodctl ssh <pod-id>

# Create admin
python -m src.create_admin "Admin" "admin@example.com"
```

### Method 2: Direct Python Deployment

1. **Clone repository on pod:**
```bash
git clone https://github.com/your-repo/odeadev-tts.git
cd odeadev-tts
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment:**
```bash
cp .env.example .env
nano .env  # Add your credentials
```

4. **Initialize and run:**
```bash
python -m src.init_db
python -m src.create_admin "Admin" "admin@example.com"
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

---

## 🌐 Production Setup

### Using Nginx as Reverse Proxy

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### SSL with Let's Encrypt

```bash
# Install certbot
apt-get install certbot python3-certbot-nginx

# Get certificate
certbot --nginx -d your-domain.com

# Auto-renewal
certbot renew --dry-run
```

---

## 🗄️ Database Migration (SQLite → PostgreSQL)

For production, use PostgreSQL instead of SQLite:

### 1. Setup PostgreSQL

```bash
# Docker
docker run -d \
  --name postgres \
  -e POSTGRES_PASSWORD=yourpassword \
  -e POSTGRES_DB=odeadev_tts \
  -p 5432:5432 \
  postgres:15-alpine
```

### 2. Update Environment

```bash
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/odeadev_tts
```

### 3. Migrate Data (if needed)

```bash
# Export from SQLite
sqlite3 odeadev_tts.db .dump > backup.sql

# Import to PostgreSQL (manual process)
# Or use a migration tool like pgloader
```

---

## 📊 Monitoring

### Health Check Endpoint

```bash
curl http://your-domain.com/health
```

### Prometheus Metrics (Optional)

Add to `requirements.txt`:
```
prometheus-fastapi-instrumentator==6.1.0
```

Add to `src/main.py`:
```python
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

Access metrics at: `http://your-domain.com/metrics`

---

## 🔒 Security Checklist

- [ ] Change default `SECRET_KEY` in `.env`
- [ ] Use HTTPS in production (SSL certificate)
- [ ] Rotate API keys regularly
- [ ] Set up firewall rules (only expose port 80/443)
- [ ] Enable database backups
- [ ] Use environment variables for secrets (never hardcode)
- [ ] Limit request rate (add rate limiting middleware)
- [ ] Monitor logs for suspicious activity
- [ ] Keep dependencies updated (`pip list --outdated`)

---

## 🔄 Backup Strategy

### Automated Backup Script

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
DB_FILE="/data/odeadev_tts.db"

# Create backup
sqlite3 $DB_FILE .dump | gzip > $BACKUP_DIR/backup_$DATE.sql.gz

# Keep only last 7 days
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +7 -delete

echo "Backup completed: backup_$DATE.sql.gz"
```

### Cron Job

```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * /app/backup.sh
```

---

## 🧪 Testing in Production

### Smoke Tests

```bash
# Health check
curl http://your-domain.com/health

# Create test user (admin key required)
curl -X POST http://your-domain.com/admin/users \
  -H "Authorization: Bearer $ADMIN_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@test.com","plan":"free"}'

# Generate test audio
curl -X POST http://your-domain.com/v1/tts \
  -H "Authorization: Bearer $TEST_USER_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text":"Testing production deployment"}' \
  | jq -r '.audio_base64' | base64 -d > test.mp3
```

---

## 📈 Scaling Considerations

### Horizontal Scaling

- Deploy multiple instances behind a load balancer
- Use PostgreSQL for shared database state
- Consider Redis for rate limiting (shared state)

### Vertical Scaling

- Increase CPU/RAM for the container
- Optimize database queries
- Add database indexes for frequently queried fields

### Caching

Add caching for:
- Voice list queries
- User quota checks (with TTL)
- MiniMax voice IDs mapping

---

## 🆘 Troubleshooting

### Container Won't Start

```bash
# Check logs
docker logs odeadev-tts

# Common issues:
# - Missing environment variables
# - Port already in use
# - Database permission issues
```

### Database Locked Error (SQLite)

Solution: Switch to PostgreSQL or ensure only one process accesses the database.

### MiniMax API Errors

```bash
# Check credentials
echo $MINIMAX_API_KEY
echo $MINIMAX_GROUP_ID

# Test direct API call
curl -X POST https://api.minimaxi.chat/v1/t2a_v2?GroupId=$MINIMAX_GROUP_ID \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text":"test","model":"speech-02-turbo","voice_setting":{"voice_id":"male-qn-qingse"}}'
```

---

## 🔄 Updates & Maintenance

### Update Application

```bash
# Pull latest code
git pull

# Rebuild Docker image
docker-compose build

# Restart with new image
docker-compose up -d
```

### Database Migrations

When models change:
```bash
# Backup first!
sqlite3 odeadev_tts.db .dump > backup.sql

# Modify models in src/models.py

# Drop and recreate (dev only)
rm odeadev_tts.db
python -m src.init_db

# Production: Use Alembic for migrations
pip install alembic
alembic init migrations
# ... configure and run migrations
```

---

## 📞 Support

- **Issues:** GitHub Issues
- **Documentation:** [README.md](README.md)
- **Planning:** [planning.md](planning.md)

---

**🎉 Your production deployment is ready!**
