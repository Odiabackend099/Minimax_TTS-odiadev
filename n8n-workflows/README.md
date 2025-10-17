# n8n Workflow Templates for Minimax TTS

Complete collection of ready-to-use n8n workflows for integrating Minimax TTS into your automation pipelines.

## 📦 Available Workflows

### 1. Basic Webhook (`1-basic-minimax-tts-webhook.json`)
**Purpose:** Simple HTTP webhook endpoint that converts text to speech.

**Use case:**
- Direct API integration
- Simple text-to-speech service
- Testing and development

**Test it:**
```bash
curl -X POST https://your-n8n.app/webhook/minimax-tts \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello from Minimax TTS!",
    "voiceId": "male-qn-qingse",
    "speed": 1.0,
    "emotion": "neutral"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Audio generated successfully",
  "audio_base64": "...",
  "format": "mp3",
  "mimeType": "audio/mpeg"
}
```

---

### 2. WhatsApp Voice Bot (`2-whatsapp-voice-bot.json`)
**Purpose:** Converts WhatsApp text messages to voice notes automatically.

**Use case:**
- WhatsApp automation bots
- Voice message replies
- Accessibility features

**Features:**
- Auto-detects text messages
- Regional voice selection based on phone number
- Sends audio back as WhatsApp voice note

**Setup:**
1. Connect WhatsApp Business API or use WhatsApp node
2. Set environment variables for Minimax credentials
3. Deploy workflow

---

### 3. Telegram /speak Bot (`3-telegram-speak-bot.json`)
**Purpose:** Telegram bot with `/speak` commands to generate voice messages.

**Use case:**
- Telegram chatbots
- Language learning bots
- Voice message generation

**Commands:**
- `/speak <text>` - Generate with default voice
- `/speak_cn <text>` - Chinese voice
- `/speak_en <text>` - English voice
- `/speak_female <text>` - Female voice

**Example:**
```
/speak Hello, this is a test message!
```

Bot replies with voice message 🎙️

---

### 4. Batch CSV Processing (`4-batch-csv-processing.json`)
**Purpose:** Generate multiple audio files from CSV data in batches.

**Use case:**
- Bulk audio generation
- Content creation pipelines
- Voice-over production

**CSV Format:**
```csv
text,voiceId,filename
"Hello world",male-qn-qingse,hello.mp3
"Welcome message",female-shaonv,welcome.mp3
"Thank you for listening",male-qn-qingse,thanks.mp3
```

**Test it:**
```bash
curl -X POST https://your-n8n.app/webhook/batch-tts \
  -H "Content-Type: application/json" \
  -d '{
    "csv": "text,voiceId,filename\n\"Hello\",male-qn-qingse,hello.mp3\n\"Welcome\",female-shaonv,welcome.mp3"
  }'
```

**Features:**
- Processes in batches of 3 (configurable)
- Returns all audio files as base64
- Error handling for individual items

---

### 5. API Gateway with Authentication (`5-api-gateway-with-auth.json`)
**Purpose:** Add your own authentication and rate limiting layer via n8n.

**Use case:**
- Reselling TTS services
- Custom billing/quota management
- Multi-tenant applications

**Features:**
- Custom API key validation
- Per-customer quotas
- Usage tracking and logging
- Rate limiting

**Customer Keys:**
```javascript
'customer_key_001': { plan: 'basic', monthlyQuota: 10000 }
'customer_key_002': { plan: 'pro', monthlyQuota: 50000 }
'test_key': { plan: 'free', monthlyQuota: 100 }
```

**Test it:**
```bash
curl -X POST https://your-n8n.app/webhook/api/v1/tts \
  -H "Authorization: Bearer test_key" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello world",
    "voiceId": "male-qn-qingse"
  }'
```

---

## 🚀 Quick Setup

### Step 1: Import Workflow to n8n

1. Open your n8n instance
2. Click **Workflows** → **Import from File**
3. Select one of the JSON files
4. Click **Import**

### Step 2: Set Environment Variables

Set these in n8n Settings → Variables:

```bash
MINIMAX_API_KEY=your-minimax-api-key
MINIMAX_GROUP_ID=your-minimax-group-id
```

**How to get credentials:**
1. Sign up at [Minimax Platform](https://platform.minimaxi.com/)
2. Go to API Keys section
3. Copy your API Key and Group ID

### Step 3: Configure Credentials (for WhatsApp/Telegram)

For workflows using WhatsApp or Telegram:

1. **WhatsApp:**
   - n8n → Credentials → **WhatsApp API**
   - Add your WhatsApp Business API credentials

2. **Telegram:**
   - Create bot with [@BotFather](https://t.me/botfather)
   - Get bot token
   - n8n → Credentials → **Telegram API**

### Step 4: Activate Workflow

1. Click **Activate** toggle in top right
2. Get your webhook URL from the Webhook node
3. Test with curl or Postman

---

## 🎯 Minimax Voice IDs

Available voices (add more from Minimax docs):

| Voice ID | Language | Gender | Description |
|----------|----------|--------|-------------|
| `male-qn-qingse` | Chinese | Male | Clear, natural |
| `female-shaonv` | Chinese | Female | Young, friendly |
| `male-qn-jingying` | Chinese | Male | Professional |
| `female-tianmei` | Chinese | Female | Sweet, gentle |

**Note:** Minimax supports 30+ languages. Check their [voice library](https://platform.minimaxi.com/document/T2A%20V2?key=66719005a427f0c8a5701643) for full list.

---

## 🛠️ Customization Tips

### Adjust Voice Speed
```javascript
"speed": 1.2  // 0.5 to 2.0 (slower to faster)
```

### Change Emotion
```javascript
"emotion": "happy"  // Options: neutral, happy, sad, angry, etc.
```

### Batch Size (for CSV processing)
In "Split In Batches" node:
```json
"batchSize": 5  // Process 5 items at a time
```

### Add Error Notifications
Add an IF node after HTTP requests:
- **Success:** Continue to next node
- **Error:** Send notification (Slack, email, etc.)

---

## 📊 Monitoring & Logs

### View Execution Logs
1. n8n → Executions
2. Click any execution to see detailed logs
3. Check each node's input/output

### Track Usage
Workflow 5 (API Gateway) includes usage logging:
```javascript
{
  customer: "Customer One",
  duration_seconds: 45,
  timestamp: "2025-01-14T12:00:00Z"
}
```

Store in:
- Google Sheets
- Database (PostgreSQL, MySQL)
- Analytics platform

---

## 🔧 Troubleshooting

### Issue: "Invalid API key"
**Solution:** Check environment variables are set correctly in n8n Settings → Variables

### Issue: "Insufficient balance" (Minimax error 1008)
**Solution:** Add credits at [Minimax Platform](https://platform.minimaxi.com/)

### Issue: Webhook not receiving requests
**Solution:**
1. Check webhook is activated
2. Verify webhook URL is correct
3. Test with curl first

### Issue: Audio not playing
**Solution:**
- Check MIME type is `audio/mpeg`
- Verify base64 encoding is correct
- Try downloading and playing locally

---

## 📚 Additional Resources

- **Minimax API Docs:** [https://platform.minimaxi.com/document](https://platform.minimaxi.com/document)
- **n8n Documentation:** [https://docs.n8n.io/](https://docs.n8n.io/)
- **n8n Community:** [https://community.n8n.io/](https://community.n8n.io/)
- **Full Integration Guide:** See [N8N_INTEGRATION.md](../N8N_INTEGRATION.md)

---

## 🤝 Contributing

Have a cool workflow idea? Submit a PR with:
1. New workflow JSON file
2. Description in this README
3. Test instructions

---

## ⚡ Quick Links

- [Minimax TTS Server](../minimax_tts.js) - Local server running on port 3000
- [Test Scripts](../test.js) - Test your Minimax integration
- [Package Info](../package.json) - Project dependencies

---

**🎉 You're all set! Start automating with Minimax TTS + n8n!**

Need help? Open an issue or check the docs linked above.
