# MiniMax TTS - Production Voice Showcase

## 🎯 **Production-Ready Voice System**

This project provides a complete voice showcase using **verified voice characteristics** from the MiniMax TTS API. All voices have been tested and confirmed for production use.

---

## **Verified Voices**

### **American Voices**
- **American Female** (`moss_audio_fdad4786-ab84-11f0-a816-023f15327f7a`)
  - Characteristics: American Female, Neutral
  - Use Cases: Business communications, customer service, educational content
  - Variations: Professional, Warm & Friendly

- **Marcus American Male** (`moss_audio_a59cd561-ab87-11f0-a74c-2a7a0b4baedc`)
  - Characteristics: American Male, Neutral
  - Use Cases: Corporate communications, technical documentation, leadership presentations
  - Variations: Authoritative, Technical

### **Nigerian Voices**
- **Ezinne Nigerian Female** (`moss_audio_141d8c4c-a6f8-11f0-84c1-0ec6fa858d82`)
  - Characteristics: Nigerian Female, Neutral
  - Use Cases: Business communications, educational content, professional presentations
  - Variations: Professional, Conversational

- **Odia Nigerian Male** (`moss_audio_4e6eb029-ab89-11f0-a74c-2a7a0b4baedc`)
  - Characteristics: Nigerian Male, Neutral
  - Use Cases: Corporate communications, technical documentation, executive presentations
  - Variations: Authoritative, Narrative

---

## **Quick Start**

### **Installation**
```bash
npm install
```

### **Environment Setup**
```bash
export MINIMAX_API_KEY="your_api_key_here"
export MINIMAX_GROUP_ID="your_group_id_here"
```

### **Generate Voice Showcase**
```bash
npm run showcase
```

### **Generate CallWaiting Demo**
```bash
npm run callwaiting
```

---

## **API Usage**

### **Basic TTS Request**
```javascript
const response = await axios.post(
  `https://api.minimaxi.chat/v1/t2a_v2?GroupId=${GROUP_ID}`,
  {
    text: "Your text here",
    model: "speech-02-hd",
    voice_setting: {
      voice_id: "moss_audio_fdad4786-ab84-11f0-a816-023f15327f7a", // American Female
      speed: 1.0,
      pitch: 0,
      emotion: "neutral",
    },
  },
  {
    headers: {
      Authorization: `Bearer ${API_KEY}`,
      "Content-Type": "application/json",
    },
  }
);
```

### **Voice Selection Guide**
- **Business Communications**: American Female, Marcus American Male
- **Customer Service**: American Female (Warm & Friendly)
- **Technical Documentation**: Marcus American Male (Technical)
- **Nigerian Market**: Ezinne Nigerian Female, Odia Nigerian Male
- **Narrative Content**: Odia Nigerian Male (Narrative)
- **Conversational**: Ezinne Nigerian Female (Conversational)

---

## **Production Deployment**

### **Render Deployment**
1. Connect your GitHub repository to Render
2. Set environment variables:
   - `MINIMAX_API_KEY`
   - `MINIMAX_GROUP_ID`
3. Deploy automatically on push

### **Docker Deployment**
```bash
docker build -t minimax-tts .
docker run -p 10000:10000 -e MINIMAX_API_KEY=your_key minimax-tts
```

---

## **File Structure**

```
├── src/                    # Python FastAPI backend
│   ├── main.py            # Main application
│   ├── models.py          # Database models
│   ├── schemas.py         # Pydantic schemas
│   └── minimax_client.py  # MiniMax API client
├── generate_voice_showcase.js  # Voice showcase generator
├── generate_callwaiting_audio.js  # CallWaiting demo
├── package.json           # Node.js dependencies
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
└── render.yaml           # Render deployment config
```

---

## **Voice Characteristics**

All voices have been verified with the following characteristics:
- **Gender**: Clearly identifiable male/female voices
- **Accent**: American and Nigerian accents confirmed
- **Tone**: Professional, neutral delivery
- **Clarity**: Excellent pronunciation and enunciation
- **Speed**: Configurable (0.5x to 2.0x)
- **Pitch**: Configurable (-5 to +5)
- **Emotion**: Neutral (other emotions may be available)

---

## **Best Practices**

1. **Use verified voice IDs only** - Don't guess or assume characteristics
2. **Test with your content** - Verify quality with your specific text
3. **Optimize settings** - Adjust speed and pitch for your use case
4. **Monitor quality** - Listen to generated samples before production use
5. **Keep backups** - Save generated audio files for reference

---

## **Support**

For issues or questions:
1. Check the generated voice samples for quality
2. Verify your API credentials are correct
3. Test with different voice settings
4. Review the showcase report for detailed information

---

## **License**

This project is for production use with verified voice characteristics. All voice IDs have been tested and confirmed for quality and accuracy.

**Ready for production deployment.**
