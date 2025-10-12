# 🔗 n8n Integration Guide for OdeaDev-AI-TTS

Complete guide for integrating your TTS service with n8n workflows.

---

## 🚀 Quick Start: Basic TTS Workflow

### Workflow 1: Simple Text-to-Speech Webhook

**Use case:** Send text via webhook, get audio back

```
[Webhook] → [HTTP Request: TTS API] → [Respond with Audio]
```

**n8n Configuration:**

1. **Webhook Node**
   - Method: POST
   - Path: `tts-webhook`
   - Response: `Respond Using 'Respond to Webhook' Node`

2. **HTTP Request Node** (TTS API)
   ```json
   {
     "method": "POST",
     "url": "https://odeadev-ai-tts.onrender.com/v1/tts",
     "authentication": "predefinedCredentialType",
     "nodeCredentialType": "httpHeaderAuth",
     "sendHeaders": true,
     "headerParameters": {
       "parameters": [
         {
           "name": "Authorization",
           "value": "Bearer YOUR_API_KEY_HERE"
         }
       ]
     },
     "sendBody": true,
     "bodyParameters": {
       "parameters": [
         {
           "name": "text",
           "value": "={{ $json.body.text }}"
         },
         {
           "name": "voice_name",
           "value": "={{ $json.body.voice || 'nigerian-male' }}"
         }
       ]
     },
     "options": {
       "response": {
         "response": {
           "responseFormat": "json"
         }
       }
     }
   }
   ```

3. **Respond to Webhook Node**
   ```json
   {
     "respondWith": "json",
     "responseBody": "={{ $json }}"
   }
   ```

**Test it:**
```bash
curl -X POST https://your-n8n.app/webhook/tts-webhook \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello from n8n!",
    "voice": "nigerian-male"
  }'
```

---

## 📱 WhatsApp Integration

### Workflow 2: WhatsApp Message → TTS → Voice Note

**Use case:** User sends text to WhatsApp bot, receives voice message

```
[WhatsApp Trigger] → [Extract Text] → [TTS API] → [Base64 to Binary] → [Send WhatsApp Audio]
```

**Step-by-step:**

#### 1. WhatsApp Trigger Node
```json
{
  "trigger": "On Message Received",
  "filter": {
    "messageType": "text"
  }
}
```

#### 2. Function Node: Extract Message
```javascript
// Get message text
const text = $input.item.json.message.text;
const from = $input.item.json.message.from;

return {
  json: {
    text: text,
    phone: from,
    timestamp: new Date().toISOString()
  }
};
```

#### 3. HTTP Request Node: Call TTS
```json
{
  "method": "POST",
  "url": "https://odeadev-ai-tts.onrender.com/v1/tts",
  "authentication": "headerAuth",
  "sendBody": true,
  "jsonParameters": true,
  "body": {
    "text": "={{ $json.text }}",
    "voice_name": "nigerian-male",
    "speed": 1.0,
    "emotion": "neutral"
  },
  "options": {}
}
```

#### 4. Code Node: Convert Base64 to Binary
```javascript
const audioBase64 = $input.item.json.audio_base64;
const audioBuffer = Buffer.from(audioBase64, 'base64');

return {
  json: {},
  binary: {
    data: {
      data: audioBuffer.toString('base64'),
      mimeType: 'audio/mpeg',
      fileName: 'voice_message.mp3'
    }
  }
};
```

#### 5. WhatsApp Node: Send Audio
```json
{
  "operation": "sendAudio",
  "chatId": "={{ $('WhatsApp Trigger').item.json.message.from }}",
  "binaryProperty": "data",
  "caption": "🎙️ Here's your voice message!"
}
```

**Advanced: Voice Selection by Country**

Add after "Extract Message" node:

```javascript
// Auto-select voice based on user's country code
const phone = $json.phone;
let voice = "nigerian-male";

if (phone.startsWith("+234")) {
  voice = "nigerian-male";
} else if (phone.startsWith("+44")) {
  voice = "british-female";
} else if (phone.startsWith("+1")) {
  voice = "american-male";
}

return {
  json: {
    ...$json,
    voice_name: voice
  }
};
```

---

## 💬 Telegram Bot Integration

### Workflow 3: Telegram Bot with Voice Commands

**Use case:** `/speak <text>` command generates voice message

```
[Telegram Trigger] → [Check Command] → [TTS API] → [Send Voice]
```

#### 1. Telegram Trigger
```json
{
  "updates": ["message"],
  "filters": {
    "text": {
      "startsWith": "/speak"
    }
  }
}
```

#### 2. Function: Parse Command
```javascript
const message = $input.item.json.message.text;
const text = message.replace(/^\/speak\s*/i, '');
const chatId = $input.item.json.message.chat.id;
const userId = $input.item.json.message.from.id;

if (!text || text.length === 0) {
  return {
    json: {
      error: true,
      message: "Please provide text: /speak Hello world"
    }
  };
}

return {
  json: {
    text: text,
    chatId: chatId,
    userId: userId
  }
};
```

#### 3. IF Node: Check for Error
- Condition: `{{ $json.error }} is false`

#### 4. HTTP Request: TTS API
```json
{
  "url": "https://odeadev-ai-tts.onrender.com/v1/tts",
  "method": "POST",
  "body": {
    "text": "={{ $json.text }}",
    "voice_name": "american-male"
  }
}
```

#### 5. Code: Convert Audio
```javascript
const audio = Buffer.from($json.audio_base64, 'base64');
return {
  binary: {
    voice: {
      data: audio.toString('base64'),
      mimeType: 'audio/mpeg',
      fileName: 'tts_output.mp3'
    }
  }
};
```

#### 6. Telegram: Send Voice
```json
{
  "operation": "sendVoice",
  "chatId": "={{ $('Function').item.json.chatId }}",
  "binaryProperty": "voice"
}
```

**Bonus: Multi-voice Support**

Add voice selection:
```
/speak_ng Hello (Nigerian voice)
/speak_us Hello (American voice)
/speak_uk Hello (British voice)
```

Parse in Function node:
```javascript
const message = $input.item.json.message.text;
let voice = "nigerian-male";
let text = "";

if (message.startsWith("/speak_ng")) {
  voice = "nigerian-male";
  text = message.replace(/^\/speak_ng\s*/i, '');
} else if (message.startsWith("/speak_us")) {
  voice = "american-male";
  text = message.replace(/^\/speak_us\s*/i, '');
} else if (message.startsWith("/speak_uk")) {
  voice = "british-female";
  text = message.replace(/^\/speak_uk\s*/i, '');
} else {
  text = message.replace(/^\/speak\s*/i, '');
}

return {
  json: { text, voice, chatId: $input.item.json.message.chat.id }
};
```

---

## 📧 Email to Voice Message

### Workflow 4: Email → TTS → Audio Attachment Reply

**Use case:** Send email with text, get audio reply

```
[Email Trigger] → [Extract Body] → [TTS API] → [Email with Audio]
```

#### 1. Email Trigger (IMAP)
```json
{
  "mailbox": "INBOX",
  "format": "simple",
  "download": false,
  "markAsRead": true
}
```

#### 2. Function: Extract Email Body
```javascript
const subject = $json.subject;
const body = $json.textPlain || $json.textHtml;
const from = $json.from.address;

// Clean HTML if needed
const cleanText = body.replace(/<[^>]*>/g, '').trim();

return {
  json: {
    text: cleanText,
    subject: subject,
    from: from
  }
};
```

#### 3. HTTP Request: TTS
Same as previous examples

#### 4. Code: Save Audio to Temp File
```javascript
const audio = Buffer.from($json.audio_base64, 'base64');
const fs = require('fs');
const path = '/tmp/voice_message.mp3';

fs.writeFileSync(path, audio);

return {
  json: {
    audioPath: path,
    from: $('Function').item.json.from,
    subject: $('Function').item.json.subject
  }
};
```

#### 5. Email: Send Reply with Attachment
```json
{
  "operation": "send",
  "to": "={{ $json.from }}",
  "subject": "Re: {{ $json.subject }}",
  "text": "Here's your message as audio!",
  "attachments": "audioPath"
}
```

---

## 🌐 REST API with n8n Proxy

### Workflow 5: n8n as API Gateway with Auth

**Use case:** Add your own authentication layer via n8n

```
[Webhook] → [Validate API Key] → [TTS API] → [Log Usage] → [Response]
```

#### 1. Webhook Node
```json
{
  "path": "api/v1/tts",
  "method": "POST",
  "responseMode": "responseNode"
}
```

#### 2. Function: Validate Custom API Key
```javascript
// Your custom API keys (store in n8n credentials)
const validKeys = {
  "customer1_key": { name: "Customer 1", plan: "basic", quota: 1000 },
  "customer2_key": { name: "Customer 2", plan: "pro", quota: 5000 }
};

const apiKey = $input.item.json.headers.authorization?.replace('Bearer ', '');

if (!apiKey || !validKeys[apiKey]) {
  return {
    json: {
      error: true,
      message: "Invalid API key"
    }
  };
}

const customer = validKeys[apiKey];

return {
  json: {
    valid: true,
    customer: customer,
    text: $input.item.json.body.text,
    voice: $input.item.json.body.voice_name || "nigerian-male"
  }
};
```

#### 3. IF: Check Validation
- True branch: Continue to TTS
- False branch: Return error

#### 4. HTTP Request: Your TTS API
Use your service API key (different from customer keys)

#### 5. Function: Log Usage to Database
```javascript
// Log to your database
const customer = $('Function').item.json.customer;
const duration = $json.duration_seconds;

return {
  json: {
    customer: customer.name,
    duration: duration,
    audio_base64: $json.audio_base64,
    timestamp: new Date().toISOString()
  }
};
```

#### 6. Respond to Webhook
Return the audio response

---

## 🔄 Batch Processing

### Workflow 6: CSV to Multiple Audio Files

**Use case:** Generate audio for multiple texts at once

```
[Webhook/Manual] → [Split CSV] → [For Each Text] → [TTS API] → [Collect Results]
```

#### 1. Webhook: Upload CSV
```json
{
  "path": "batch-tts",
  "responseMode": "responseNode",
  "options": {
    "rawBody": true
  }
}
```

#### 2. Code: Parse CSV
```javascript
const csv = require('csv-parse/sync');
const content = $input.item.json.body;

const records = csv.parse(content, {
  columns: true,
  skip_empty_lines: true
});

return records.map(record => ({
  json: {
    text: record.text,
    voice: record.voice || 'nigerian-male',
    filename: record.filename || `audio_${Date.now()}.mp3`
  }
}));
```

#### 3. Loop Over Items: Split in Batches
Use "Split In Batches" node:
```json
{
  "batchSize": 5,
  "options": {}
}
```

#### 4. HTTP Request: TTS API
Process each item

#### 5. Code: Aggregate Results
```javascript
const items = $input.all();
const results = items.map(item => ({
  filename: item.json.filename,
  audio_url: `data:audio/mp3;base64,${item.json.audio_base64}`,
  duration: item.json.duration_seconds
}));

return {
  json: {
    total: results.length,
    files: results
  }
};
```

---

## 📊 Usage Analytics & Monitoring

### Workflow 7: Track TTS Usage in Google Sheets

```
[Schedule Trigger] → [Get Usage from DB] → [Update Google Sheets]
```

#### 1. Schedule: Daily at 9 AM
```json
{
  "rule": {
    "interval": [{ "field": "cronExpression", "expression": "0 9 * * *" }]
  }
}
```

#### 2. HTTP Request: Get User Stats
```bash
GET https://odeadev-ai-tts.onrender.com/v1/me
Authorization: Bearer YOUR_API_KEY
```

#### 3. Google Sheets: Append Row
```json
{
  "operation": "append",
  "sheetId": "YOUR_SHEET_ID",
  "range": "A:E",
  "values": [
    "={{ $now }}",
    "={{ $json.used_seconds }}",
    "={{ $json.quota_seconds }}",
    "={{ $json.remaining_seconds }}",
    "={{ $json.quota_percentage_used }}"
  ]
}
```

---

## 🎯 Pre-built n8n Workflow Templates

### Template URLs (Import to n8n)

You can create these as JSON exports:

**1. Basic TTS Webhook:**
```json
{
  "name": "OdeaDev TTS - Basic Webhook",
  "nodes": [...]
}
```

**2. WhatsApp Voice Bot:**
```json
{
  "name": "OdeaDev TTS - WhatsApp Bot",
  "nodes": [...]
}
```

Save these as `.json` files and import via:
n8n → Workflows → Import from File

---

## 🔐 Credentials Setup in n8n

### Add HTTP Header Auth Credential

1. n8n → Credentials → **+ Add Credential**
2. Type: **Header Auth**
3. Configuration:
   ```
   Name: Authorization
   Value: Bearer YOUR_ODEADEV_API_KEY
   ```
4. Save as: `OdeaDev TTS API`

### Use in HTTP Request Nodes

```json
{
  "authentication": "predefinedCredentialType",
  "nodeCredentialType": "httpHeaderAuth",
  "credential": "OdeaDev TTS API"
}
```

---

## 🧪 Testing Workflows

### Test Webhook Locally

```bash
# Test n8n webhook
curl -X POST http://localhost:5678/webhook-test/tts \
  -H "Content-Type: application/json" \
  -d '{"text":"Test from local n8n"}'
```

### Test Production Workflow

```bash
curl -X POST https://your-n8n.app/webhook/tts \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Production test",
    "voice": "nigerian-male"
  }'
```

---

## 📚 Additional Resources

- **n8n Docs**: https://docs.n8n.io/
- **n8n Community**: https://community.n8n.io/
- **OdeaDev API Docs**: https://odeadev-ai-tts.onrender.com/docs

---

**🎉 Your n8n integration is ready!**

Start building powerful automation workflows with text-to-speech! 🚀
