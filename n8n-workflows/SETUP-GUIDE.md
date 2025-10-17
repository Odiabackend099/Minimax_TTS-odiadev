# 🚀 n8n + Minimax TTS Setup Guide

Complete step-by-step guide to set up your Minimax TTS workflows in n8n.

## 📋 Your Credentials

```bash
API_KEY: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJHcm91cE5hbWUiOiJPRElBIGJhY2tlbmQiLCJVc2VyTmFtZSI6Ik9ESUEgYmFja2VuZCIsIkFjY291bnQiOiIiLCJTdWJqZWN0SUQiOiIxOTMzNTEwOTg4MDAzMjgzNzUxIiwiUGhvbmUiOiIiLCJHcm91cElEIjoiMTkzMzUxMDk4Nzk5NDg5NTE0MyIsIlBhZ2VOYW1lIjoiIiwiTWFpbCI6Im9kaWFiYWNrZW5kQGdtYWlsLmNvbSIsIkNyZWF0ZVRpbWUiOiIyMDI1LTEwLTEyIDA3OjU0OjM2IiwiVG9rZW5UeXBlIjoxLCJpc3MiOiJtaW5pbWF4In0.bNkZV8ocPKShS5gATCWX8P1OrKfkMHK1q8PSBoDYxEBCZsqAhIPj8_7ndN2QEEWjxusGFNHIVBWMj_34P-SSKJ4P-d9Rlsuji7XKZZsja7sJc-zOMRX8lSB_TO7Pn-MErhMID-z7ld7hSihtCeFBuqD_xDwd2g6jIsUFtVlQ8S3SfBHv1PM65Fly9fUAh36BEpEIYhga8E27_x0f26bHBhvMis8WsQthENWXd4lBXu2b5lvrQ64IlPRUBok2dJ4fZViHxnwIcJPRNjxsRW9-EArBowPwFTeTmeAUaPaSv-SdMslJK6jVFb0Y7ULFJUdJAoLJWCYmzphvVGhmbdKVgw

GROUP_ID: 1933510987994895143

VOICE_ID: moss_audio_141d8c4c-a6f8-11f0-84c1-0ec6fa858d82
```

## ⚡ Quick Setup (5 Minutes)

### Step 1: Set Environment Variables in n8n

1. Open n8n
2. Go to **Settings** → **Environments**
3. Add these variables:

```bash
MINIMAX_API_KEY=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJHcm91cE5hbWUiOiJPRElBIGJhY2tlbmQiLCJVc2VyTmFtZSI6Ik9ESUEgYmFja2VuZCIsIkFjY291bnQiOiIiLCJTdWJqZWN0SUQiOiIxOTMzNTEwOTg4MDAzMjgzNzUxIiwiUGhvbmUiOiIiLCJHcm91cElEIjoiMTkzMzUxMDk4Nzk5NDg5NTE0MyIsIlBhZ2VOYW1lIjoiIiwiTWFpbCI6Im9kaWFiYWNrZW5kQGdtYWlsLmNvbSIsIkNyZWF0ZVRpbWUiOiIyMDI1LTEwLTEyIDA3OjU0OjM2IiwiVG9rZW5UeXBlIjoxLCJpc3MiOiJtaW5pbWF4In0.bNkZV8ocPKShS5gATCWX8P1OrKfkMHK1q8PSBoDYxEBCZsqAhIPj8_7ndN2QEEWjxusGFNHIVBWMj_34P-SSKJ4P-d9Rlsuji7XKZZsja7sJc-zOMRX8lSB_TO7Pn-MErhMID-z7ld7hSihtCeFBuqD_xDwd2g6jIsUFtVlQ8S3SfBHv1PM65Fly9fUAh36BEpEIYhga8E27_x0f26bHBhvMis8WsQthENWXd4lBXu2b5lvrQ64IlPRUBok2dJ4fZViHxnwIcJPRNjxsRW9-EArBowPwFTeTmeAUaPaSv-SdMslJK6jVFb0Y7ULFJUdJAoLJWCYmzphvVGhmbdKVgw

MINIMAX_GROUP_ID=1933510987994895143
```

### Step 2: Import Workflow

1. Download: `PRODUCTION-minimax-tts-complete.json`
2. In n8n: **Workflows** → **Import from File**
3. Select the JSON file
4. Click **Import**

### Step 3: Activate Workflow

1. Click **Activate** toggle (top right)
2. Copy the webhook URL from the Webhook node
3. Test it!

---

## 🧪 Test Your Workflow

### Test 1: Simple Text-to-Speech

```bash
curl -X POST https://your-n8n-instance.com/webhook/minimax-tts \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, this is a test of Minimax TTS!"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Audio generated successfully with Minimax TTS",
  "audio_base64": "//uQx...",
  "format": "mp3",
  "mimeType": "audio/mpeg",
  "duration_ms": 2500,
  "voice_id": "moss_audio_141d8c4c-a6f8-11f0-84c1-0ec6fa858d82",
  "timestamp": "2025-01-14T12:00:00.000Z"
}
```

### Test 2: Custom Voice Settings

```bash
curl -X POST https://your-n8n-instance.com/webhook/minimax-tts \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Testing with custom voice settings",
    "voiceId": "moss_audio_141d8c4c-a6f8-11f0-84c1-0ec6fa858d82",
    "speed": 1.2,
    "pitch": 0,
    "emotion": "happy",
    "model": "speech-02-hd"
  }'
```

### Test 3: Play Audio (Browser)

Save this as `test.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Minimax TTS Test</title>
</head>
<body>
    <h1>Minimax TTS Tester</h1>

    <textarea id="text" rows="4" cols="50">Hello, this is a test!</textarea><br>
    <button onclick="generateAudio()">Generate Audio</button>

    <div id="result"></div>
    <audio id="audioPlayer" controls style="display:none;"></audio>

    <script>
        async function generateAudio() {
            const text = document.getElementById('text').value;

            const response = await fetch('https://your-n8n-instance.com/webhook/minimax-tts', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text })
            });

            const data = await response.json();

            if (data.success) {
                const audio = document.getElementById('audioPlayer');
                audio.src = 'data:audio/mpeg;base64,' + data.audio_base64;
                audio.style.display = 'block';
                audio.play();

                document.getElementById('result').innerHTML =
                    `<p style="color: green;">✓ Success! Duration: ${data.duration_ms}ms</p>`;
            } else {
                document.getElementById('result').innerHTML =
                    `<p style="color: red;">✗ Error: ${data.error}</p>`;
            }
        }
    </script>
</body>
</html>
```

---

## 🎯 Available Workflows

### 1. Production Complete Workflow ⭐ **RECOMMENDED**
**File:** `PRODUCTION-minimax-tts-complete.json`

**Features:**
- ✅ Direct Minimax API integration
- ✅ Proper error handling
- ✅ Hex to Base64 conversion
- ✅ Environment variable support
- ✅ Detailed response metadata

**Use:** Import this first!

---

### 2. Basic Webhook
**File:** `1-basic-minimax-tts-webhook.json`

Simple webhook that proxies through your local server.

---

### 3. WhatsApp Voice Bot
**File:** `2-whatsapp-voice-bot.json`

Converts WhatsApp messages to voice notes.

---

### 4. Telegram Bot
**File:** `3-telegram-speak-bot.json`

`/speak` command for Telegram.

---

### 5. Batch CSV Processing
**File:** `4-batch-csv-processing.json`

Generate multiple audio files from CSV.

---

### 6. API Gateway
**File:** `5-api-gateway-with-auth.json`

Add custom authentication layer.

---

## 🔧 Common Issues & Solutions

### Issue 1: "Environment variable not found"

**Solution:**
Make sure you added the variables in n8n Settings → Environments:
- `MINIMAX_API_KEY`
- `MINIMAX_GROUP_ID`

### Issue 2: "Status code 1008: Insufficient balance"

**Solution:**
Add credits at: https://platform.minimaxi.com/user_center/basic_info/interface_account

### Issue 3: "No audio data in response"

**Solution:**
Check the Minimax API response in n8n execution logs. The audio should be in hex format.

### Issue 4: Webhook not accessible

**Solution:**
- Check workflow is **activated**
- Verify webhook URL is correct
- Test locally first if using n8n desktop

---

## 📊 Monitoring

### View Execution History
1. n8n → **Executions**
2. Click any execution
3. See input/output for each node

### Check API Usage
Visit Minimax dashboard:
https://platform.minimaxi.com/user_center/basic_info

---

## 🎨 Voice Customization

### Available Parameters

```json
{
  "text": "Your text here",           // Required
  "voiceId": "moss_audio_...",      // Optional (uses default)
  "model": "speech-02-hd",           // Optional (default: speech-02-hd)
  "speed": 1.0,                      // Optional (0.5 - 2.0)
  "pitch": 0,                        // Optional (-12 to 12)
  "emotion": "neutral"               // Optional (neutral, happy, sad, etc.)
}
```

### Available Models
- `speech-01`: Standard quality
- `speech-02`: High quality
- `speech-02-hd`: Highest quality (recommended)

### Emotions
- `neutral` (default)
- `happy`
- `sad`
- `angry`
- `fearful`
- `disgusted`
- `surprised`

---

## 💡 Pro Tips

### 1. Save Audio Files
Add a "Write Binary File" node after "Process Audio Response":
```
File Path: /tmp/audio_{{ $json.timestamp }}.mp3
Binary Property: data
```

### 2. Add Webhook Authentication
Before "Set Environment Variables", add an IF node:
```javascript
{{ $json.headers.authorization === 'Bearer your-secret-key' }}
```

### 3. Rate Limiting
Add a "Rate Limit" node to prevent abuse:
```
Limit: 10 requests per minute
```

### 4. Logging to Database
Add a "Postgres/MySQL" node after success:
```sql
INSERT INTO tts_logs (text, duration_ms, timestamp)
VALUES ($1, $2, $3)
```

---

## 🔗 Useful Links

- **Minimax Platform:** https://platform.minimaxi.com/
- **Minimax API Docs:** https://platform.minimaxi.com/document/T2A%20V2
- **n8n Documentation:** https://docs.n8n.io/
- **Voice Library:** https://platform.minimaxi.com/document/T2A%20V2?key=66719005a427f0c8a5701643

---

## 📞 Support

**API Issues:**
- Check Minimax status: https://platform.minimaxi.com/
- Contact: support@minimaxi.com

**n8n Issues:**
- Community: https://community.n8n.io/
- Discord: https://discord.gg/n8n

---

## 🎉 You're All Set!

Your Minimax TTS integration is ready to use. Start building awesome voice automation workflows!

**Next Steps:**
1. ✅ Import the production workflow
2. ✅ Set environment variables
3. ✅ Test with the curl command
4. ✅ Integrate into your applications
5. 🚀 Build something amazing!

---

**Need help?** Check the README.md in this folder or the main N8N_INTEGRATION.md guide.
