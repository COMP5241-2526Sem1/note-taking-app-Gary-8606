import os
import sys

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Set environment variable for production
os.environ['FLASK_CONFIG'] = 'production'

try:
    from src.main import create_app
    # Create the Flask app instance for Vercel
    app = create_app('production')
    
    # Ensure all routes are properly registered
    print(f"✅ Flask app created with {len(app.url_map._rules)} routes")
    for rule in app.url_map.iter_rules():
        print(f"  - {rule.rule} -> {rule.endpoint}")
        
except Exception as e:
    print(f"❌ Error creating Flask app: {e}")
    import traceback
    traceback.print_exc()
    
    # Fallback minimal app
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/')
    def hello():
        return jsonify({
            'message': 'Note Taking App API - Fallback Mode', 
            'status': 'running', 
            'error': str(e),
            'mode': 'fallback'
        })
    
    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy', 'service': 'note-taking-app-fallback'})

# For Vercel serverless functions, we need to export the app directly
# Vercel will handle the WSGI interface automatically