from flask import Blueprint, jsonify, request, render_template_string
from src.models.note import Note, db
from src.models.share import SharedNote
from src.llm import translate_text, extract_structured_notes
from src.templates import get_template_list, get_template, format_template
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
        note = Note(title=data['title'], content=data['content'], order_index=max_order + 1, user_id=1)
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
    """Simple search for existing functionality"""
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
        try:
            translated_title = translate_text(note.title, target_language) if note.title else ""
            translated_content = translate_text(note.content, target_language) if note.content else ""
        except ValueError as ve:
            # Handle missing GITHUB_TOKEN
            return jsonify({
                'error': str(ve),
                'setup_instructions': 'Please configure a valid GitHub Personal Access Token with AI API access in your Vercel environment variables.'
            }), 503
        except Exception as translation_error:
            # Handle API errors
            error_msg = str(translation_error)
            if "Invalid GitHub token" in error_msg or "Unauthorized" in error_msg:
                return jsonify({
                    'error': 'GitHub token is not authorized for AI API access',
                    'instructions': [
                        '1. Visit https://github.com/marketplace/models to sign up for GitHub Models',
                        '2. Generate a new Personal Access Token with AI/Models permissions',
                        '3. Update GITHUB_TOKEN in Vercel environment variables',
                        '4. Redeploy the application'
                    ]
                }), 401
            return jsonify({'error': f'Translation API error: {error_msg}'}), 502
        
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

@note_bp.route('/notes/templates', methods=['GET'])
def get_note_templates():
    """Get list of available note templates"""
    try:
        templates = get_template_list()
        return jsonify({'templates': templates}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/templates/<template_id>', methods=['GET'])
def get_note_template(template_id):
    """Get a specific note template"""
    try:
        template = get_template(template_id)
        if not template:
            return jsonify({'error': 'Template not found'}), 404
        
        return jsonify({'template': template}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@note_bp.route('/templates/<template_id>/create', methods=['POST'])
def create_note_from_template(template_id):
    """Create a note from a template"""
    try:
        data = request.get_json()
        custom_title = data.get('title', '').strip() if data else ''
        
        # Get template
        template = get_template(template_id)
        if not template:
            return jsonify({'error': 'Template not found'}), 404
        
        # Format template
        note_data = format_template(template, custom_title)
        
        # Create note
        note = Note(
            title=note_data['title'],
            content=note_data['content'],
            user_id=1  # Default user for now
        )
        
        db.session.add(note)
        db.session.commit()
        
        return jsonify({
            'message': 'Note created successfully',
            'note': {
                'id': note.id,
                'title': note.title,
                'content': note.content,
                'created_at': note.created_at.isoformat(),
                'updated_at': note.updated_at.isoformat()
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@note_bp.route('/advanced-search', methods=['GET'])
def advanced_search():
    """Advanced search for notes with filtering and sorting"""
    try:
        # Get search parameters
        query = request.args.get('q', '').strip()
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        sort_by = request.args.get('sort', 'updated_desc')
        content_only = request.args.get('content_only') == 'true'
        
        # Start with base query
        notes_query = Note.query.filter(Note.user_id == 1)  # Filter by user
        
        # Apply text search
        if query:
            if content_only:
                # Search only in content
                notes_query = notes_query.filter(Note.content.contains(query))
            else:
                # Search in both title and content
                notes_query = notes_query.filter(
                    db.or_(
                        Note.title.contains(query),
                        Note.content.contains(query)
                    )
                )
        
        # Apply date filters
        if date_from:
            try:
                from datetime import datetime
                from_date = datetime.strptime(date_from, '%Y-%m-%d').date()
                notes_query = notes_query.filter(Note.created_at >= from_date)
            except ValueError:
                pass
        
        if date_to:
            try:
                from datetime import datetime, timedelta
                to_date = datetime.strptime(date_to, '%Y-%m-%d').date() + timedelta(days=1)
                notes_query = notes_query.filter(Note.created_at < to_date)
            except ValueError:
                pass
        
        # Apply sorting
        if sort_by == 'updated_asc':
            notes_query = notes_query.order_by(Note.updated_at.asc())
        elif sort_by == 'created_desc':
            notes_query = notes_query.order_by(Note.created_at.desc())
        elif sort_by == 'created_asc':
            notes_query = notes_query.order_by(Note.created_at.asc())
        elif sort_by == 'title_asc':
            notes_query = notes_query.order_by(Note.title.asc())
        elif sort_by == 'title_desc':
            notes_query = notes_query.order_by(Note.title.desc())
        else:  # default: updated_desc
            notes_query = notes_query.order_by(Note.updated_at.desc())
        
        # Execute query
        notes = notes_query.all()
        
        return jsonify({
            'notes': [{
                'id': note.id,
                'title': note.title,
                'content': note.content,
                'created_at': note.created_at.isoformat(),
                'updated_at': note.updated_at.isoformat()
            } for note in notes]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Note Sharing Endpoints

@note_bp.route('/notes/<int:note_id>/share', methods=['POST'])
def create_share_link(note_id):
    """Create a shareable link for a note"""
    try:
        # Check if note exists and belongs to user
        note = Note.query.filter_by(id=note_id, user_id=1).first()
        if not note:
            return jsonify({'error': 'Note not found'}), 404
        
        data = request.get_json() or {}
        password = data.get('password', '').strip() or None
        expires_days = data.get('expires_days')
        
        # Validate expires_days
        if expires_days is not None:
            try:
                expires_days = int(expires_days)
                if expires_days < 1 or expires_days > 365:
                    return jsonify({'error': 'Expiration must be between 1 and 365 days'}), 400
            except (ValueError, TypeError):
                return jsonify({'error': 'Invalid expiration days'}), 400
        
        # Create shared note
        shared_note = SharedNote(
            note_id=note_id,
            password=password,
            expires_days=expires_days
        )
        
        db.session.add(shared_note)
        db.session.commit()
        
        return jsonify({
            'message': 'Share link created successfully',
            'share': shared_note.to_dict(),
            'share_url': f'/shared/{shared_note.share_token}'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/<int:note_id>/shares', methods=['GET'])
def get_note_shares(note_id):
    """Get all share links for a note"""
    try:
        # Check if note exists and belongs to user
        note = Note.query.filter_by(id=note_id, user_id=1).first()
        if not note:
            return jsonify({'error': 'Note not found'}), 404
        
        shares = SharedNote.query.filter_by(note_id=note_id).order_by(SharedNote.created_at.desc()).all()
        
        return jsonify({
            'shares': [share.to_dict() for share in shares]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@note_bp.route('/shared/<share_token>', methods=['GET'])
def get_shared_note_page(share_token):
    """Access a shared note by token - returns HTML page"""
    try:
        shared_note = SharedNote.query.filter_by(share_token=share_token).first()
        if not shared_note:
            return render_template_string('''
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Note Not Found</title>
                    <style>
                        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
                        .error { color: #d32f2f; }
                    </style>
                </head>
                <body>
                    <h1 class="error">Shared Note Not Found</h1>
                    <p>The shared note you're looking for doesn't exist or has been removed.</p>
                </body>
                </html>
            '''), 404
        
        if not shared_note.is_accessible():
            error_msg = 'This shared link has expired' if shared_note.is_expired() else 'This shared link is no longer active'
            return render_template_string(f'''
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Link Unavailable</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }}
                        .error {{ color: #d32f2f; }}
                    </style>
                </head>
                <body>
                    <h1 class="error">Link Unavailable</h1>
                    <p>{error_msg}</p>
                </body>
                </html>
            '''), 410 if shared_note.is_expired() else 403
        
        # Check if password is required
        if shared_note.password_hash:
            password = request.args.get('password')
            if not password or not shared_note.check_password(password):
                return render_template_string('''
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>Password Required</title>
                        <style>
                            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
                            input, button { padding: 10px; margin: 10px 0; }
                            button { background: #1976d2; color: white; border: none; cursor: pointer; }
                            button:hover { background: #1565c0; }
                        </style>
                    </head>
                    <body>
                        <h1>🔒 Password Required</h1>
                        <p>This shared note is password protected.</p>
                        <form method="get">
                            <input type="password" name="password" placeholder="Enter password" required>
                            <br>
                            <button type="submit">View Note</button>
                        </form>
                    </body>
                    </html>
                '''), 200
        
        # Increment view count
        shared_note.increment_view_count()
        
        # Return HTML page with the note
        return render_template_string('''
            <!DOCTYPE html>
            <html>
            <head>
                <title>{{ note.title }}</title>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body {
                        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                        max-width: 800px;
                        margin: 0 auto;
                        padding: 20px;
                        background: #f5f5f5;
                    }
                    .note-container {
                        background: white;
                        border-radius: 8px;
                        padding: 30px;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    }
                    h1 {
                        color: #333;
                        margin-bottom: 10px;
                    }
                    .meta {
                        color: #666;
                        font-size: 14px;
                        margin-bottom: 20px;
                        padding-bottom: 15px;
                        border-bottom: 1px solid #eee;
                    }
                    .content {
                        white-space: pre-wrap;
                        word-wrap: break-word;
                        line-height: 1.6;
                        color: #444;
                    }
                    .footer {
                        margin-top: 30px;
                        padding-top: 20px;
                        border-top: 1px solid #eee;
                        text-align: center;
                        color: #999;
                        font-size: 12px;
                    }
                </style>
            </head>
            <body>
                <div class="note-container">
                    <h1>{{ note.title }}</h1>
                    <div class="meta">
                        Created: {{ note.created_at.strftime('%B %d, %Y at %I:%M %p') }}
                        • Views: {{ view_count }}
                    </div>
                    <div class="content">{{ note.content }}</div>
                    <div class="footer">
                        This is a shared note from Note Taking App
                    </div>
                </div>
            </body>
            </html>
        ''', note=shared_note.note, view_count=shared_note.view_count)
        
    except Exception as e:
        return render_template_string(f'''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Error</title>
                <style>
                    body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }}
                    .error {{ color: #d32f2f; }}
                </style>
            </head>
            <body>
                <h1 class="error">Error</h1>
                <p>An error occurred: {str(e)}</p>
            </body>
            </html>
        '''), 500

@note_bp.route('/shares/<share_token>', methods=['GET'])
def get_shared_note(share_token):
    """Access a shared note by token - API endpoint (JSON response)"""
    try:
        shared_note = SharedNote.query.filter_by(share_token=share_token).first()
        if not shared_note:
            return jsonify({'error': 'Shared note not found'}), 404
        
        if not shared_note.is_accessible():
            if shared_note.is_expired():
                return jsonify({'error': 'This shared link has expired'}), 410
            else:
                return jsonify({'error': 'This shared link is no longer active'}), 403
        
        # Check if password is required
        if shared_note.password_hash:
            password = request.args.get('password') or request.headers.get('X-Share-Password')
            if not password or not shared_note.check_password(password):
                return jsonify({
                    'error': 'Password required',
                    'requires_password': True
                }), 401
        
        # Increment view count
        shared_note.increment_view_count()
        
        return jsonify({
            'note': {
                'title': shared_note.note.title,
                'content': shared_note.note.content,
                'created_at': shared_note.note.created_at.isoformat(),
                'updated_at': shared_note.note.updated_at.isoformat()
            },
            'share_info': {
                'view_count': shared_note.view_count,
                'created_at': shared_note.created_at.isoformat()
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@note_bp.route('/api/shares/<share_token>', methods=['GET'])
def get_shared_note_api(share_token):
    """API alias for getting shared notes"""
    return get_shared_note(share_token)

@note_bp.route('/shares/<share_token>', methods=['DELETE'])
def revoke_share_link(share_token):
    """Revoke a share link"""
    try:
        shared_note = SharedNote.query.filter_by(share_token=share_token).first()
        if not shared_note:
            return jsonify({'error': 'Shared note not found'}), 404
        
        # Check ownership (in a real app, you'd verify the user owns the note)
        if shared_note.note.user_id != 1:
            return jsonify({'error': 'Access denied'}), 403
        
        shared_note.is_active = False
        db.session.commit()
        
        return jsonify({'message': 'Share link revoked successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

