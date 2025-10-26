import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, render_template_string, request
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.note import note_bp
from src.models.note import Note
from src.models.share import SharedNote
from src.config import config

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG') or 'default'
    
    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
    
    # Load configuration
    app.config.from_object(config[config_name])
    app.config['SQLALCHEMY_DATABASE_URI'] = config[config_name].get_database_uri()
    
    # Initialize configuration
    config[config_name].init_app(app)

    # Enable CORS for all routes
    CORS(app)

    # Initialize database
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(note_bp, url_prefix='/api')
    
    # Create tables
    with app.app_context():
        try:
            db.create_all()
            print(f"✅ Database tables created successfully using: {app.config['SQLALCHEMY_DATABASE_URI'][:50]}...")
            
            # Create default user if it doesn't exist
            from src.models.user import User
            default_user = User.query.filter_by(id=1).first()
            if not default_user:
                default_user = User(username='default_user', email='user@example.com')
                default_user.id = 1  # Explicitly set ID to 1
                db.session.add(default_user)
                db.session.commit()
                print("✅ Default user created successfully")
                
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            print("💡 Make sure your DATABASE_URL is correct or remove it to use SQLite")
    
    # Add shared note route
    @app.route('/shared/<share_token>')
    def shared_note_view(share_token):
        """Render a shared note view (HTML page)"""
        try:
            shared_note = SharedNote.query.filter_by(share_token=share_token).first()
            if not shared_note:
                return render_template_string("""
                <html>
                    <head><title>Note Not Found</title></head>
                    <body style="font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px;">
                        <h1>📄 Note Not Found</h1>
                        <p>The shared note you're looking for doesn't exist.</p>
                    </body>
                </html>
                """), 404
            
            if not shared_note.is_accessible():
                error_msg = "This shared link has expired" if shared_note.is_expired() else "This shared link is no longer active"
                return render_template_string(f"""
                <html>
                    <head><title>Access Denied</title></head>
                    <body style="font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px;">
                        <h1>🚫 Access Denied</h1>
                        <p>{error_msg}</p>
                    </body>
                </html>
                """), 403
            
            # Handle password protection
            if shared_note.password_hash:
                password = request.args.get('password')
                if not password or not shared_note.check_password(password):
                    return render_template_string("""
                    <html>
                        <head><title>Password Required</title></head>
                        <body style="font-family: Arial, sans-serif; max-width: 500px; margin: 100px auto; padding: 20px;">
                            <h2>🔒 Password Required</h2>
                            <form method="GET">
                                <div style="margin: 20px 0;">
                                    <input type="password" name="password" placeholder="Enter password" required
                                           style="padding: 10px; font-size: 16px; width: 100%; border: 2px solid #ddd; border-radius: 5px;">
                                </div>
                                <button type="submit" style="padding: 10px 20px; font-size: 16px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer;">
                                    Access Note
                                </button>
                            </form>
                        </body>
                    </html>
                    """), 401
            
            # Increment view count
            shared_note.increment_view_count()
            
            # Render the shared note
            return render_template_string("""
            <html>
                <head>
                    <title>{{ title }} - Shared Note</title>
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                    <style>
                        body { 
                            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                            max-width: 800px; 
                            margin: 0 auto; 
                            padding: 20px;
                            line-height: 1.6;
                            background: #f8f9fa;
                        }
                        .container {
                            background: white;
                            padding: 30px;
                            border-radius: 10px;
                            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                        }
                        h1 { 
                            color: #333; 
                            border-bottom: 2px solid #007bff; 
                            padding-bottom: 10px; 
                        }
                        .content { 
                            white-space: pre-wrap; 
                            background: #f8f9fa; 
                            padding: 20px; 
                            border-radius: 5px; 
                            border-left: 4px solid #007bff;
                            margin: 20px 0;
                        }
                        .meta { 
                            font-size: 14px; 
                            color: #666; 
                            margin-top: 30px; 
                            padding-top: 20px;
                            border-top: 1px solid #eee;
                        }
                        .badge {
                            background: #007bff;
                            color: white;
                            padding: 4px 8px;
                            border-radius: 12px;
                            font-size: 12px;
                        }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>📄 {{ title }}</h1>
                        <div class="content">{{ content }}</div>
                        <div class="meta">
                            <span class="badge">👁️ {{ view_count }} views</span> •
                            Shared on {{ created_date }}
                        </div>
                    </div>
                </body>
            </html>
            """, 
                title=shared_note.note.title,
                content=shared_note.note.content,
                view_count=shared_note.view_count,
                created_date=shared_note.created_at.strftime('%B %d, %Y')
            )
            
        except Exception as e:
            return render_template_string(f"""
            <html>
                <head><title>Error</title></head>
                <body style="font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px;">
                    <h1>❌ Error</h1>
                    <p>An error occurred: {str(e)}</p>
                </body>
            </html>
            """), 500
    
    return app

def register_routes(app):
    """Register routes for serving static files in development"""
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        static_folder_path = app.static_folder
        if static_folder_path is None:
                return "Static folder not configured", 404

        if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
            return send_from_directory(static_folder_path, path)
        else:
            index_path = os.path.join(static_folder_path, 'index.html')
            if os.path.exists(index_path):
                return send_from_directory(static_folder_path, 'index.html')
            else:
                return "index.html not found", 404

# Create the app instance for local development
app = create_app()

# Only register static file routes in development
if os.environ.get('FLASK_CONFIG', 'development') == 'development':
    register_routes(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
