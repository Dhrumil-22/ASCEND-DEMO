# ASCEND - Alumni-Student Career ENgagement Dashboard

> **A Flask-based mentorship platform connecting students with alumni for company-specific career guidance**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Project Overview

ASCEND is a web-based mentorship platform that enables students to:
- 🏢 **Discover alumni** working at target companies (Google, Amazon, TCS, etc.)
- ❓ **Ask structured questions** about interviews, career paths, and company culture
- 🎯 **Get matched** with relevant mentors using intelligent algorithms
- 📊 **Track outcomes** through a trust-based feedback system
- 🤝 **Request referrals** from verified alumni

### Key Features
- Company-based mentor discovery
- Asynchronous Q&A system (no real-time chat)
- Fair FIFO queue management for mentors
- Outcome-based trust scoring
- Admin verification and moderation
- Knowledge base of answered questions

## 🏗️ Project Structure

```
ASCEND/
├── app/                      # Main application package
│   ├── __init__.py          # App factory
│   ├── models.py            # Database models
│   ├── routes/              # Route blueprints
│   │   ├── auth.py         # Authentication routes
│   │   ├── main.py         # Main app routes
│   │   └── admin.py        # Admin panel routes
│   ├── templates/           # Jinja2 templates
│   │   ├── auth/           # Login, register
│   │   ├── main/           # Dashboards, company list
│   │   ├── questions/      # Ask, view questions
│   │   └── admin/          # Admin panel
│   └── static/              # CSS, JS, images
│       └── css/
├── tests/                   # Test suite
│   ├── test_basics.py
│   ├── test_models.py
│   └── test_routes.py
├── scripts/                 # Utility scripts
│   ├── setup_db.py         # Database seeding
│   ├── extract_pdf.py      # PDF extraction utilities
│   └── make_pdfs.py        # PDF generation
├── extras/                  # Documentation & resources
│   ├── pdfs/               # Project PDFs
│   ├── project_docs/       # Text documentation
│   └── DOCS/               # Design docs, wireframes
├── migrations/              # Database migrations
├── instance/                # Instance-specific files (gitignored)
├── config.py               # Configuration
├── run.py                  # Application entry point
├── requirements.txt        # Python dependencies
└── .gitignore             # Git ignore rules

```

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Dhrumil-22/ASCEND-DEMO.git
   cd ASCEND
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up database**
   ```bash
   # Initialize migrations
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   
   # Seed demo data
   python scripts/setup_db.py
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

6. **Access the application**
   - Open browser: `http://localhost:5000`
   - Student login: `rohan@college.edu` / `password123`
   - Admin login: `admin@ascend.edu` / `admin123`

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_models.py
```

## 🛠️ Technology Stack

### Backend
- **Framework:** Flask 2.3+
- **ORM:** SQLAlchemy
- **Authentication:** Flask-Login
- **Migrations:** Flask-Migrate
- **Forms:** Flask-WTF

### Frontend
- **Templates:** Jinja2
- **Styling:** Bootstrap 5 + Custom CSS
- **JavaScript:** Vanilla JS (ES6+)

### Database
- **Development:** SQLite
- **Production:** PostgreSQL (recommended)

### Data Structures & Algorithms
- FIFO Queue for mentor question distribution
- Priority Queue for urgent questions
- HashMap for company-to-mentor mapping
- Sorting algorithms for mentor ranking
- String similarity for duplicate detection

## 📊 Database Models

- **User** - Base user (student/alumni/admin)
- **Student** - Student profile with skills, batch, branch
- **Alumni** - Alumni profile with company, role, trust score
- **Company** - Company master data
- **Question** - Student questions with category, urgency
- **Response** - Mentor answers
- **Feedback** - Outcome-based feedback (planned)
- **Referral** - Referral requests (planned)

## 🔐 Environment Variables

Create a `.env` file in the root directory:

```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///instance/ascend.db
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

## 📈 Development Status

**Current Completion: 100%** ✅

✅ **Completed:**
- Authentication system (login, register, role-based access)
- Database models and relationships (User, Student, Alumni, Company, Question, Response, Feedback, Referral)
- Student dashboard with statistics and recent activity
- Company listing with search and pagination
- Question submission with categories and urgency levels
- Admin panel with user verification and moderation
- Knowledge base with answered questions
- **Mentor dashboard with trust score and activity tracking**
- **Mentor answer submission with markdown support**
- **FIFO queue implementation with priority handling**
- **Intelligent mentor matching algorithm with load balancing**
- **Trust score calculation based on feedback outcomes**
- **Outcome-based feedback system (interviews, referrals, helpfulness)**
- **Referral request and approval system**
- **Responsive UI with modern CSS and animations**
- **JavaScript utilities (form validation, auto-save, toast notifications)**

### Key Algorithms Implemented:
- **FIFO Queue**: Using Python `deque` for fair question distribution
- **Priority Queue**: Using `heapq` for urgent question handling
- **Mentor Matching**: Multi-criteria scoring algorithm with fallback strategies
- **Trust Score**: Formula-based calculation with outcome weighting
- **Load Balancing**: Round-robin assignment with mentor availability tracking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- **Dhrumil** - *Initial work* - [Dhrumil-22](https://github.com/Dhrumil-22)

## 🙏 Acknowledgments

- LJIET College for project guidance
- Flask documentation and community
- Bootstrap for UI components

## 📞 Contact

For questions or support, please contact:
- Email: [your-email@example.com]
- GitHub: [@Dhrumil-22](https://github.com/Dhrumil-22)

---

**Note:** This project is part of an academic assignment demonstrating practical application of Data Structures and Algorithms in a real-world web application.
