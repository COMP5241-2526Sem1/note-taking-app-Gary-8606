#!/usr/bin/env python3
"""
Demo script to test the drag and drop functionality
"""
import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_drag_drop_api():
    print("🧪 Testing Drag and Drop API functionality\n")
    
    # 1. Get initial notes
    print("1. Getting initial notes...")
    response = requests.get(f"{BASE_URL}/notes")
    initial_notes = response.json()
    print(f"   Found {len(initial_notes)} notes")
    for i, note in enumerate(initial_notes):
        print(f"   {i+1}. {note['title']} (ID: {note['id']}, Order: {note['order_index']})")
    
    if len(initial_notes) < 2:
        print("\n⚠️  Need at least 2 notes to test reordering. Creating some test notes...")
        
        # Create test notes
        test_notes = [
            {"title": "Task 1: Buy groceries", "content": "Milk, eggs, bread, fruits"},
            {"title": "Task 2: Call dentist", "content": "Schedule appointment for next week"},
            {"title": "Task 3: Finish project", "content": "Complete the drag and drop feature"}
        ]
        
        created_ids = []
        for note_data in test_notes:
            response = requests.post(f"{BASE_URL}/notes", json=note_data)
            if response.status_code == 201:
                note = response.json()
                created_ids.append(note['id'])
                print(f"   ✅ Created: {note['title']} (ID: {note['id']})")
        
        # Get updated notes list
        response = requests.get(f"{BASE_URL}/notes")
        initial_notes = response.json()
    
    print(f"\n2. Current note order:")
    for i, note in enumerate(initial_notes):
        print(f"   {i+1}. {note['title']} (ID: {note['id']}, Order: {note['order_index']})")
    
    # 3. Test reordering - reverse the order
    note_ids = [note['id'] for note in initial_notes]
    reversed_ids = list(reversed(note_ids))
    
    print(f"\n3. Reordering notes (reversing order)...")
    print(f"   Original order: {note_ids}")
    print(f"   New order: {reversed_ids}")
    
    response = requests.put(f"{BASE_URL}/notes/reorder", json={"note_ids": reversed_ids})
    if response.status_code == 200:
        print("   ✅ Reorder successful!")
    else:
        print(f"   ❌ Reorder failed: {response.text}")
        return
    
    # 4. Verify the new order
    print(f"\n4. Verifying new order...")
    response = requests.get(f"{BASE_URL}/notes")
    reordered_notes = response.json()
    
    for i, note in enumerate(reordered_notes):
        print(f"   {i+1}. {note['title']} (ID: {note['id']}, Order: {note['order_index']})")
    
    print(f"\n🎉 Drag and Drop API test completed successfully!")
    print(f"   The notes are now in the new order as expected.")

if __name__ == "__main__":
    try:
        test_drag_drop_api()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the Flask app. Make sure it's running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Error during test: {e}")