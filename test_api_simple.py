#!/usr/bin/env python3
"""
Simple test script to verify the note creation API
"""

import requests
import json

# Test the local server
BASE_URL = "http://127.0.0.1:5000"

def test_api():
    print("🧪 Testing Note Creation API...")
    
    # Test creating a note
    note_data = {
        "title": "Test Note from API",
        "content": "This is a test note created via API to verify functionality."
    }
    
    try:
        # Create note
        print("📝 Creating note...")
        response = requests.post(f"{BASE_URL}/api/notes", json=note_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            note = response.json()
            print(f"✅ Note created successfully! ID: {note['id']}")
            
            # Get all notes
            print("\n📚 Getting all notes...")
            response = requests.get(f"{BASE_URL}/api/notes")
            print(f"Status: {response.status_code}")
            notes = response.json()
            print(f"✅ Found {len(notes)} notes")
            
            return True
        else:
            print(f"❌ Failed to create note: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure Flask is running on port 5000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_api()
    if success:
        print("\n🎉 API test passed! Note creation is working.")
    else:
        print("\n💥 API test failed. Check server logs for errors.")