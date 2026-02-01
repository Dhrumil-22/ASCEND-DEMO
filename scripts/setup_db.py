from app import create_app, db
from app.models import User, Student, Alumni, Company, Question, Response

app = create_app()

with app.app_context():
    db.drop_all() # Clean slate for development
    db.create_all()
    print("Database tables created successfully!")

    # 1. Create Companies
    companies = [
        Company(name='Google', industry='Technology'),
        Company(name='Odoo', industry='ERP Software'),
        Company(name='TCS', industry='IT Services'),
        Company(name='Amazon', industry='E-commerce'),
        Company(name='Microsoft', industry='Technology')
    ]
    db.session.add_all(companies)
    db.session.commit()
    print("Companies added.")

    # 2. Create Student (Rohan)
    student_user = User(name='Rohan Shah', email='rohan@college.edu', role='student')
    student_user.set_password('password123')
    db.session.add(student_user)
    db.session.commit()

    student_profile = Student(user_id=student_user.id, batch_year=2026, branch='Computer Engineering', skills='Python, Java')
    db.session.add(student_profile)
    
    # 3. Create Mentors
    # Mentor 1: Rahul at Odoo
    mentor1_user = User(name='Rahul Patel', email='rahul@alumni.edu', role='alumni')
    mentor1_user.set_password('password123')
    db.session.add(mentor1_user)
    db.session.commit()
    
    odoo = Company.query.filter_by(name='Odoo').first()
    mentor1_profile = Alumni(user_id=mentor1_user.id, current_company_id=odoo.id, current_role='Senior SDE', trust_score=94, is_verified=True)
    db.session.add(mentor1_profile)

    # Mentor 2: Sarah at Google
    mentor2_user = User(name='Sarah Lee', email='sarah@alumni.edu', role='alumni')
    mentor2_user.set_password('password123')
    db.session.add(mentor2_user)
    db.session.commit()

    google = Company.query.filter_by(name='Google').first()
    mentor2_profile = Alumni(user_id=mentor2_user.id, current_company_id=google.id, current_role='Product Manager', trust_score=98, is_verified=True)
    db.session.add(mentor2_profile)

    db.session.commit()
    print("Users & Mentors added.")

    # 4. Create Demo Questions & Answers
    q1 = Question(
        student_id=student_profile.id,
        company_id=odoo.id,
        title='How to prepare for Odoo technical round?',
        body='I have an interview coming up in 2 weeks. What topics should I focus on?',
        category='Interview Prep',
        status='answered'
    )
    db.session.add(q1)
    db.session.commit()

    r1 = Response(
        question_id=q1.id,
        mentor_id=mentor1_profile.id,
        body='Focus on Python OOPS concepts, PostgreSQL queries, and Javascript basics. Also read about Odoo framework basics.'
    )
    db.session.add(r1)

    q2 = Question(
        student_id=student_profile.id,
        company_id=google.id,
        title='Referral process for freshers?',
        body='Is it possible to get a referral for a new grad role?',
        category='Referral',
        status='pending'
    )
    db.session.add(q2)

    db.session.commit()
    print("Demo Questions added.")

    # 5. Create Admin
    admin_user = User(name='Admin User', email='admin@ascend.edu', role='admin')
    admin_user.set_password('admin123')
    db.session.add(admin_user)
    db.session.commit()
    print("Admin added.")

    print("Setup Complete! Login with rohan@college.edu / password123 or admin@ascend.edu / admin123")
