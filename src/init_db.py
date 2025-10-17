"""Database initialization and seeding."""
from __future__ import annotations

from .database import engine
from .models import Base, Voice, Gender


def init_database():
    """Create all database tables."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")


def seed_default_voices(db_session):
    """Seed database with verified ODIADEV TTS voices."""
    default_voices = [
        {
            "friendly_name": "american-female",
            "minimax_voice_id": "moss_audio_fdad4786-ab84-11f0-a816-023f15327f7a",
            "language": "en-US",
            "gender": Gender.FEMALE,
            "description": "American female voice with professional, neutral tone - verified for production use",
            "is_cloned": False,
        },
        {
            "friendly_name": "american-male",
            "minimax_voice_id": "moss_audio_a59cd561-ab87-11f0-a74c-2a7a0b4baedc",
            "language": "en-US",
            "gender": Gender.MALE,
            "description": "Marcus American male voice with confident, neutral tone - verified for production use",
            "is_cloned": False,
        },
        {
            "friendly_name": "nigerian-female",
            "minimax_voice_id": "moss_audio_141d8c4c-a6f8-11f0-84c1-0ec6fa858d82",
            "language": "en-NG",
            "gender": Gender.FEMALE,
            "description": "Ezinne Nigerian female voice with professional, neutral tone - verified for production use",
            "is_cloned": False,
        },
        {
            "friendly_name": "nigerian-male",
            "minimax_voice_id": "moss_audio_4e6eb029-ab89-11f0-a74c-2a7a0b4baedc",
            "language": "en-NG",
            "gender": Gender.MALE,
            "description": "Odia Nigerian male voice with strong, authoritative tone - verified for production use",
            "is_cloned": False,
        },
    ]
    
    print("Seeding default voices...")
    for voice_data in default_voices:
        # Check if voice already exists
        existing = db_session.query(Voice).filter(
            Voice.friendly_name == voice_data["friendly_name"]
        ).first()
        
        if not existing:
            voice = Voice(**voice_data)
            db_session.add(voice)
            print(f"  ✅ Added voice: {voice_data['friendly_name']}")
        else:
            # Update existing voice with new data
            existing.minimax_voice_id = voice_data["minimax_voice_id"]
            existing.language = voice_data["language"]
            existing.gender = voice_data["gender"]
            existing.description = voice_data["description"]
            existing.is_cloned = voice_data["is_cloned"]
            print(f"  🔄 Updated voice: {voice_data['friendly_name']}")
    
    db_session.commit()
    print("✅ Default voices seeded successfully!")


if __name__ == "__main__":
    from .database import SessionLocal
    
    # Initialize tables
    init_database()
    
    # Seed default voices
    db = SessionLocal()
    try:
        seed_default_voices(db)
    finally:
        db.close()
    
    print("\n🎉 Database initialization complete!")
    print("\nNext steps:")
    print("1. Create your first user: POST /admin/users")
    print("2. Test TTS endpoint: POST /v1/tts")
