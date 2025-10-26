#!/usr/bin/env python3
"""
Test script for the Smart Note Generation feature
"""
import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_smart_note_generation():
    print("🤖 Testing Smart Note Generation Feature\n")
    
    test_cases = [
        {
            "input": "Meeting tmr 2pm with John about project review",
            "language": "English",
            "description": "Simple meeting reminder"
        },
        {
            "input": "Buy groceries: milk, eggs, bread, fruits. Also pick up dry cleaning",
            "language": "English", 
            "description": "Shopping list with multiple tasks"
        },
        {
            "input": "Call dentist for appointment next week, prefer afternoon",
            "language": "Spanish",
            "description": "Appointment scheduling in Spanish"
        },
        {
            "input": "Badminton tmr 5pm @polyu with team members",
            "language": "Chinese",
            "description": "Sports activity in Chinese"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"{i}. Testing: {case['description']}")
        print(f"   Input: '{case['input']}'")
        print(f"   Language: {case['language']}")
        
        try:
            # Test note generation (preview)
            response = requests.post(f"{BASE_URL}/notes/generate", json={
                "input": case["input"],
                "language": case["language"]
            })
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Generation successful!")
                print(f"   📝 Generated Title: {result['generated']['title']}")
                print(f"   📄 Generated Content: {result['generated']['content'][:100]}...")
                print(f"   🏷️  Generated Tags: {result['generated']['tags']}")
            else:
                error = response.json()
                print(f"   ❌ Generation failed: {error.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            
        print()  # Empty line for spacing
    
    # Test the generate-and-save endpoint
    print("5. Testing direct save functionality...")
    save_test = {
        "input": "Team standup meeting every Monday 9am, discuss progress and blockers",
        "language": "English"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/notes/generate-and-save", json=save_test)
        
        if response.status_code == 201:
            result = response.json()
            print(f"   ✅ Note created and saved successfully!")
            print(f"   📝 Note ID: {result['note']['id']}")
            print(f"   📝 Saved Title: {result['note']['title']}")
            print(f"   📄 Saved Content: {result['note']['content'][:100]}...")
        else:
            error = response.json()
            print(f"   ❌ Save failed: {error.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print(f"\n🎉 Smart Note Generation test completed!")
    print(f"   You can now use the 🤖 Smart Note button in the UI")
    print(f"   Just type quick notes and let AI structure them for you!")

if __name__ == "__main__":
    try:
        test_smart_note_generation()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the Flask app. Make sure it's running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Error during test: {e}")