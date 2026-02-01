import unittest
from app import create_app, db
from app.models import User, Student
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False # Disable CSRF for testing

class RouteTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # Create user
        u = User(name='Test User', email='test@example.com', role='student')
        u.set_password('password')
        db.session.add(u)
        db.session.commit()
        
        s = Student(user_id=u.id, batch_year=2024, branch='CS')
        db.session.add(s)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_login_logout(self):
        response = self.client.get('/auth/login')
        self.assertEqual(response.status_code, 200)

        # Login
        response = self.client.post('/auth/login', data=dict(
            email='test@example.com',
            password='password'
        ), follow_redirects=True)
        self.assertIn(b'Welcome', response.data) # Assuming 'Welcome' is in dashboard

        # Logout
        response = self.client.get('/auth/logout', follow_redirects=True)
        self.assertIn(b'Login', response.data)

    def test_dashboard_access_denied_anonymous(self):
        response = self.client.get('/student_dashboard', follow_redirects=True)
        self.assertIn(b'Login', response.data) # Should redirect to login
