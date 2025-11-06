from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, UTC

db = SQLAlchemy()

# Base Model Definitions
class Theme(db.Model):
    __tablename__ = 'theme'
    id = db.Column(db.Integer, primary_key=True)
    # ADDED INDEX for fast theme lookup/sorting (O(log N) via B-Tree)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True) 
    ideas = db.relationship('ProjectIdea', backref='theme', lazy=True, cascade="all, delete-orphan")
    apis = db.relationship('ApiRecommendation', backref='theme', lazy=True, cascade="all, delete-orphan")
    
    __table_args__ = {'extend_existing': True}

class ProjectIdea(db.Model):
    __tablename__ = 'project_idea'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(50), nullable=False, default='Intermediate')
    # ADDED INDEX on ForeignKey
    theme_id = db.Column(db.Integer, db.ForeignKey('theme.id'), nullable=False, index=True)
    
    # Relationship name 'kit' is used correctly in app.py
    kit = db.relationship('HackathonKit', back_populates='idea', uselist=False, cascade="all, delete-orphan") 

    __table_args__ = {'extend_existing': True}

class TechStack(db.Model):
    __tablename__ = 'tech_stack'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    frontend = db.Column(db.String(100))
    backend = db.Column(db.String(100))
    database = db.Column(db.String(100))
    
    __table_args__ = {'extend_existing': True}

class ApiRecommendation(db.Model):
    __tablename__ = 'api_recommendation'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(255))
    description = db.Column(db.Text)
    theme_id = db.Column(db.Integer, db.ForeignKey('theme.id'), nullable=False)
    
    __table_args__ = {'extend_existing': True}

class PitchTip(db.Model):
    __tablename__ = 'pitch_tip'
    id = db.Column(db.Integer, primary_key=True)
    tip = db.Column(db.Text, nullable=False)
    
    __table_args__ = {'extend_existing': True}

# links everything together
class HackathonKit(db.Model):
    __tablename__ = 'hackathon_kit'
    id = db.Column(db.Integer, primary_key=True)
    
    idea_id = db.Column(db.Integer, db.ForeignKey('project_idea.id'), unique=True, nullable=False)
    stack_id = db.Column(db.Integer, db.ForeignKey('tech_stack.id'), nullable=True)
    api_id = db.Column(db.Integer, db.ForeignKey('api_recommendation.id'), nullable=True)
    tip_id = db.Column(db.Integer, db.ForeignKey('pitch_tip.id'), nullable=True)

    idea = db.relationship('ProjectIdea', back_populates='kit', uselist=False)
    stack = db.relationship('TechStack')
    api = db.relationship('ApiRecommendation')
    tip = db.relationship('PitchTip')
    
    __table_args__ = {'extend_existing': True}
    
class ChatRoom(db.Model):
    __tablename__ = 'chat_room'
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(100), unique=True, nullable=False)
    secret_code = db.Column(db.String(20), unique=True, nullable=False)
    # CORRECTED: Use timezone-aware datetime.now(UTC)
    created_at = db.Column(db.DateTime, default=datetime.now(UTC))

    __table_args__ = {'extend_existing': True}

class ChatMessage(db.Model):
    __tablename__ = 'chat_message'
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.String(100), nullable=False, index=True) 
    username = db.Column(db.String(100), nullable=False, index=True)
    message = db.Column(db.Text, nullable=False)
    # CORRECTED: Use timezone-aware datetime.now(UTC)
    timestamp = db.Column(db.DateTime, default=datetime.now(UTC), index=True)
    
    __table_args__ = {'extend_existing': True}