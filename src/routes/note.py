from flask import Blueprint, jsonify, request
from src.models.note import Note, db
from src.llm import translate_text, extract_structured_notes
import json

note_bp = Blueprint('note', __name__)

@note_bp.route('/notes', methods=['GET'])
def get_notes():
    """Get all notes, ordered by order_index, then by most recently updated"""
    notes = Note.query.order_by(Note.order_index.asc(), Note.updated_at.desc()).all()
    return jsonify([note.to_dict() for note in notes])

@note_bp.route('/notes', methods=['POST'])
def create_note():
    """Create a new note"""
    try:
        data = request.json
        if not data or 'title' not in data or 'content' not in data:
            return jsonify({'error': 'Title and content are required'}), 400
        
        # Get the highest order_index and add 1 to put new notes at the end
        max_order = db.session.query(db.func.max(Note.order_index)).scalar() or 0
        note = Note(title=data['title'], content=data['content'], order_index=max_order + 1)
        db.session.add(note)
        db.session.commit()
        return jsonify(note.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    """Get a specific note by ID"""
    note = Note.query.get_or_404(note_id)
    return jsonify(note.to_dict())

@note_bp.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    """Update a specific note"""
    try:
        note = Note.query.get_or_404(note_id)
        data = request.json
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        note.title = data.get('title', note.title)
        note.content = data.get('content', note.content)
        db.session.commit()
        return jsonify(note.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    """Delete a specific note"""
    try:
        note = Note.query.get_or_404(note_id)
        db.session.delete(note)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/search', methods=['GET'])
def search_notes():
    """Search notes by title or content"""
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    
    notes = Note.query.filter(
        (Note.title.contains(query)) | (Note.content.contains(query))
    ).order_by(Note.order_index.asc(), Note.updated_at.desc()).all()
    
    return jsonify([note.to_dict() for note in notes])

@note_bp.route('/notes/reorder', methods=['PUT'])
def reorder_notes():
    """Reorder notes based on provided array of note IDs"""
    try:
        data = request.json
        if not data or 'note_ids' not in data:
            return jsonify({'error': 'note_ids array is required'}), 400
        
        note_ids = data['note_ids']
        
        # Update order_index for each note
        for index, note_id in enumerate(note_ids):
            note = Note.query.get(note_id)
            if note:
                note.order_index = index
        
        db.session.commit()
        return jsonify({'message': 'Notes reordered successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/<int:note_id>/translate', methods=['POST'])
def translate_note(note_id):
    """Translate a note's content to the specified target language"""
    try:
        note = Note.query.get_or_404(note_id)
        
        data = request.json
        if not data or 'target_language' not in data:
            return jsonify({'error': 'target_language is required'}), 400
        
        target_language = data['target_language']
        
        # Translate both title and content
        translated_title = translate_text(note.title, target_language) if note.title else ""
        translated_content = translate_text(note.content, target_language) if note.content else ""
        
        return jsonify({
            'original': {
                'title': note.title,
                'content': note.content
            },
            'translated': {
                'title': translated_title,
                'content': translated_content
            },
            'target_language': target_language
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/generate', methods=['POST'])
def generate_structured_note():
    """Generate a structured note from user input using LLM"""
    try:
        data = request.json
        if not data or 'input' not in data:
            return jsonify({'error': 'input is required'}), 400
        
        user_input = data['input'].strip()
        if not user_input:
            return jsonify({'error': 'input cannot be empty'}), 400
            
        language = data.get('language', 'English')
        
        # Generate structured notes using LLM
        llm_response = extract_structured_notes(user_input, language)
        
        # Parse the JSON response from LLM
        try:
            structured_data = json.loads(llm_response)
        except json.JSONDecodeError:
            # If LLM doesn't return valid JSON, create a basic structure
            structured_data = {
                "Title": "Generated Note",
                "Notes": user_input,
                "Tags": []
            }
        
        # Ensure all required fields exist
        title = structured_data.get('Title', 'Generated Note')
        notes = structured_data.get('Notes', user_input)
        tags = structured_data.get('Tags', [])
        
        return jsonify({
            'generated': {
                'title': title,
                'content': notes,
                'tags': tags
            },
            'original_input': user_input,
            'language': language
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/generate-and-save', methods=['POST'])
def generate_and_save_note():
    """Generate a structured note and save it directly"""
    try:
        data = request.json
        if not data or 'input' not in data:
            return jsonify({'error': 'input is required'}), 400
        
        user_input = data['input'].strip()
        if not user_input:
            return jsonify({'error': 'input cannot be empty'}), 400
            
        language = data.get('language', 'English')
        
        # Generate structured notes using LLM
        llm_response = extract_structured_notes(user_input, language)
        
        # Parse the JSON response from LLM
        try:
            structured_data = json.loads(llm_response)
        except json.JSONDecodeError:
            # If LLM doesn't return valid JSON, create a basic structure
            structured_data = {
                "Title": "Generated Note",
                "Notes": user_input,
                "Tags": []
            }
        
        # Ensure all required fields exist
        title = structured_data.get('Title', 'Generated Note')
        notes = structured_data.get('Notes', user_input)
        tags = structured_data.get('Tags', [])
        
        # Add tags to the content if they exist
        content = notes
        if tags:
            content += f"\n\nTags: {', '.join(tags)}"
        
        # Create and save the note
        max_order = db.session.query(db.func.max(Note.order_index)).scalar() or 0
        note = Note(title=title, content=content, order_index=max_order + 1)
        db.session.add(note)
        db.session.commit()
        
        return jsonify({
            'note': note.to_dict(),
            'generated': {
                'title': title,
                'content': notes,
                'tags': tags
            },
            'original_input': user_input,
            'language': language
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

