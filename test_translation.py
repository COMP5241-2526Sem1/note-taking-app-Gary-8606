#!/usr/bin/env python3
"""
Test script to demonstrate the translation functionality
"""
import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_translation_functionality():
    print("🌍 Testing Translation Functionality\n")
    
    # 1. Create a test note if none exists
    print("1. Creating a test note...")
    test_note_data = {
        "title": "My Travel Plans",
        "content": "I'm planning to visit Paris next month. I want to see the Eiffel Tower, visit the Louvre Museum, and try some authentic French cuisine. I'm also planning to take a day trip to Versailles."
    }
    
    response = requests.post(f"{BASE_URL}/notes", json=test_note_data)
    if response.status_code == 201:
        note = response.json()
        note_id = note['id']
        print(f"   ✅ Created test note: '{note['title']}' (ID: {note_id})")
    else:
        print("   ❌ Failed to create test note")
        return
    
    # 2. Test translation to Spanish
    print(f"\n2. Testing translation to Spanish...")
    translation_data = {"target_language": "Spanish"}
    
    response = requests.post(f"{BASE_URL}/notes/{note_id}/translate", json=translation_data)
    if response.status_code == 200:
        result = response.json()
        print(f"   ✅ Translation successful!")
        print(f"   📝 Original Title: {result['original']['title']}")
        print(f"   🌍 Spanish Title: {result['translated']['title']}")
        print(f"   📝 Original Content: {result['original']['content'][:100]}...")
        print(f"   🌍 Spanish Content: {result['translated']['content'][:100]}...")
    else:
        error = response.json()
        print(f"   ❌ Translation failed: {error.get('error', 'Unknown error')}")
        return
    
    # 3. Test translation to French
    print(f"\n3. Testing translation to French...")
    translation_data = {"target_language": "French"}
    
    response = requests.post(f"{BASE_URL}/notes/{note_id}/translate", json=translation_data)
    if response.status_code == 200:
        result = response.json()
        print(f"   ✅ Translation successful!")
        print(f"   📝 Original Title: {result['original']['title']}")
        print(f"   🌍 French Title: {result['translated']['title']}")
        print(f"   📝 Original Content: {result['original']['content'][:100]}...")
        print(f"   🌍 French Content: {result['translated']['content'][:100]}...")
    else:
        error = response.json()
        print(f"   ❌ Translation failed: {error.get('error', 'Unknown error')}")
    
    # 4. Test translation to Japanese
    print(f"\n4. Testing translation to Japanese...")
    translation_data = {"target_language": "Japanese"}
    
    response = requests.post(f"{BASE_URL}/notes/{note_id}/translate", json=translation_data)
    if response.status_code == 200:
        result = response.json()
        print(f"   ✅ Translation successful!")
        print(f"   📝 Original Title: {result['original']['title']}")
        print(f"   🌍 Japanese Title: {result['translated']['title']}")
        print(f"   📝 Original Content: {result['original']['content'][:100]}...")
        print(f"   🌍 Japanese Content: {result['translated']['content'][:100]}...")
    else:
        error = response.json()
        print(f"   ❌ Translation failed: {error.get('error', 'Unknown error')}")
    
    print(f"\n🎉 Translation functionality test completed!")
    print(f"   You can now use the translate button in the UI to translate any note.")
    print(f"   Available languages include Spanish, French, German, Chinese, Japanese, and many more!")

if __name__ == "__main__":
    try:
        test_translation_functionality()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the Flask app. Make sure it's running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Error during test: {e}")