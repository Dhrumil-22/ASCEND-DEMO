from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), nullable=False) # 'student', 'alumni', 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    student_profile = db.relationship('Student', backref='user', uselist=False)
    alumni_profile = db.relationship('Alumni', backref='user', uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    batch_year = db.Column(db.Integer)
    branch = db.Column(db.String(50))
    skills = db.Column(db.String(200)) # Simple comma-separated string for MPV
    questions = db.relationship('Question', backref='student', lazy='dynamic')

class Alumni(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    current_company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    current_role = db.Column(db.String(100))
    trust_score = db.Column(db.Integer, default=50)
    is_accepting_questions = db.Column(db.Boolean, default=True)
    responses = db.relationship('Response', backref='mentor', lazy='dynamic')

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    industry = db.Column(db.String(50))
    logo_url = db.Column(db.String(200)) # Placeholder or URL
    alumni = db.relationship('Alumni', backref='company', lazy='dynamic')
    questions = db.relationship('Question', backref='target_company', lazy='dynamic')

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50)) # Interview, Roadmap, etc.
    urgency = db.Column(db.String(20)) # Normal, High
    status = db.Column(db.String(20), default='pending') # pending, answered
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    responses = db.relationship('Response', backref='question', lazy='dynamic')

    # Optional: Targeted mentor
    target_mentor_id = db.Column(db.Integer, db.ForeignKey('alumni.id'), nullable=True)

class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    mentor_id = db.Column(db.Integer, db.ForeignKey('alumni.id'))
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    helpful_count = db.Column(db.Integer, default=0)
