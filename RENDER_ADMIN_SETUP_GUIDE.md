# 🔧 ODIADEV TTS - Render Admin Setup Guide

## **PROBLEM IDENTIFIED** ❌

The service is still enforcing authentication even though we set `ENFORCE_AUTH=false` in the environment variables. This means the environment variable is not being properly applied.

---

## **SOLUTION 1: Fix Environment Variables in Render** ✅

### **Step 1: Access Render Dashboard**
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Find your service: `minimax-tts-odiadev`
3. Click on the service name

### **Step 2: Update Environment Variables**
1. Click on **"Environment"** tab
2. Add/Update these environment variables:

```
ENFORCE_AUTH=false
ADMIN_API_KEY=your_admin_key_here
MINIMAX_API_KEY=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJHcm91cE5hbWUiOiJPRElBIGJhY2tlbmQiLCJVc2VyTmFtZSI6Ik9ESUEgYmFja2VuZCIsIkFjY291bnQiOiIiLCJTdWJqZWN0SUQiOiIxOTMzNTEwOTg4MDAzMjgzNzUxIiwiUGhvbmUiOiIiLCJHcm91cElEIjoiMTkzMzUxMDk4Nzk5NDg5NTE0MyIsIlBhZ2VOYW1lIjoiIiwiTWFpbCI6Im9kaWFiYWNrZW5kQGdtYWlsLmNvbSIsIkNyZWF0ZVRpbWUiOiIyMDI1LTEwLTEyIDA3OjU0OjM2IiwiVG9rZW5UeXBlIjoxLCJpc3MiOiJtaW5pbWF4In0.bNkZV8ocPKShS5gATCWX8P1OrKfkMHK1q8PSBoDYxEBCZsqAhIPj8_7ndN2QEEWjxusGFNHIVBWMj_34P-SSKJ4P-d9Rlsuji7XKZZsja7sJc-zOMRX8lSB_TO7Pn-MErhMID-z7ld7hSihtCeFBuqD_xDwd2g6jIsUFtVlQ8S3SfBHv1PM65Fly9fUAh36BEpEIYhga8E27_x0f26bHBhvMis8WsQthENWXd4lBXu2b5lvrQ64IlPRUBok2dJ4fZViHxnwIcJPRNjxsRW9-EArBowPwFTeTmeAUaPaSv-SdMslJK6jVFb0Y7ULFJUdJAoLJWCYmzphvVGhmbdKVgw
MINIMAX_GROUP_ID=1933510987994895143
MINIMAX_MODEL=speech-02-hd
```

### **Step 3: Restart Service**
1. Click on **"Manual Deploy"** button
2. Select **"Deploy latest commit"**
3. Wait for deployment to complete

---

## **SOLUTION 2: Use Local MiniMax Client** ✅

If the environment variable fix doesn't work, use the local client:

### **Step 1: Set Environment Variables Locally**
```bash
export MINIMAX_API_KEY="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJHcm91cE5hbWUiOiJPRElBIGJhY2tlbmQiLCJVc2VyTmFtZSI6Ik9ESUEgYmFja2VuZCIsIkFjY291bnQiOiIiLCJTdWJqZWN0SUQiOiIxOTMzNTEwOTg4MDAzMjgzNzUxIiwiUGhvbmUiOiIiLCJHcm91cElEIjoiMTkzMzUxMDk4Nzk5NDg5NTE0MyIsIlBhZ2VOYW1lIjoiIiwiTWFpbCI6Im9kaWFiYWNrZW5kQGdtYWlsLmNvbSIsIkNyZWF0ZVRpbWUiOiIyMDI1LTEwLTEyIDA3OjU0OjM2IiwiVG9rZW5UeXBlIjoxLCJpc3MiOiJtaW5pbWF4In0.bNkZV8ocPKShS5gATCWX8P1OrKfkMHK1q8PSBoDYxEBCZsqAhIPj8_7ndN2QEEWjxusGFNHIVBWMj_34P-SSKJ4P-d9Rlsuji7XKZZsja7sJc-zOMRX8lSB_TO7Pn-MErhMID-z7ld7hSihtCeFBuqD_xDwd2g6jIsUFtVlQ8S3SfBHv1PM65Fly9fUAh36BEpEIYhga8E27_x0f26bHBhvMis8WsQthENWXd4lBXu2b5lvrQ64IlPRUBok2dJ4fZViHxnwIcJPRNjxsRW9-EArBowPwFTeTmeAUaPaSv-SdMslJK6jVFb0Y7ULFJUdJAoLJWCYmzphvVGhmbdKVgw"
export MINIMAX_GROUP_ID="1933510987994895143"
```

### **Step 2: Run Local Generation**
```bash
python3 generate_callwaiting_local.py
```

---

## **SOLUTION 3: Direct API Testing** ✅

Test the service directly with curl:

### **Step 1: Test Health**
```bash
curl https://minimax-tts-odiadev.onrender.com/health
```

### **Step 2: Test Voices (if auth disabled)**
```bash
curl https://minimax-tts-odiadev.onrender.com/v1/voices
```

### **Step 3: Test TTS (if auth disabled)**
```bash
curl -X POST https://minimax-tts-odiadev.onrender.com/v1/tts \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello from ODIADEV AI TTS!",
    "voice_name": "american-male",
    "model": "speech-02-hd"
  }'
```

---

## **CALLWAITING AI DEMO SCRIPT** 🎤

**Ready to generate with Marcus voice:**
```
Imagine waking up to realize every missed call might be costing you $500 or more. 
Callwaiting AI is here to change that. For just $80 each month, this intelligent 
agent answers your calls, books appointments, and sends payment links and updates 
you on whatsapp and email—even while you sleep. Never miss a valuable opportunity 
again. Start now and experience the peace of knowing your business is always moving 
forward, effortlessly handled by Callwaiting AI.
```

**Voice Configuration:**
- **Voice**: Marcus (american-male)
- **Voice ID**: `moss_audio_a59cd561-ab87-11f0-a74c-2a7a0b4baedc`
- **Model**: speech-02-hd
- **Speed**: 1.0
- **Pitch**: 0
- **Emotion**: neutral

---

## **VERIFIED VOICE IDs** 🎯

### **American Voices**
- **american-female**: `moss_audio_fdad4786-ab84-11f0-a816-023f15327f7a`
- **american-male**: `moss_audio_a59cd561-ab87-11f0-a74c-2a7a0b4baedc`

### **Nigerian Voices**
- **nigerian-female**: `moss_audio_141d8c4c-a6f8-11f0-84c1-0ec6fa858d82`
- **nigerian-male**: `moss_audio_4e6eb029-ab89-11f0-a74c-2a7a0b4baedc`

---

## **NEXT STEPS** 🚀

1. **Try Solution 1** - Fix environment variables in Render
2. **Try Solution 2** - Use local MiniMax client
3. **Try Solution 3** - Direct API testing
4. **Generate CallWaiting AI demo** with Marcus voice
5. **Test all 4 voices** for production use

**Your ODIADEV AI TTS service is ready - just needs proper authentication setup! 🎉**
