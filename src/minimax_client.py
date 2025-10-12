"""MiniMax T2A API client."""
from __future__ import annotations
import os
import base64
from typing import Dict, Any

try:
    import requests
except Exception:
    requests = None


class MinimaxAPIError(Exception):
    """Custom exception for MiniMax API errors."""
    def __init__(self, status_code: int, message: str, details: Any = None):
        self.status_code = status_code
        self.message = message
        self.details = details
        super().__init__(f"MiniMax API Error {status_code}: {message}")


class MinimaxClient:
    """Client for MiniMax Text-to-Audio API."""
    
    def __init__(self, api_key: str = None, group_id: str = None):
        """
        Initialize MiniMax client.
        
        Args:
            api_key: MiniMax API key (JWT token). If not provided, reads from MINIMAX_API_KEY env var.
            group_id: MiniMax Group ID. If not provided, reads from MINIMAX_GROUP_ID env var.
        """
        self.api_key = api_key or os.getenv("MINIMAX_API_KEY")
        self.group_id = group_id or os.getenv("MINIMAX_GROUP_ID")
        
        if not self.api_key:
            raise ValueError("MINIMAX_API_KEY not provided")
        if not self.group_id:
            raise ValueError("MINIMAX_GROUP_ID not provided")
        
        self.base_url = "https://api.minimaxi.chat"
    
    def text_to_speech(
        self,
        text: str,
        voice_id: str,
        model: str = "speech-02-turbo",
        speed: float = 1.0,
        pitch: int = 0,
        emotion: str = "neutral",
        timeout: int = 30
    ) -> Dict[str, Any]:
        """
        Convert text to speech using MiniMax API.
        
        Args:
            text: Text to convert to speech
            voice_id: MiniMax voice ID
            model: Model to use (default: speech-02-turbo)
            speed: Speech speed (0.5-2.0)
            pitch: Voice pitch (-12 to 12)
            emotion: Emotion (neutral, happy, sad, angry, etc.)
            timeout: Request timeout in seconds
            
        Returns:
            dict with keys:
                - audio_data: bytes of MP3 audio
                - audio_base64: base64-encoded audio
                - duration_seconds: estimated duration
                - sample_rate: audio sample rate
                
        Raises:
            MinimaxAPIError: If API request fails
        """
        url = f"{self.base_url}/v1/t2a_v2?GroupId={self.group_id}"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "text": text,
            "model": model,
            "voice_setting": {
                "voice_id": voice_id,
                "speed": speed,
                "pitch": pitch,
                "emotion": emotion,
            },
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=timeout)
            
            # Check HTTP status
            if response.status_code != 200:
                raise MinimaxAPIError(
                    response.status_code,
                    f"HTTP {response.status_code}",
                    response.text
                )
            
            data = response.json()
            
            # Check MiniMax API response status
            base_resp = data.get("base_resp", {})
            status_code = base_resp.get("status_code")
            status_msg = base_resp.get("status_msg", "Unknown error")
            
            if status_code != 0:
                # Map MiniMax error codes to readable messages
                error_messages = {
                    1008: "Insufficient balance in MiniMax account. Please add credits.",
                    2013: "Invalid parameters provided to MiniMax API.",
                    401: "Invalid MiniMax API key or authentication failed.",
                }
                
                readable_msg = error_messages.get(status_code, status_msg)
                raise MinimaxAPIError(status_code, readable_msg, data)
            
            # Extract audio data
            audio_hex = data.get("data", {}).get("audio")
            if not audio_hex:
                raise MinimaxAPIError(500, "No audio data in response", data)
            
            # Decode hex to bytes
            audio_bytes = bytes.fromhex(audio_hex)
            audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
            
            # Estimate duration (rough estimate: ~150 words per minute)
            word_count = len(text.split())
            estimated_duration = (word_count / 150) * 60 / speed
            
            return {
                "audio_data": audio_bytes,
                "audio_base64": audio_base64,
                "duration_seconds": estimated_duration,
                "sample_rate": 32000,  # Default MiniMax sample rate
            }
            
        except requests.exceptions.Timeout:
            raise MinimaxAPIError(408, "Request to MiniMax API timed out")
        except requests.exceptions.ConnectionError:
            raise MinimaxAPIError(503, "Could not connect to MiniMax API")
        except requests.exceptions.RequestException as e:
            raise MinimaxAPIError(500, f"Request failed: {str(e)}")
        except (ValueError, KeyError) as e:
            raise MinimaxAPIError(500, f"Failed to parse MiniMax response: {str(e)}")
