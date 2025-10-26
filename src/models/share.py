"""
Shared Note model for public note sharing functionality
"""

import secrets
from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from src.models.note import db

class SharedNote(db.Model):
    """Model for shared notes with public access"""
    __tablename__ = 'shared_notes'
    
    id = Column(Integer, primary_key=True)
    note_id = Column(Integer, ForeignKey('notes.id', ondelete='CASCADE'), nullable=False)
    share_token = Column(String(32), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=True)  # Optional password protection
    expires_at = Column(DateTime, nullable=True)  # Optional expiration
    is_active = Column(Boolean, default=True, nullable=False)
    view_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    note = relationship("Note", backref="shared_links")
    
    def __init__(self, note_id, password=None, expires_days=None):
        self.note_id = note_id
        self.share_token = secrets.token_urlsafe(24)  # Generate unique token
        
        if password:
            from werkzeug.security import generate_password_hash
            self.password_hash = generate_password_hash(password)
            
        if expires_days:
            self.expires_at = datetime.utcnow() + timedelta(days=expires_days)
    
    def check_password(self, password):
        """Check if provided password matches the hash"""
        if not self.password_hash:
            return True  # No password required
        
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)
    
    def is_expired(self):
        """Check if the shared link has expired"""
        if not self.expires_at:
            return False  # No expiration set
        return datetime.utcnow() > self.expires_at
    
    def is_accessible(self):
        """Check if the shared link is accessible"""
        return self.is_active and not self.is_expired()
    
    def increment_view_count(self):
        """Increment the view count"""
        self.view_count += 1
        db.session.commit()
    
    def to_dict(self, include_sensitive=False):
        """Convert to dictionary for JSON serialization"""
        data = {
            'id': self.id,
            'share_token': self.share_token,
            'has_password': bool(self.password_hash),
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'is_active': self.is_active,
            'view_count': self.view_count,
            'created_at': self.created_at.isoformat(),
            'is_expired': self.is_expired()
        }
        
        if include_sensitive and hasattr(self, 'note'):
            data['note'] = {
                'id': self.note.id,
                'title': self.note.title,
                'content': self.note.content,
                'created_at': self.note.created_at.isoformat(),
                'updated_at': self.note.updated_at.isoformat()
            }
            
        return data

# The table will be created by the main app initialization