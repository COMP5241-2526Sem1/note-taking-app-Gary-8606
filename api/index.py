import os
import sys

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.main import create_app

# Create the Flask app instance for Vercel
app = create_app('production')

# For Vercel serverless functions, we need to export the app directly
# Vercel will handle the WSGI interface automatically