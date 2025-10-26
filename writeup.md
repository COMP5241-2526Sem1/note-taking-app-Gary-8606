# Note-Taking App - Project Writeup

## Project Overview

A modern, feature-rich note-taking web application built with Flask and deployed on Vercel. The application provides comprehensive note management capabilities with AI-powered features, collaborative sharing, and an intuitive drag-and-drop interface.

**Live Deployment:** https://note-9m1taqljx-gary-wongs-projects-618f39d1.vercel.app

---

## Table of Contents

1. [Features](#features)
2. [Technology Stack](#technology-stack)
3. [Architecture](#architecture)
4. [Implementation Details](#implementation-details)
5. [AI Integration](#ai-integration)
6. [Deployment](#deployment)
7. [Challenges and Solutions](#challenges-and-solutions)
8. [Future Enhancements](#future-enhancements)

---

## Features

### Core Features

#### 1. **Note Management (CRUD Operations)**
- Create, read, update, and delete notes
- Each note has a title, content, timestamps (created_at, updated_at)
- User-friendly interface with real-time updates
- Automatic saving and synchronization

#### 2. **Drag-and-Drop Reordering**
- Intuitive drag-and-drop interface for reordering notes
- Custom `order_index` field for persistent ordering
- Visual feedback during drag operations
- Automatic position updates via API endpoint

#### 3. **AI-Powered Translation**
- Translate notes to multiple languages
- Powered by OpenAI GPT-4.1-mini via GitHub Models API
- Translates both title and content
- Supports languages: Spanish, French, German, Japanese, Chinese, and more
- Beautiful modal interface showing original and translated versions

#### 4. **Smart Notes Generation**
- AI-powered structured note extraction from quick input
- Automatically generates:
  - Concise title (< 5 words)
  - Full sentence notes
  - Relevant tags (up to 3)
- Supports multiple languages
- Example: "Meeting tomorrow 3pm client" → Structured note with title, content, and tags

#### 5. **Note Templates**
- Pre-built templates for common note types:
  - Meeting Notes
  - Daily Journal
  - To-Do List
  - Project Planning
  - Study Notes
  - Book Notes
  - Recipe
  - Travel Itinerary
- Quick note creation from templates
- Customizable titles and content

#### 6. **Advanced Search & Filtering**
- Full-text search across titles and content
- Content-only search option
- Date range filtering (from/to dates)
- Multiple sorting options:
  - Most recently updated (default)
  - Oldest updated
  - Newest created
  - Oldest created
  - Title A-Z
  - Title Z-A
- Real-time search results

#### 7. **Note Sharing**
- Generate shareable public links for any note
- Optional password protection
- Optional expiration dates (1-365 days)
- Beautiful, mobile-responsive shared note pages
- View count tracking
- Share link management (create, list, revoke)
- Multiple active shares per note supported

### User Interface Features

- **Modern, Clean Design**: Professional UI with intuitive navigation
- **Responsive Layout**: Works seamlessly on desktop, tablet, and mobile
- **Modal Dialogs**: For translation, smart notes, templates, and sharing
- **Visual Feedback**: Loading states, success/error messages, animations
- **Editor Visibility**: Note editor visible by default for quick note creation
- **Action Buttons**: Clearly visible translate, share, and smart notes buttons

---

## Technology Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: 
  - SQLite (development & Vercel deployment - in-memory)
  - PostgreSQL/Supabase support (production-ready)
- **ORM**: SQLAlchemy
- **API Design**: RESTful JSON API
- **AI Integration**: OpenAI GPT-4.1-mini via GitHub Models

### Frontend
- **HTML5/CSS3**: Modern semantic markup and styling
- **JavaScript**: Vanilla JS for interactivity
- **Drag & Drop**: HTML5 Drag and Drop API
- **AJAX**: Fetch API for asynchronous operations

### Deployment & DevOps
- **Platform**: Vercel Serverless
- **Environment**: Python 3.x runtime
- **Configuration**: vercel.json with custom routing
- **Environment Variables**: Secure token management via Vercel CLI

### Development Tools
- **Version Control**: Git/GitHub
- **Environment Management**: python-dotenv
- **Testing**: Custom test scripts
- **API Testing**: curl, HTTP files

---

## Architecture

### Application Structure

```
note-taking-app-Gary-8606/
├── src/
│   ├── main.py                 # Flask app factory
│   ├── config.py               # Environment configurations
│   ├── llm.py                  # AI integration module
│   ├── templates.py            # Note templates
│   ├── models/
│   │   ├── note.py            # Note model
│   │   ├── share.py           # SharedNote model
│   │   └── user.py            # User model
│   ├── routes/
│   │   ├── note.py            # Note API endpoints
│   │   └── user.py            # User endpoints
│   └── static/
│       └── index.html         # Frontend application
├── api/
│   └── index.py               # Vercel serverless entry point
├── public/
│   └── index.html             # Static files for Vercel
├── vercel.json                # Vercel configuration
├── requirements.txt           # Python dependencies
└── .env                       # Environment variables
```

### Database Schema

#### Notes Table
```sql
CREATE TABLE notes (
    id INTEGER PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    order_index INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

#### Shared Notes Table
```sql
CREATE TABLE shared_notes (
    id INTEGER PRIMARY KEY,
    note_id INTEGER NOT NULL,
    share_token VARCHAR(32) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    expires_at DATETIME,
    is_active BOOLEAN DEFAULT TRUE,
    view_count INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE
);
```

### API Endpoints

#### Note Operations
- `GET /api/notes` - Get all notes (ordered by order_index, updated_at)
- `POST /api/notes` - Create a new note
- `GET /api/notes/<id>` - Get a specific note
- `PUT /api/notes/<id>` - Update a note
- `DELETE /api/notes/<id>` - Delete a note
- `PUT /api/notes/reorder` - Update note order

#### Search & Filter
- `GET /api/notes/search?q=<query>` - Simple search
- `GET /api/advanced-search?q=<query>&date_from=<date>&date_to=<date>&sort=<field>` - Advanced search

#### AI Features
- `POST /api/notes/<id>/translate` - Translate a note
  - Body: `{"target_language": "Spanish"}`
- `POST /api/notes/generate` - Generate structured note
  - Body: `{"input": "text", "language": "English"}`
- `POST /api/notes/generate-and-save` - Generate and save note

#### Templates
- `GET /api/notes/templates` - List all templates
- `GET /api/notes/templates/<id>` - Get specific template
- `POST /api/templates/<id>/create` - Create note from template

#### Sharing
- `POST /api/notes/<id>/share` - Create share link
  - Body: `{"password": "optional", "expires_days": 7}`
- `GET /api/notes/<id>/shares` - List all shares for a note
- `GET /shared/<token>` - Access shared note (HTML page)
- `GET /shares/<token>` - Access shared note (JSON API)
- `DELETE /shares/<token>` - Revoke share link

---

## Implementation Details

### 1. Drag-and-Drop Reordering

**Challenge**: Implement intuitive note reordering with persistent state.

**Solution**:
- Added `order_index` field to Note model
- Implemented HTML5 Drag and Drop API
- Created `/api/notes/reorder` endpoint
- Updates all note positions in single transaction

```javascript
// Frontend drag handlers
item.addEventListener('dragstart', (e) => {
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/html', item.innerHTML);
    dragSrcEl = item;
});

item.addEventListener('drop', async (e) => {
    // Reorder logic and API call
    await fetch('/api/notes/reorder', {
        method: 'PUT',
        body: JSON.stringify({ note_ids: newOrder })
    });
});
```

### 2. AI Translation Integration

**Implementation**:
- GitHub Models API with OpenAI GPT-4.1-mini
- Direct HTTP requests for Vercel compatibility
- Proper error handling for token issues
- Token trimming to prevent header errors

```python
def translate_text(text, target_language):
    prompt = f"Translate the following text to {target_language}:\n\n{text}"
    messages = [{"role": "user", "content": prompt}]
    return call_llm_model(model, messages)
```

**Key Features**:
- Translates both title and content
- Maintains formatting
- Returns original and translated versions
- Beautiful modal UI with copy functionality

### 3. Smart Notes Generation

**Implementation**:
- Structured prompt engineering
- JSON response parsing
- Automatic field extraction (title, notes, tags)
- Fallback handling for non-JSON responses

```python
system_prompt = '''
Extract the user's notes into the following structured fields:
1. Title: A concise title of the notes less than 5 words
2. Notes: The notes based on user input written in full sentences.
3. Tags (A list): At most 3 Keywords or tags that categorize the content.
Output in JSON format without ```json.
'''
```

### 4. Note Sharing System

**Implementation**:
- Secure token generation using `secrets.token_urlsafe(24)`
- Password hashing with werkzeug security
- Expiration date handling
- View count tracking
- Beautiful HTML rendering for shared notes

```python
class SharedNote(db.Model):
    share_token = Column(String(32), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=True)
    expires_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    view_count = Column(Integer, default=0)
```

### 5. Template System

**Implementation**:
- Pre-defined templates with placeholders
- Dynamic content generation
- Date/time insertion
- Custom title support

```python
templates = {
    'meeting': {
        'name': 'Meeting Notes',
        'icon': '📝',
        'title': 'Meeting - {date}',
        'content': '## Attendees\n- \n\n## Agenda\n1. \n\n## Notes\n\n## Action Items\n- [ ] '
    }
}
```

---

## AI Integration

### GitHub Models API Setup

1. **Token Generation**: 
   - GitHub Personal Access Token with Models permission
   - Stored securely in Vercel environment variables

2. **API Configuration**:
   - Endpoint: `https://models.github.ai/inference`
   - Model: `openai/gpt-4.1-mini`
   - Timeout: 30 seconds

3. **Error Handling**:
   - Invalid token detection (401)
   - Rate limiting (429)
   - Connection errors
   - Timeout handling
   - User-friendly error messages

### Translation Feature

- **Input**: Note title and content, target language
- **Process**: Two separate API calls for title and content
- **Output**: Original and translated versions in JSON
- **UI**: Modal with side-by-side comparison

### Smart Notes Feature

- **Input**: Quick text (e.g., "Meeting tomorrow 3pm")
- **Process**: Structured extraction via system prompt
- **Output**: JSON with title, notes, and tags
- **Options**: Preview or save directly

---

## Deployment

### Vercel Configuration

**vercel.json**:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    },
    {
      "src": "public/**",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/index.py"
    },
    {
      "src": "/shares/(.*)",
      "dest": "/api/index.py"
    },
    {
      "src": "/shared/(.*)",
      "dest": "/api/index.py"
    },
    {
      "src": "/",
      "dest": "/public/index.html"
    },
    {
      "src": "/(.*)",
      "dest": "/public/$1"
    }
  ],
  "env": {
    "FLASK_CONFIG": "production"
  }
}
```

### Environment Variables

**Required Variables** (set via Vercel CLI):
- `GITHUB_TOKEN`: GitHub Personal Access Token for AI features
- `FLASK_CONFIG`: Set to "production"

**Setting Environment Variables**:
```bash
printf "your-token-here" | vercel env add GITHUB_TOKEN production
printf "your-token-here" | vercel env add GITHUB_TOKEN preview
printf "your-token-here" | vercel env add GITHUB_TOKEN development
```

### Database Strategy

**Development**: SQLite database file
**Production (Vercel)**: In-memory SQLite (due to read-only filesystem)
**Alternative**: PostgreSQL/Supabase support included

```python
class ProductionConfig(Config):
    @staticmethod
    def get_database_uri():
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            return 'sqlite:///:memory:'  # In-memory for Vercel
        return database_url
```

### Deployment Process

1. **Prepare Files**:
   ```bash
   cp src/static/index.html public/
   ```

2. **Deploy**:
   ```bash
   vercel --prod --yes
   ```

3. **Verify**:
   - Check deployment URL
   - Test all endpoints
   - Verify environment variables

---

## Challenges and Solutions

### 1. **Vercel Read-Only Filesystem**

**Challenge**: Vercel serverless functions have a read-only filesystem, preventing SQLite file creation.

**Solution**: 
- Use in-memory SQLite (`sqlite:///:memory:`) for Vercel
- Support PostgreSQL for production use
- Data persists during function execution but resets between cold starts
- Acceptable for demo/development on Vercel

### 2. **GitHub Token Authentication**

**Challenge**: Multiple iterations to get the correct token with proper permissions.

**Issues Encountered**:
- Truncated token (had newline character)
- Wrong model name format
- Missing GitHub Models permission

**Solutions**:
- Token trimming: `.strip()` to remove whitespace
- Use `printf` instead of `echo` to avoid newlines
- Verified token has Models permission
- Correct model format: `openai/gpt-4.1-mini`

### 3. **JavaScript Event Listeners**

**Challenge**: Non-existent element reference causing all event listeners to fail.

**Solution**:
- Created safe `addListener()` helper function
- Checks element existence before binding
- Removed references to non-existent `templateNoteBtn`

```javascript
function addListener(selector, event, handler) {
    const element = document.querySelector(selector);
    if (element) {
        element.addEventListener(event, handler);
    }
}
```

### 4. **Share Link Routing**

**Challenge**: Share links returned 404 errors.

**Solution**:
- Added explicit routes in `vercel.json` for `/shared/` and `/shares/`
- Created HTML rendering for shared notes
- Separate JSON API endpoint for programmatic access

### 5. **Translation Connection Errors**

**Challenge**: OpenAI SDK had connection issues on Vercel.

**Solution**:
- Switched to direct HTTP requests using `requests` library
- Better error handling and timeout management
- More compatible with Vercel's serverless environment

---

## Future Enhancements

### Planned Features

1. **User Authentication**
   - Multi-user support
   - User registration and login
   - Personal note spaces

2. **Rich Text Editor**
   - Markdown support
   - WYSIWYG editing
   - Syntax highlighting for code

3. **Persistent External Database**
   - PostgreSQL/Supabase integration
   - Data persistence across deployments
   - Backup and export functionality

4. **Collaboration Features**
   - Real-time collaborative editing
   - Comments and annotations
   - Share with edit permissions

5. **Mobile App**
   - Native iOS/Android apps
   - Offline support
   - Push notifications

6. **Advanced AI Features**
   - Summary generation
   - Sentiment analysis
   - Auto-tagging
   - Related note suggestions

7. **Export & Import**
   - PDF export
   - Markdown export
   - Import from Evernote/OneNote
   - Bulk operations

8. **Organization**
   - Folders/categories
   - Tag-based organization
   - Favorites/pinning
   - Archive functionality

---

## Technical Achievements

### Performance
- ✅ Fast load times with serverless architecture
- ✅ Efficient API design with minimal requests
- ✅ Optimized database queries with proper indexing
- ✅ Client-side rendering for instant UI updates

### Security
- ✅ Password hashing for protected shares
- ✅ Secure token generation
- ✅ Environment variable protection
- ✅ SQL injection prevention via ORM
- ✅ XSS protection with proper escaping

### Code Quality
- ✅ Modular architecture with clear separation of concerns
- ✅ Comprehensive error handling
- ✅ RESTful API design
- ✅ Clean, maintainable code
- ✅ Inline documentation

### User Experience
- ✅ Intuitive interface
- ✅ Responsive design
- ✅ Clear visual feedback
- ✅ Error messages that guide users
- ✅ Smooth animations and transitions

---

## Conclusion

This note-taking application demonstrates a full-stack web development project with modern features and deployment practices. Key accomplishments include:

1. **Feature-Rich Application**: Comprehensive note management with CRUD, search, templates, and sharing
2. **AI Integration**: Successful integration of OpenAI GPT-4.1-mini for translation and smart notes
3. **Modern UI/UX**: Drag-and-drop, modals, responsive design
4. **Cloud Deployment**: Successfully deployed on Vercel with serverless architecture
5. **Problem Solving**: Overcame multiple deployment and integration challenges

The project showcases skills in:
- Backend development (Flask, SQLAlchemy, REST APIs)
- Frontend development (HTML, CSS, JavaScript)
- AI/ML integration (OpenAI API, prompt engineering)
- Cloud deployment (Vercel, serverless architecture)
- Database design and management
- Security best practices
- User experience design

**Live Demo**: https://note-9m1taqljx-gary-wongs-projects-618f39d1.vercel.app

---

## Repository

- **GitHub**: https://github.com/COMP5241-2526Sem1/note-taking-app-Gary-8606
- **Branch**: dev → main (via Pull Request #1)

---

*Last Updated: October 26, 2025*
