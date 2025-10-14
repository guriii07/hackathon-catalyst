# models.py
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Theme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    ideas = db.relationship('ProjectIdea', backref='theme', lazy=True, cascade="all, delete-orphan")
    apis = db.relationship('ApiRecommendation', backref='theme', lazy=True, cascade="all, delete-orphan")
    
    __table_args__ = {'extend_existing': True}

class ProjectIdea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(20), nullable=False, default='Intermediate')
    theme_id = db.Column(db.Integer, db.ForeignKey('theme.id'), nullable=False)
    
    # Relationship to the HackathonKit
    kit = db.relationship('HackathonKit', backref='project_idea_kit', uselist=False, cascade="all, delete-orphan")

    __table_args__ = {'extend_existing': True}

class TechStack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    frontend = db.Column(db.String(100))
    backend = db.Column(db.String(100))
    database = db.Column(db.String(100))
    
    __table_args__ = {'extend_existing': True}

class ApiRecommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(200))
    description = db.Column(db.Text)
    theme_id = db.Column(db.Integer, db.ForeignKey('theme.id'), nullable=False)
    
    __table_args__ = {'extend_existing': True}

class PitchTip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tip = db.Column(db.Text, nullable=False)
    
    __table_args__ = {'extend_existing': True}

# The new model that links everything together
class HackathonKit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    idea_id = db.Column(db.Integer, db.ForeignKey('project_idea.id'), unique=True, nullable=False)
    stack_id = db.Column(db.Integer, db.ForeignKey('tech_stack.id'), nullable=True)
    api_id = db.Column(db.Integer, db.ForeignKey('api_recommendation.id'), nullable=True)
    tip_id = db.Column(db.Integer, db.ForeignKey('pitch_tip.id'), nullable=True)

    idea = db.relationship('ProjectIdea', backref='kit_link', uselist=False)
    stack = db.relationship('TechStack')
    api = db.relationship('ApiRecommendation')
    tip = db.relationship('PitchTip')
    
    __table_args__ = {'extend_existing': True}
    
class ChatRoom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(50), unique=True, nullable=False)
    secret_code = db.Column(db.String(20), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    __table_args__ = {'extend_existing': True}

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    __table_args__ = {'extend_existing': True}