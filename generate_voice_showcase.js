import axios from 'axios';
import fs from 'fs/promises';
import { execFile } from 'child_process';
import { promisify } from 'util';

const execFileAsync = promisify(execFile);

const API_KEY = process.env.MINIMAX_API_KEY || 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJHcm91cE5hbWUiOiJPRElBIGJhY2tlbmQiLCJVc2VyTmFtZSI6Ik9ESUEgYmFja2VuZCIsIkFjY291bnQiOiIiLCJTdWJqZWN0SUQiOiIxOTMzNTEwOTg4MDAzMjgzNzUxIiwiUGhvbmUiOiIiLCJHcm91cElEIjoiMTkzMzUxMDk4Nzk5NDg5NTE0MyIsIlBhZ2VOYW1lIjoiIiwiTWFpbCI6Im9kaWFiYWNrZW5kQGdtYWlsLmNvbSIsIkNyZWF0ZVRpbWUiOiIyMDI1LTEwLTEyIDA3OjU0OjM2IiwiVG9rZW5UeXBlIjoxLCJpc3MiOiJtaW5pbWF4In0.bNkZV8ocPKShS5gATCWX8P1OrKfkMHK1q8PSBoDYxEBCZsqAhIPj8_7ndN2QEEWjxusGFNHIVBWMj_34P-SSKJ4P-d9Rlsuji7XKZZsja7sJc-zOMRX8lSB_TO7Pn-MErhMID-z7ld7hSihtCeFBuqD_xDwd2g6jIsUFtVlQ8S3SfBHv1PM65Fly9fUAh36BEpEIYhga8E27_x0f26bHBhvMis8WsQthENWXd4lBXu2b5lvrQ64IlPRUBok2dJ4fZViHxnwIcJPRNjxsRW9-EArBowPwFTeTmeAUaPaSv-SdMslJK6jVFb0Y7ULFJUdJAoLJWCYmzphvVGhmbdKVgw';
const GROUP_ID = process.env.MINIMAX_GROUP_ID || '1933510987994895143';
const MODEL = process.env.MINIMAX_MODEL || 'speech-02-hd';

// Only verified voice IDs with confirmed characteristics
const VERIFIED_VOICES = [
  {
    name: 'American Female - Professional',
    voiceId: 'moss_audio_fdad4786-ab84-11f0-a816-023f15327f7a',
    characteristics: 'American Female, Neutral',
    text: 'Welcome to our voice showcase! I am an American female voice with a professional, neutral tone. I excel at business communications, customer service, and educational content. My clear pronunciation and warm yet authoritative delivery make me perfect for presentations, training materials, and professional announcements.',
    speed: 1.0,
    pitch: 0,
    emotion: 'neutral'
  },
  {
    name: 'Marcus - American Male - Authoritative',
    voiceId: 'moss_audio_a59cd561-ab87-11f0-a74c-2a7a0b4baedc',
    characteristics: 'American Male, Neutral',
    text: 'Hello there! I am Marcus, an American male voice with a confident, neutral tone. I bring clarity and authority to every word I speak, making me ideal for corporate communications, technical documentation, and leadership presentations. My voice is professional yet approachable, perfect for training, announcements, and executive content.',
    speed: 1.0,
    pitch: 0,
    emotion: 'neutral'
  },
  {
    name: 'Ezinne - Nigerian Female - Professional',
    voiceId: 'moss_audio_141d8c4c-a6f8-11f0-84c1-0ec6fa858d82',
    characteristics: 'Nigerian Female, Neutral',
    text: 'Hello! I am Ezinne, a Nigerian female voice with a neutral, professional tone. I bring the warmth and authenticity of Nigerian culture to every word I speak. My clear pronunciation and confident delivery make me perfect for business communications, educational content, and professional presentations in Nigeria and beyond.',
    speed: 1.0,
    pitch: 0,
    emotion: 'neutral'
  },
  {
    name: 'Odia - Nigerian Male - Authoritative',
    voiceId: 'moss_audio_4e6eb029-ab89-11f0-a74c-2a7a0b4baedc',
    characteristics: 'Nigerian Male, Neutral',
    text: 'Greetings! I am Odia, a Nigerian male voice with a strong, authoritative tone. I represent the strength and confidence of Nigerian men in business and leadership. My clear Nigerian accent and professional delivery make me ideal for corporate communications, technical documentation, and executive presentations across Africa and internationally.',
    speed: 1.0,
    pitch: 0,
    emotion: 'neutral'
  },
  {
    name: 'American Female - Warm & Friendly',
    voiceId: 'moss_audio_fdad4786-ab84-11f0-a816-023f15327f7a',
    characteristics: 'American Female, Neutral',
    text: 'Hi everyone! I am the same American female voice, but now speaking with a warmer, more friendly tone. Notice how I can adapt my delivery while maintaining my professional quality. I am perfect for customer service, hospitality, and any situation where you need a welcoming, approachable voice.',
    speed: 1.1,
    pitch: 1,
    emotion: 'neutral'
  },
  {
    name: 'Marcus - American Male - Technical',
    voiceId: 'moss_audio_a59cd561-ab87-11f0-a74c-2a7a0b4baedc',
    characteristics: 'American Male, Neutral',
    text: 'Technical documentation requires precision and clarity. I am Marcus, delivering complex information with accuracy and professionalism. My neutral American accent ensures universal understanding, while my authoritative tone commands attention. Perfect for software tutorials, technical training, and professional documentation.',
    speed: 0.9,
    pitch: -1,
    emotion: 'neutral'
  },
  {
    name: 'Ezinne - Nigerian Female - Conversational',
    voiceId: 'moss_audio_141d8c4c-a6f8-11f0-84c1-0ec6fa858d82',
    characteristics: 'Nigerian Female, Neutral',
    text: 'Hey there! I am Ezinne, the same Nigerian female voice, but now speaking in a more conversational style. I can adapt to different contexts while maintaining my professional quality. Whether it is business meetings, casual presentations, or friendly announcements, I bring the right tone for every situation.',
    speed: 1.2,
    pitch: 0,
    emotion: 'neutral'
  },
  {
    name: 'Odia - Nigerian Male - Narrative',
    voiceId: 'moss_audio_4e6eb029-ab89-11f0-a74c-2a7a0b4baedc',
    characteristics: 'Nigerian Male, Neutral',
    text: 'Storytelling requires a voice that can capture attention and maintain engagement. I am Odia, bringing depth and character to every narrative. My Nigerian accent provides authenticity, while my neutral tone ensures universal appeal. Perfect for audiobooks, documentaries, and any content that needs a compelling narrator.',
    speed: 0.8,
    pitch: 0,
    emotion: 'neutral'
  }
];

const OUTPUT_DIR = 'voice_showcase';

async function generateVoiceSample(voiceId, text, settings = {}) {
  try {
    const response = await axios.post(
      `https://api.minimaxi.chat/v1/t2a_v2?GroupId=${GROUP_ID}`,
      {
        text: text,
        model: MODEL,
        voice_setting: {
          voice_id: voiceId,
          speed: settings.speed || 1.0,
          pitch: settings.pitch || 0,
          emotion: settings.emotion || 'neutral',
        },
      },
      {
        headers: {
          Authorization: `Bearer ${API_KEY}`,
          'Content-Type': 'application/json',
        },
      }
    );

    const baseStatus = response.data?.base_resp?.status_code;
    if (baseStatus === 0) {
      const audioHex = response.data?.data?.audio;
      if (audioHex) {
        const audioBuffer = Buffer.from(audioHex, 'hex');
        return { success: true, audioBuffer };
      }
    }
    return { success: false, error: 'No audio data' };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

async function generateVoiceShowcase() {
  console.log('🎯 GENERATING VERIFIED VOICE SHOWCASE');
  console.log('='.repeat(60));
  console.log('Creating showcase with only verified voice characteristics...\n');

  if (!API_KEY || API_KEY.includes('...')) {
    console.error('❌ MiniMax API key is missing. Set MINIMAX_API_KEY in your environment.');
    process.exit(1);
  }

  // Create output directory
  try {
    await fs.mkdir(OUTPUT_DIR, { recursive: true });
  } catch (error) {
    // Directory might already exist
  }

  const generatedFiles = [];
  const showcaseData = [];

  for (let i = 0; i < VERIFIED_VOICES.length; i++) {
    const voice = VERIFIED_VOICES[i];
    const filename = `${OUTPUT_DIR}/voice_${i + 1}_${voice.name.replace(/\s+/g, '_').toLowerCase()}.mp3`;
    
    console.log(`\n🎤 Generating ${voice.name}...`);
    console.log(`- Voice ID: ${voice.voiceId}`);
    console.log(`- Characteristics: ${voice.characteristics}`);
    console.log(`- Speed: ${voice.speed}`);
    console.log(`- Pitch: ${voice.pitch}`);

    const result = await generateVoiceSample(voice.voiceId, voice.text, {
      speed: voice.speed,
      pitch: voice.pitch,
      emotion: voice.emotion
    });

    if (result.success) {
      await fs.writeFile(filename, result.audioBuffer);
      
      console.log(`✅ Generated: ${filename}`);
      console.log(`📁 File size: ${result.audioBuffer.length} bytes`);
      
      generatedFiles.push(filename);
      showcaseData.push({
        name: voice.name,
        voiceId: voice.voiceId,
        characteristics: voice.characteristics,
        filename: filename,
        fileSize: result.audioBuffer.length,
        settings: {
          speed: voice.speed,
          pitch: voice.pitch,
          emotion: voice.emotion
        }
      });
    } else {
      console.log(`❌ Failed: ${result.error}`);
    }
  }

  // Save showcase data
  const showcaseReport = {
    timestamp: new Date().toISOString(),
    totalVoices: VERIFIED_VOICES.length,
    successfulGenerations: generatedFiles.length,
    voices: showcaseData
  };

  await fs.writeFile(`${OUTPUT_DIR}/showcase_report.json`, JSON.stringify(showcaseReport, null, 2));
  
  console.log('\n📋 VOICE SHOWCASE COMPLETE');
  console.log('='.repeat(60));
  console.log(`✅ Generated ${generatedFiles.length} voice samples`);
  console.log(`📁 All files saved in: ${OUTPUT_DIR}/`);
  console.log(`📊 Showcase report: ${OUTPUT_DIR}/showcase_report.json`);
  
  // Start autoplay sequence
  await playVoiceSequence(generatedFiles, showcaseData);
}

async function playVoiceSequence(files, data) {
  console.log('\n🔊 Starting voice showcase playback...');
  console.log('Press Ctrl+C to stop playback at any time.\n');

  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    const voiceData = data[i];
    
    console.log(`🎧 Playing: ${voiceData.name}`);
    console.log(`📁 File: ${file}`);
    console.log(`🎤 Characteristics: ${voiceData.characteristics}`);
    
    try {
      await execFileAsync('afplay', [file]);
      console.log(`✅ Completed: ${voiceData.name}\n`);
      
      // Small pause between voices
      if (i < files.length - 1) {
        console.log('⏸️  Brief pause before next voice...\n');
        await new Promise(resolve => setTimeout(resolve, 2000));
      }
    } catch (error) {
      if (error.code === 'ENOENT') {
        console.warn('⚠️  `afplay` not found. Please play the files manually:');
        files.forEach(f => console.log(`   - ${f}`));
        break;
      } else {
        console.warn(`⚠️  Failed to play ${voiceData.name}: ${error.message}`);
      }
    }
  }

  console.log('🎭 Voice showcase completed!');
  console.log(`📁 All files saved in: ${OUTPUT_DIR}/`);
  
  console.log('\n📊 SHOWCASE SUMMARY:');
  console.log('🇺🇸 American Female: 2 variations (Professional, Warm & Friendly)');
  console.log('🇺🇸 Marcus American Male: 2 variations (Authoritative, Technical)');
  console.log('🇳🇬 Ezinne Nigerian Female: 2 variations (Professional, Conversational)');
  console.log('🇳🇬 Odia Nigerian Male: 2 variations (Authoritative, Narrative)');
  console.log('📈 Total: 8 voice samples showcasing different styles and use cases');
  console.log('✅ All based on verified voice characteristics');
}

// Handle graceful shutdown
process.on('SIGINT', () => {
  console.log('\n\n🛑 Playback interrupted by user.');
  console.log('📁 Generated files are still available in the output directory.');
  process.exit(0);
});

generateVoiceShowcase();
