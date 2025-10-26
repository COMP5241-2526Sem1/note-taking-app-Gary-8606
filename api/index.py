import os
import sys

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.main import create_app

# Create the Flask app instance for Vercel
app = create_app('production')

# This is the WSGI application that Vercel will use
def handler(request, context):
    return app(request.environ, context)

# For local testing
if __name__ == "__main__":
    app.run(debug=False)