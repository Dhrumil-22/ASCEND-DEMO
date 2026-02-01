import unittest
from app import create_app, db
from app.models import User, Student
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(name='Susan', email='susan@example.com', role='student')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_student_relationship(self):
        u = User(name='John', email='john@example.com', role='student')
        db.session.add(u)
        db.session.commit()
        s = Student(user_id=u.id, batch_year=2024, branch='CS')
        db.session.add(s)
        db.session.commit()
        
        self.assertTrue(u.student_profile is not None)
        self.assertEqual(u.student_profile.batch_year, 2024)
