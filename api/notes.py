"""
Notes API endpoints for Vercel deployment
"""
import os
import sys

# Add the parent directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from flask import Flask
from src.main import create_app

app = create_app('production')

# This will handle all /api/notes/* routes
if __name__ == "__main__":
    app.run(debug=False)