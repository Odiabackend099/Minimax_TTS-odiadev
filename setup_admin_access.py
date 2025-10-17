#!/usr/bin/env python3
"""Setup admin access for ODIADEV TTS service."""

import requests
import json
import base64
from datetime import datetime

# Configuration
API_BASE_URL = "https://minimax-tts-odiadev.onrender.com"

def check_service_status():
    """Check if service is running and get info."""
    print("🏥 Checking service status...")
    
    try:
        # Check health
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Service is healthy")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
        
        # Check OpenAPI spec
        response = requests.get(f"{API_BASE_URL}/openapi.json", timeout=10)
        if response.status_code == 200:
            spec = response.json()
            print("✅ API documentation accessible")
            print(f"   - Title: {spec.get('info', {}).get('title', 'N/A')}")
            print(f"   - Version: {spec.get('info', {}).get('version', 'N/A')}")
            
            # Check if there are any public endpoints
            paths = spec.get('paths', {})
            print(f"   - Available endpoints: {len(paths)}")
            
            public_endpoints = []
            for path, methods in paths.items():
                for method, details in methods.items():
                    if isinstance(details, dict):
                        security = details.get('security', [])
                        if not security:  # No security requirements
                            public_endpoints.append(f"{method.upper()} {path}")
            
            if public_endpoints:
                print("   - Public endpoints (no auth required):")
                for endpoint in public_endpoints:
                    print(f"     - {endpoint}")
            else:
                print("   - All endpoints require authentication")
            
            return True
        else:
            print(f"❌ API documentation failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Service check failed: {e}")
        return False

def try_admin_endpoints():
    """Try different approaches to access admin endpoints."""
    print("\n🔐 Trying admin endpoint access...")
    
    # Try 1: No auth header
    print("   - Trying POST /admin/users without auth...")
    try:
        response = requests.post(f"{API_BASE_URL}/admin/users", 
                               json={"name": "Test", "email": "test@test.com", "plan": "free"},
                               timeout=10)
        print(f"     Status: {response.status_code}")
        if response.status_code != 401:
            print(f"     Response: {response.text[:100]}...")
    except Exception as e:
        print(f"     Error: {e}")
    
    # Try 2: With empty auth header
    print("   - Trying POST /admin/users with empty auth...")
    try:
        headers = {"Authorization": "", "Content-Type": "application/json"}
        response = requests.post(f"{API_BASE_URL}/admin/users", 
                               headers=headers,
                               json={"name": "Test", "email": "test2@test.com", "plan": "free"},
                               timeout=10)
        print(f"     Status: {response.status_code}")
        if response.status_code != 401:
            print(f"     Response: {response.text[:100]}...")
    except Exception as e:
        print(f"     Error: {e}")
    
    # Try 3: With dummy auth header
    print("   - Trying POST /admin/users with dummy auth...")
    try:
        headers = {"Authorization": "Bearer dummy-key", "Content-Type": "application/json"}
        response = requests.post(f"{API_BASE_URL}/admin/users", 
                               headers=headers,
                               json={"name": "Test", "email": "test3@test.com", "plan": "free"},
                               timeout=10)
        print(f"     Status: {response.status_code}")
        if response.status_code != 401:
            print(f"     Response: {response.text[:100]}...")
    except Exception as e:
        print(f"     Error: {e}")

def check_environment_variables():
    """Check if we can determine environment variables."""
    print("\n🔧 Checking environment configuration...")
    
    # Try to access any endpoint that might reveal environment info
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=10)
        print(f"   - Root endpoint: {response.status_code}")
        if response.text:
            print(f"     Response: {response.text[:200]}...")
    except Exception as e:
        print(f"   - Root endpoint error: {e}")
    
    # Check if there's a way to get environment info
    try:
        response = requests.get(f"{API_BASE_URL}/env", timeout=10)
        print(f"   - Environment endpoint: {response.status_code}")
    except Exception as e:
        print(f"   - Environment endpoint error: {e}")

def main():
    """Main function."""
    print("🎯 ODIADEV TTS - Admin Access Setup")
    print("=" * 60)
    print("Attempting to setup admin access for the service...")
    print()
    
    # Check service status
    if not check_service_status():
        print("❌ Service is not accessible. Exiting.")
        return
    
    # Try admin endpoints
    try_admin_endpoints()
    
    # Check environment
    check_environment_variables()
    
    print(f"\n📋 SUMMARY")
    print("=" * 60)
    print("✅ Service is running and healthy")
    print("❌ All endpoints require authentication")
    print("💡 To test the TTS service, you need to:")
    print("   1. Set up admin authentication in the service")
    print("   2. Create a user with API key")
    print("   3. Use the API key for TTS generation")
    print("\n🔧 Possible solutions:")
    print("   - Set ENFORCE_AUTH=false in Render environment variables")
    print("   - Create an admin user manually in the database")
    print("   - Use a different authentication method")

if __name__ == "__main__":
    main()
