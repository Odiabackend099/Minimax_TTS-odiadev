"""Script to create the first admin user."""
import sys
from .database import SessionLocal
from .models import User, Plan, PLAN_CONFIGS
from .auth import generate_api_key, hash_api_key


def create_admin_user(name: str, email: str):
    """
    Create an admin user with enterprise plan.
    
    This user can then create other users via the API.
    """
    db = SessionLocal()
    
    try:
        # Check if user already exists
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            print(f"❌ User with email {email} already exists!")
            print(f"   User ID: {existing.id}")
            print(f"   Plan: {existing.plan.value}")
            return
        
        # Generate API key
        api_key = generate_api_key()
        api_key_hash = hash_api_key(api_key)
        
        # Create enterprise user (acts as admin)
        plan_config = PLAN_CONFIGS[Plan.ENTERPRISE]
        user = User(
            name=name,
            email=email,
            api_key_hash=api_key_hash,
            plan=Plan.ENTERPRISE,
            quota_seconds=plan_config["quota_seconds"],
            used_seconds=0.0,
            is_active=True,
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        print("\n✅ Admin user created successfully!")
        print(f"\n{'='*70}")
        print(f"📝 User Details:")
        print(f"   ID:    {user.id}")
        print(f"   Name:  {user.name}")
        print(f"   Email: {user.email}")
        print(f"   Plan:  {user.plan.value.upper()}")
        print(f"   Quota: {user.quota_seconds}s ({user.quota_seconds/60:.0f} minutes)")
        print(f"\n🔑 API Key (SAVE THIS - shown only once!):")
        print(f"   {api_key}")
        print(f"{'='*70}\n")
        print("💡 Use this key in Authorization header:")
        print(f"   Authorization: Bearer {api_key}\n")
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python -m src.create_admin <name> <email>")
        print("\nExample:")
        print('  python -m src.create_admin "Admin User" "admin@odeadev.com"')
        sys.exit(1)
    
    name = sys.argv[1]
    email = sys.argv[2]
    
    print(f"Creating admin user: {name} ({email})")
    create_admin_user(name, email)
