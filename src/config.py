import os
from urllib.parse import urlparse

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'asdf#FGSgvasgf$5$WGT'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    
    @staticmethod
    def get_database_uri():
        # Use PostgreSQL if DATABASE_URL is provided, otherwise SQLite
        database_url = os.environ.get('DATABASE_URL')
        if database_url:
            # Handle Supabase URL format
            if database_url.startswith('postgresql://'):
                return database_url
            return database_url
        else:
            # Fallback to SQLite for local development
            ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
            DB_PATH = os.path.join(ROOT_DIR, 'database', 'app.db')
            os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
            return f"sqlite:///{DB_PATH}"

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    
    @staticmethod
    def get_database_uri():
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            # For Vercel deployment, use in-memory SQLite (filesystem is read-only)
            print("⚠️ No DATABASE_URL found, using in-memory SQLite for serverless deployment")
            return 'sqlite:///:memory:'
        
        # Handle Heroku/Railway postgres URL format (postgres:// -> postgresql://)
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        
        return database_url

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    
    @staticmethod
    def get_database_uri():
        return 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}