[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=20424596)

# 📝 NoteTaker - AI-Powered Note Management Application

A modern, feature-rich web application for managing personal notes with AI-powered features, collaborative sharing, and an intuitive drag-and-drop interface. Built with Flask and deployed on Vercel serverless platform.

## 🚀 Live Demo

**Production URL**: https://note-9m1taqljx-gary-wongs-projects-618f39d1.vercel.app

## ✨ Features Overview

### 📋 Core Note Management
- **Full CRUD Operations**: Create, read, update, and delete notes
- **Auto-save**: Notes are automatically saved as you type
- **Drag-and-Drop Reordering**: Intuitive interface to reorder notes by dragging
- **Persistent Ordering**: Custom order_index field maintains your preferred note order
- **Real-time Updates**: Instant feedback and seamless UI updates

### 🤖 AI-Powered Features

#### 🌍 Translation
- **Multi-language Translation**: Translate notes to any language
- **Powered by GPT-4.1-mini**: Uses OpenAI's latest model via GitHub Models API
- **Dual Translation**: Translates both title and content
- **Supported Languages**: Spanish, French, German, Japanese, Chinese, and more
- **Beautiful UI**: Side-by-side comparison of original and translated text

#### 🧠 Smart Notes Generation
- **Quick Input Processing**: Convert brief text into structured notes
- **AI Extraction**: Automatically generates:
  - Concise title (< 5 words)
  - Full sentence notes
  - Relevant tags (up to 3)
- **Multi-language Support**: Generate notes in your preferred language
- **Example**: "Meeting tomorrow 3pm client" → Structured note with title, content, and tags

### 📑 Templates System
Pre-built templates for quick note creation:
- **📝 Meeting Notes**: Attendees, agenda, notes, action items
- **📔 Daily Journal**: Morning reflection, gratitude, goals, evening review
- **✅ To-Do List**: Organized task management
- **🎯 Project Planning**: Goals, timeline, resources, milestones
- **📚 Study Notes**: Subject, topics, key concepts, questions
- **📖 Book Notes**: Title, author, summary, key takeaways, quotes
- **🍳 Recipe**: Ingredients, instructions, prep/cook time, servings
- **✈️ Travel Itinerary**: Destination, dates, accommodations, activities

### 🔍 Advanced Search & Filtering
- **Full-text Search**: Search across titles and content
- **Content-only Search**: Option to search only in note content
- **Date Range Filtering**: Filter by creation date (from/to)
- **Multiple Sort Options**:
  - Most recently updated (default)
  - Oldest updated
  - Newest created
  - Oldest created
  - Title A-Z
  - Title Z-A
- **Real-time Results**: Instant search feedback

### 🔗 Note Sharing
- **Public Share Links**: Generate shareable links for any note
- **Password Protection**: Optional password to secure shared notes
- **Expiration Dates**: Set expiration (1-365 days) for time-limited sharing
- **Beautiful Shared Pages**: Mobile-responsive HTML pages for shared notes
- **View Tracking**: Monitor how many times your note has been viewed
- **Share Management**: Create, list, and revoke share links
- **Multiple Shares**: Create multiple share links for the same note

### 🎨 User Interface
- **Modern Design**: Clean, professional interface
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Modal Dialogs**: For translation, templates, and sharing
- **Visual Feedback**: Loading states, success/error messages
- **Smooth Animations**: Polished transitions and effects
- **Default Editor Visibility**: Note editor visible for quick access

## 🛠 Technology Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: SQLite (in-memory for Vercel), PostgreSQL/Supabase support
- **ORM**: SQLAlchemy
- **API Design**: RESTful JSON API
- **AI Integration**: OpenAI GPT-4.1-mini via GitHub Models API

### Frontend
- **HTML5**: Semantic markup structure
- **CSS3**: Modern styling with responsive design
- **JavaScript (ES6+)**: Vanilla JS for interactivity
- **Drag & Drop**: HTML5 Drag and Drop API
- **AJAX**: Fetch API for asynchronous operations

### Deployment & DevOps
- **Platform**: Vercel Serverless
- **Runtime**: Python 3.x
- **Configuration**: vercel.json with custom routing
- **Environment**: Secure token management via Vercel CLI
- **CI/CD**: Automatic deployments via Git integration

## 📁 Project Structure

```
note-taking-app-Gary-8606/
├── src/
│   ├── models/
│   │   ├── note.py              # Note model with order_index
│   │   ├── share.py             # SharedNote model for sharing
│   │   └── user.py              # User model
│   ├── routes/
│   │   ├── note.py              # Note API endpoints (CRUD, search, share, translate)
│   │   └── user.py              # User API routes
│   ├── static/
│   │   └── index.html           # Frontend application
│   ├── main.py                  # Flask app factory
│   ├── config.py                # Environment configurations
│   ├── llm.py                   # AI integration (translation, smart notes)
│   └── templates.py             # Note templates
├── api/
│   └── index.py                 # Vercel serverless entry point
├── public/
│   └── index.html               # Static files for Vercel
├── database/
│   └── app.db                   # SQLite database (development)
├── vercel.json                  # Vercel deployment configuration
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables
├── writeup.md                   # Comprehensive project documentation
└── README.md                    # This file
```

## 🔧 Local Development Setup

### Prerequisites
- Python 3.11+
- pip (Python package manager)
- GitHub Personal Access Token with Models permission (for AI features)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/COMP5241-2526Sem1/note-taking-app-Gary-8606.git
   cd note-taking-app-Gary-8606
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   ```bash
   source venv/bin/activate  # On Linux/Mac
   # or
   venv\Scripts\activate     # On Windows
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   GITHUB_TOKEN=your_github_token_here
   FLASK_CONFIG=development
   SECRET_KEY=your-secret-key-here
   ```

6. **Run the application**
   ```bash
   python src/main.py
   ```

7. **Access the application**
   - Open your browser and go to `http://localhost:5000`

### Getting a GitHub Token for AI Features

1. Visit https://github.com/marketplace/models
2. Sign up for GitHub Models access
3. Go to https://github.com/settings/tokens
4. Generate a new Personal Access Token with Models permissions
5. Add the token to your `.env` file

## 📡 API Endpoints

### Note Operations
- `GET /api/notes` - Get all notes (ordered by order_index, updated_at)
- `POST /api/notes` - Create a new note
- `GET /api/notes/<id>` - Get a specific note
- `PUT /api/notes/<id>` - Update a note
- `DELETE /api/notes/<id>` - Delete a note
- `PUT /api/notes/reorder` - Update note order (drag-and-drop)

### Search & Filter
- `GET /api/notes/search?q=<query>` - Simple search
- `GET /api/advanced-search?q=<query>&date_from=<date>&date_to=<date>&sort=<field>` - Advanced search

### AI Features
- `POST /api/notes/<id>/translate` - Translate a note
  - Body: `{"target_language": "Spanish"}`
- `POST /api/notes/generate` - Generate structured note (preview)
  - Body: `{"input": "text", "language": "English"}`
- `POST /api/notes/generate-and-save` - Generate and save note
  - Body: `{"input": "text", "language": "English"}`

### Templates
- `GET /api/notes/templates` - List all templates
- `GET /api/notes/templates/<id>` - Get specific template
- `POST /api/templates/<id>/create` - Create note from template
  - Body: `{"title": "optional custom title"}`

### Sharing
- `POST /api/notes/<id>/share` - Create share link
  - Body: `{"password": "optional", "expires_days": 7}`
- `GET /api/notes/<id>/shares` - List all shares for a note
- `GET /shared/<token>` - Access shared note (HTML page)
- `GET /shares/<token>` - Access shared note (JSON API)
- `DELETE /shares/<token>` - Revoke share link

### Request/Response Format

**Create/Update Note**:
```json
{
  "title": "My Note Title",
  "content": "Note content here..."
}
```

**Note Response**:
```json
{
  "id": 1,
  "title": "My Note Title",
  "content": "Note content here...",
  "user_id": 1,
  "order_index": 0,
  "created_at": "2025-10-26T12:00:00.000000",
  "updated_at": "2025-10-26T12:30:00.000000"
}
```

**Translation Response**:
```json
{
  "original": {
    "title": "Hello World",
    "content": "This is a test."
  },
  "translated": {
    "title": "Hola Mundo",
    "content": "Esto es una prueba."
  },
  "target_language": "Spanish"
}
```

## 🎨 User Interface Features

### Main Application
- **Note List**: Drag-and-drop reorderable list of all notes
- **Search Box**: Real-time search with advanced filters
- **New Note Button**: Quick note creation
- **Action Buttons**: Translate, Share, Smart Notes clearly visible

### Note Editor
- **Title Input**: Edit note titles
- **Content Textarea**: Full-featured text editing
- **Save Button**: Manual save (auto-save also available)
- **Delete Button**: Remove notes with confirmation
- **Translate Button**: AI-powered translation
- **Share Button**: Create public share links

### Modals & Dialogs
- **Translation Modal**: Side-by-side original and translated text
- **Smart Notes Modal**: Preview AI-generated structured notes
- **Templates Modal**: Browse and select from 8 templates
- **Share Modal**: Configure and manage share links
- **Advanced Search**: Comprehensive search and filter options

### Design Elements
- **Responsive Layout**: Adapts to desktop, tablet, and mobile
- **Modern UI**: Clean, professional design
- **Smooth Animations**: Polished transitions and effects
- **Visual Feedback**: Loading states, success/error messages
- **Accessibility**: Keyboard navigation and screen reader support

## 🔒 Database Schema

### Notes Table
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

### Shared Notes Table
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

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 🚀 Deployment

### Vercel Deployment

The application is deployed on Vercel serverless platform with the following configuration:

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
  ]
}
```

### Environment Variables Setup

Set environment variables via Vercel CLI:

```bash
# Add GitHub token for AI features
printf "your-github-token" | vercel env add GITHUB_TOKEN production
printf "your-github-token" | vercel env add GITHUB_TOKEN preview
printf "your-github-token" | vercel env add GITHUB_TOKEN development

# Deploy to production
vercel --prod
```

### Database Configuration

- **Development**: SQLite file (`src/database/app.db`)
- **Production (Vercel)**: In-memory SQLite (due to read-only filesystem)
- **Alternative**: PostgreSQL/Supabase (set `DATABASE_URL` environment variable)

### Deployment Steps

1. **Prepare files**:
   ```bash
   cp src/static/index.html public/
   ```

2. **Deploy to Vercel**:
   ```bash
   vercel --prod --yes
   ```

3. **Verify deployment**:
   - Check the deployment URL
   - Test all features
   - Verify environment variables

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# GitHub Token for AI features (required)
GITHUB_TOKEN=your_github_personal_access_token_here

# Database Configuration (optional)
# Leave empty for SQLite, or set PostgreSQL URL
DATABASE_URL=postgresql://username:password@host:port/database

# Flask Configuration
FLASK_CONFIG=development  # or production
SECRET_KEY=your-secret-key-here
```

### Available Templates

The application includes 8 pre-built templates:

1. **Meeting Notes** - Attendees, agenda, notes, action items
2. **Daily Journal** - Morning reflection, gratitude, goals, evening review  
3. **To-Do List** - Organized task management with checkboxes
4. **Project Planning** - Goals, timeline, resources, milestones
5. **Study Notes** - Subject, topics, key concepts, questions
6. **Book Notes** - Title, author, summary, key takeaways, quotes
7. **Recipe** - Ingredients, instructions, prep/cook time, servings
8. **Travel Itinerary** - Destination, dates, accommodations, activities

### AI Models Configuration

The application uses OpenAI GPT-4.1-mini via GitHub Models:

- **Endpoint**: `https://models.github.ai/inference`
- **Model**: `openai/gpt-4.1-mini`
- **Timeout**: 30 seconds
- **Features**: Translation and smart notes generation

## 📱 Browser Compatibility

Tested and working on:
- ✅ Chrome/Chromium (recommended)
- ✅ Firefox
- ✅ Safari (desktop and iOS)
- ✅ Edge
- ✅ Mobile browsers (Chrome Mobile, Safari iOS)

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support & Troubleshooting

### Common Issues

**AI features not working:**
- Ensure `GITHUB_TOKEN` is set in environment variables
- Verify token has GitHub Models permission
- Check token is properly formatted (no newlines)

**Database issues on Vercel:**
- Vercel uses in-memory SQLite (data resets on cold starts)
- For persistent data, configure `DATABASE_URL` with PostgreSQL

**Share links return 404:**
- Verify Vercel routes are properly configured
- Check that `/shared/` routes point to API

**Translation errors:**
- Confirm GitHub Models API access is enabled
- Verify model name is `openai/gpt-4.1-mini`
- Check network connectivity

### Getting Help

1. Check the browser console for error messages
2. Review the [writeup.md](writeup.md) for detailed documentation
3. Verify all environment variables are set
4. Check Vercel deployment logs
5. Open an issue on GitHub with detailed error information

## 📚 Documentation

- **[writeup.md](writeup.md)** - Comprehensive project documentation
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Implementation details
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deployment guide
- **[DEBUGGING_GUIDE.md](DEBUGGING_GUIDE.md)** - Debugging tips

## 🏆 Project Information

- **Course**: COMP5241 - Software Engineering
- **Semester**: 2025 Semester 1
- **Repository**: [note-taking-app-Gary-8606](https://github.com/COMP5241-2526Sem1/note-taking-app-Gary-8606)
- **Live Demo**: https://note-9m1taqljx-gary-wongs-projects-618f39d1.vercel.app

## 🎯 Key Achievements

### Features Implemented
✅ Full CRUD operations with persistent storage  
✅ Drag-and-drop note reordering  
✅ AI-powered translation (40+ languages)  
✅ Smart notes generation from quick input  
✅ 8 professional note templates  
✅ Advanced search with multiple filters  
✅ Public note sharing with password protection  
✅ Share link expiration and revocation  
✅ View count tracking for shared notes  
✅ Responsive design for all devices  

### Technical Accomplishments
✅ Serverless deployment on Vercel  
✅ RESTful API design  
✅ Integration with OpenAI GPT-4.1-mini  
✅ Secure token management  
✅ In-memory database for serverless environment  
✅ HTML5 Drag and Drop API implementation  
✅ Modal-based UI for enhanced UX  
✅ PostgreSQL/Supabase support  

### Challenges Overcome
✅ Vercel read-only filesystem → In-memory SQLite solution  
✅ GitHub token authentication → Proper token setup and permissions  
✅ JavaScript event listener errors → Safe binding pattern  
✅ Share link routing → Custom Vercel routes configuration  
✅ Translation API connection → Direct HTTP requests implementation  

## 🎯 Future Enhancements

Potential improvements for future versions:

### User Management
- [ ] Multi-user authentication system
- [ ] User registration and login
- [ ] Personal workspaces
- [ ] Profile customization

### Rich Text Features
- [ ] Markdown support
- [ ] WYSIWYG editor
- [ ] Code syntax highlighting
- [ ] Image uploads
- [ ] File attachments

### Collaboration
- [ ] Real-time collaborative editing
- [ ] Comments and annotations
- [ ] Share with edit permissions
- [ ] Version history

### Organization
- [ ] Folders and categories
- [ ] Tag-based organization
- [ ] Favorites and pinning
- [ ] Archive functionality
- [ ] Bulk operations

### Export & Import
- [ ] PDF export
- [ ] Markdown export
- [ ] Import from Evernote/OneNote
- [ ] Backup and restore

### Mobile
- [ ] Native mobile apps (iOS/Android)
- [ ] Offline support
- [ ] Push notifications
- [ ] Widget support

### Advanced AI
- [ ] Summary generation
- [ ] Sentiment analysis
- [ ] Auto-tagging
- [ ] Related note suggestions
- [ ] Voice-to-text notes

---

**Built with ❤️ using Flask, OpenAI GPT-4.1-mini, and Vercel**

*Last Updated: October 26, 2025*


