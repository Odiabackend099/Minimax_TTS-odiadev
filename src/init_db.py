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
    """Seed database with default MiniMax voices."""
    default_voices = [
        {
            "friendly_name": "nigerian-male",
            "minimax_voice_id": "moss_audio_141d8c4c-a6f8-11f0-84c1-0ec6fa858d82",
            "language": "en-NG",
            "gender": Gender.MALE,
            "description": "Nigerian male voice with natural accent",
            "is_cloned": False,
        },
        {
            "friendly_name": "american-male",
            "minimax_voice_id": "male-qn-qingse",
            "language": "en-US",
            "gender": Gender.MALE,
            "description": "American male voice, clear and professional",
            "is_cloned": False,
        },
        {
            "friendly_name": "british-female",
            "minimax_voice_id": "female-shaonv",
            "language": "en-GB",
            "gender": Gender.FEMALE,
            "description": "British female voice, warm and friendly",
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
            print(f"  ⏭️  Voice already exists: {voice_data['friendly_name']}")
    
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
