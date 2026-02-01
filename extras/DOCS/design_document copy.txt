# ASCEND - Design Document
## Alumni-Student Career ENgagement Dashboard

> [!IMPORTANT]
> **Project Type:** Web-based Mentorship Platform  
> **Tech Stack:** Python (Flask), PostgreSQL, Bootstrap, HTML/CSS/JavaScript  
> **Academic Focus:** Practical application of Data Structures & Algorithms

---

## 1. Executive Summary

### 1.1 Product Vision
ASCEND is a college-specific platform that revolutionizes career guidance by connecting students with alumni working at their target companies. Unlike generic mentorship platforms, ASCEND enables **company-based discovery** where students can find and learn from alumni at companies like Google, Odoo, TCS, etc.

### 1.2 Problem Statement
Current challenges in student-alumni mentorship:
- **No structured access** to discover which alumni work at specific companies
- **Low response rates** on LinkedIn (<10%) and chaotic WhatsApp groups
- **Generic advice** not tailored to specific companies
- **Mentor burnout** from repetitive questions and spam
- **No accountability** to verify advice quality

### 1.3 Solution Overview
ASCEND addresses these through:
1. **Company-Based Discovery** - Search mentors by target company
2. **Asynchronous Q&A** - Structured questions, not real-time chat
3. **Fair Queue System** - FIFO distribution prevents overload
4. **Trust Scoring** - Outcome-based feedback on advice effectiveness
5. **Intelligent Matching** - Algorithm matches best mentors
6. **Referral Workflow** - Formal pipeline for job referrals
7. **Knowledge Base** - Searchable archive reduces duplicate questions

### 1.4 Key Differentiators

| Aspect | Traditional Platforms | **ASCEND** |
|--------|----------------------|------------|
| Discovery | By skills/industry | **By specific company** |
| Communication | Real-time chat | **Async structured Q&A** |
| Network | Global/open | **College-specific (trusted)** |
| Quality Control | Ratings only | **Outcome-based trust scores** |
| Mentor Load | Uncontrolled | **Queue-managed (DSA-based)** |
| Company Intel | Generic | **Aggregated insider insights** |

---

## 2. Technology Stack

### Backend
- **Language:** Python 3.10+
- **Framework:** Flask 2.3+
- **ORM:** SQLAlchemy 2.0+
- **Authentication:** Flask-Login
- **Rate Limiting:** Flask-Limiter
- **Email:** Flask-Mail

### Frontend
- **Structure:** HTML5
- **Styling:** CSS3 + Bootstrap 5
- **Interactivity:** JavaScript (ES6+)
- **Templates:** Jinja2

### Database
- **Primary:** PostgreSQL 14+
- **Alternative:** MySQL (development only)
- **Caching:** Redis (optional, for sessions)

### Deployment
- **WSGI Server:** Gunicorn
- **Reverse Proxy:** Nginx
- **Containerization:** Docker (optional)
- **Hosting:** Railway / Render / Heroku (dev), AWS/GCP (production)

### Development Tools
- **Version Control:** Git + GitHub
- **Linting:** Pylint, Flake8
- **Formatting:** Black
- **Testing:** pytest

---

## 3. System Architecture

### 3.1 Architecture Pattern
**Model-View-Controller (MVC) / Layered Architecture**

```
┌────────────────────────────────────────────┐
│      PRESENTATION LAYER (View)            │
│  - HTML Templates (Jinja2)                │
│  - CSS (Bootstrap + Custom)               │
│  - JavaScript (Client-side)               │
└───────────────┬────────────────────────────┘
                │ HTTP Requests/Responses
┌───────────────▼────────────────────────────┐
│    APPLICATION LAYER (Controller)         │
│  Flask Application                        │
│  ┌─────────────────────────────────────┐  │
│  │ Route Blueprints:                   │  │
│  │  - auth_bp (Authentication)         │  │
│  │  - company_bp (Companies)           │  │
│  │  - question_bp (Q&A System)         │  │
│  │  - mentor_bp (Mentor Features)      │  │
│  │  - admin_bp (Admin Panel)           │  │
│  │  - api_bp (REST API)                │  │
│  └─────────────────────────────────────┘  │
│  ┌─────────────────────────────────────┐  │
│  │ Middleware:                         │  │
│  │  - Authentication (Flask-Login)     │  │
│  │  - Authorization (RBAC)             │  │
│  │  - Rate Limiting                    │  │
│  │  - Error Handling                   │  │
│  └─────────────────────────────────────┘  │
└───────────────┬────────────────────────────┘
                │ Function Calls
┌───────────────▼────────────────────────────┐
│    BUSINESS LOGIC LAYER (Services)        │
│  - QuestionQueueService (FIFO Queue)      │
│  - MentorMatchingService (HashMap)        │
│  - TrustScoreService                      │
│  - ReferralService                        │
│  - NotificationService                    │
│  - CompanyIntelligenceService             │
└───────────────┬────────────────────────────┘
                │ ORM Operations
┌───────────────▼────────────────────────────┐
│      DATA ACCESS LAYER (Model)            │
│  SQLAlchemy ORM                           │
│  Models: Student, Alumni, Company,        │
│  Question, Response, TrustScore, etc.     │
└───────────────┬────────────────────────────┘
                │ SQL Queries
┌───────────────▼────────────────────────────┐
│        DATABASE (PostgreSQL)              │
│  Tables: users, companies, questions,     │
│  work_history, responses, trust_scores    │
└────────────────────────────────────────────┘
```

### 3.2 Data Structures & Algorithms Integration

> [!NOTE]
> DSA concepts are integrated into functional workflows (not standalone demos)

| DSA Concept | Implementation | Purpose | Complexity |
|-------------|----------------|---------|------------|
| **Queue (FIFO)** | `QuestionQueueService` | Fair question distribution to mentors | Enqueue: O(1), Dequeue: O(1) |
| **Priority Queue** | `UrgentQueueService` | Handle urgent/deadline-based questions | Insert: O(log n), Extract: O(log n) |
| **Stack (LIFO)** | `AdminModerationService` | Undo moderation actions | Push: O(1), Pop: O(1) |
| **HashMap** | `MentorMatchingService` | Company-to-mentors mapping | Lookup: O(1) |
| **Sorting (Merge Sort)** | `MentorMatchingService` | Rank mentors by match score | O(n log n) |
| **String Similarity** | `DuplicateDetection` | Detect duplicate questions (TF-IDF) | O(n×m) |

---

## 4. Core Features & Functionality

### 4.1 User Roles

#### 1. **Junior Student (Primary User)**
- **Can:** Submit questions, search companies, view mentor profiles, request referrals
- **Cannot:** Answer questions, access admin panel
- **Profile includes:** Roll number, year, branch, skills, CGPA, target companies

#### 2. **Alumni/Senior Mentor**
- **Can:** Answer questions, set availability, manage queue, approve/decline referrals
- **Cannot:** Submit questions (except to other alumni)
- **Profile includes:** Current company, role, work history, expertise tags, trust score

#### 3. **Administrator**
- **Can:** Verify alumni, moderate content, view analytics, manage users
- **Has:** Full access with audit logging
- **Dashboard:** User stats, engagement metrics, success stories

### 4.2 Company Discovery System

#### Features:
- **Search & Filter:**
  - Search by company name
  - Filter by industry (IT, Finance, Consulting)
  - Filter by company type (Startup, Mid-size, MNC)
  - Filter by location and hiring status
  
- **Company Detail Page:**
  - Logo, basic info, industry
  - Alumni list (current & past employees)
  - Company intelligence (hiring process, tech stack, culture)
  - Top 10 common questions
  - Success stories

- **Company Intelligence:**
  - Interview process breakdown
  - Tech stack used
  - Salary ranges (anonymized)
  - Work-life balance rating
  - Typical hiring months

### 4.3 Question Submission System

#### Structured Question Form (Mandatory Fields):
1. **Target Company** (dropdown, searchable)
2. **Preferred Mentor** (optional, top 3 suggested)
3. **Question Type:** Interview Prep, Roadmap, Culture, Salary, Resume Review, Referral, General
4. **Background Context** (auto-filled from profile, editable)
5. **Current Status** (100-500 chars): "What have you done so far?"
6. **Specific Question** (500-2000 chars): "What exactly do you need help with?"
7. **Urgency Level:** Normal, High, Urgent
8. **Attachments** (optional): Resume PDF, project links

#### Business Rules:
- Max 1 question per company per week
- Max 4 unanswered questions at a time
- Profile must be >50% complete
- High/Urgent questions require justification

#### Quality Checks:
- **AI Quality Checker** analyzes:
  - Length: 100-2000 characters
  - Specificity: Contains company/role/tech keywords
  - Clarity: Not too vague
  - Context: Sufficient background info
- **Duplicate Detection:** TF-IDF similarity check (>70% similarity shows warning)

### 4.4 Queue Management (Core DSA Feature)

#### FIFO Queue Implementation
```python
# Conceptual structure
class MentorQuestionQueue:
    queue: deque  # collections.deque
    max_size: int  # mentor-defined limit
    mentor_id: int
    
    def enqueue(question):
        if queue.size() < max_size:
            queue.append(question)  # O(1)
        else:
            redirect_to_next_available_mentor()
    
    def dequeue():
        return queue.popleft()  # O(1), FIFO order
    
    def peek():
        return queue[0]  # view without removing
    
    def is_full():
        return queue.size() >= max_size
```

#### Features:
- Each mentor has individual queue
- Questions answered in order received
- Cannot skip questions (enforces fairness)
- If queue full → redirect to next available mentor
- Student sees: "Position #3 in queue, estimated wait: 6 days"

#### Priority Queue (for Urgent Questions)
- Uses Min-Heap (Python `heapq`)
- Priority levels: 1 (Urgent <2 weeks), 2 (High 2-4 weeks), 3 (Normal)
- Max 20% of questions can be urgent
- Requires justification (interview date proof)

### 4.5 Mentor Matching Algorithm

#### Scoring Factors (Total: 0-150 points)

| Factor | Weight | Calculation |
|--------|--------|-------------|
| Currently at Company | 50 pts | +50 if current, +30 if past |
| Years at Company | 20 pts | years × 5, max 20 |
| Skill Overlap | 20 pts | Jaccard similarity × 20 |
| Same Branch | 10 pts | +10 if match |
| Question Type Expertise | 15 pts | +15 if capable |
| Availability | -30 to +10 | -30 if >90% full, +10 if <30% |
| Trust Score | 15 pts | (trust/100) × 15 |
| Response Rate | 10 pts | response_rate × 10 |
| Recency | 10 pts | +10 current, decreasing |

#### Algorithm Flow:
1. Lookup mentors at target company (O(1) via HashMap)
2. Calculate match score for each mentor
3. Sort mentors by score (Merge Sort O(n log n))
4. Return top 3 matches
5. Auto-assign if student doesn't choose in 24 hours

### 4.6 Trust Score System

#### Outcome-Based Feedback
**Timing:** Requested 4-6 weeks after response

**Feedback Form:**
- Was advice relevant? (Yes/No)
- Did you implement it? (Yes/Partially/No/Too early)
- What was the outcome?
  - Got job/internship offer (+10 points)
  - Interview calls increased (+7 points)
  - Skills improved significantly (+5 points)
  - Advice was relevant (+2 points)
  - Somewhat helpful (+1 point)
  - Not helpful (-3 points)
- Rating (1-5 stars)
- Comments (optional)

#### Trust Score Calculation
```
Trust Score = (Total Points / Total Responses) × 10
Normalized to 0-100 scale

Additional Factors:
- Response rate: (answered/assigned) × 20% bonus
- Timeliness: Avg response <3 days → +5 points
- Consistency: >10 responses without negative → +5 points
```

#### Display:
- 90-100: Dark Green (Excellent) ⭐
- 75-89: Green (Very Good)
- 60-74: Yellow (Good)
- 40-59: Orange (Average)
- <40: Red (Poor)

### 4.7 Referral System

#### Eligibility Criteria:
- Interacted with mentor (≥1 question answered)
- Trust level with mentor >70/100
- Profile completeness >80%
- Has portfolio/projects showcased
- No pending unanswered questions

#### Referral Request Form:
1. Target Role (e.g., "Junior Python Developer")
2. Why you're ready (500-1000 chars):
   - Preparation completed
   - Projects built
   - Skills acquired
3. Resume Upload (PDF, max 2MB)
4. Portfolio Links (GitHub, LinkedIn, live projects)
5. Additional Notes (optional)

#### Mentor Review Process:
- View student's full profile & portfolio
- See interaction history
- Review projects and resume
- **Decision Options:**
  - **Approve:** Provide referral code and process steps
  - **Request Changes:** Ask for specific improvements
  - **Decline:** Provide constructive feedback
- Must respond within 7 days (else auto-declined)

#### Success Tracking:
- Interview Scheduled → Offer Received → Success Story

### 4.8 Knowledge Base

#### Features:
- **Full-text search** across all answered questions
- **Filters:** Company, question type, date range
- **Sort by:** Relevance, date, helpfulness
- **Privacy:** Student names anonymized, sensitive data redacted
- **Voting System:** "Was this helpful?" Yes/No buttons
- **Duplicate Linking:** Mentors can link duplicates to canonical answers

#### Benefits:
- Reduces mentor workload (40% target reduction)
- Students find answers faster
- Builds institutional knowledge

---

## 5. Data Models

### 5.1 Core Entities

```mermaid
erDiagram
    STUDENT ||--o{ QUESTION : submits
    QUESTION ||--|| RESPONSE : has
    ALUMNI ||--o{ RESPONSE : provides
    ALUMNI ||--o{ WORK_HISTORY : has
    COMPANY ||--o{ WORK_HISTORY : employs
    QUESTION }o--|| COMPANY : about
    STUDENT ||--o{ REFERRAL : requests
    ALUMNI ||--o{ REFERRAL : reviews
    ALUMNI ||--|| TRUST_SCORE : has
    COMPANY ||--|| COMPANY_INSIGHT : has
```

### 5.2 Key Database Tables

#### **users** - All user types
- `id` (PK, INT, AUTO_INCREMENT)
- `email` (VARCHAR(120), UNIQUE, NOT NULL)
- `password_hash` (VARCHAR(255), NOT NULL)
- `name` (VARCHAR(100), NOT NULL)
- `role` (ENUM: 'student', 'alumni', 'admin')
- `is_verified` (BOOLEAN, DEFAULT FALSE)
- `created_at` (TIMESTAMP)

#### **students** - Student-specific profile
- `user_id` (PK, FK → users.id)
- `roll_number` (VARCHAR(20), UNIQUE)
- `batch_year` (INT)
- `branch` (VARCHAR(50))
- `current_year` (INT: 1-4)
- `cgpa` (DECIMAL(3,2), NULL)
- `show_cgpa` (BOOLEAN, DEFAULT TRUE)
- `profile_completeness` (INT, 0-100)
- `career_goals` (TEXT)

#### **alumni** - Alumni mentor profiles
- `user_id` (PK, FK → users.id)
- `batch_year` (INT)
- `branch` (VARCHAR(50))
- `current_company_id` (FK → companies.id)
- `current_role` (VARCHAR(100))
- `linkedin_url` (VARCHAR(200))
- `is_accepting_questions` (BOOLEAN, DEFAULT TRUE)
- `max_questions_per_month` (INT, DEFAULT 10)
- `trust_score` (DECIMAL(5,2), DEFAULT 50.0)
- `total_questions_answered` (INT, DEFAULT 0)
- `avg_response_time_hours` (DECIMAL(5,2))
- `verification_status` (ENUM: 'pending', 'approved', 'rejected')

#### **companies** - Company master data
- `id` (PK, INT, AUTO_INCREMENT)
- `name` (VARCHAR(100), UNIQUE, NOT NULL)
- `website` (VARCHAR(255))
- `logo_url` (VARCHAR(255))
- `industry` (VARCHAR(50))
- `company_type` (ENUM: 'Startup', 'Mid-size', 'Large', 'MNC')
- `headquarters` (VARCHAR(100))
- `total_alumni_count` (INT, DEFAULT 0) # Denormalized
- `active_mentor_count` (INT, DEFAULT 0) # Denormalized
- `avg_trust_score` (DECIMAL(5,2)) # Denormalized

#### **questions** - Student questions
- `id` (PK, INT, AUTO_INCREMENT)
- `student_id` (FK → students.user_id, NOT NULL)
- `company_id` (FK → companies.id, NOT NULL)
- `assigned_mentor_id` (FK → alumni.user_id, NULL)
- `question_type` (ENUM: 'interview_prep', 'roadmap', 'culture', etc.)
- `question_text` (TEXT, NOT NULL)
- `context_json` (JSON) # Student background, current status
- `urgency` (ENUM: 'normal', 'high', 'urgent')
- `status` (ENUM: 'pending', 'queued', 'in_progress', 'answered', 'closed')
- `queue_position` (INT, NULL)
- `submitted_at` (TIMESTAMP)
- `answered_at` (TIMESTAMP, NULL)

#### **responses** - Mentor answers
- `id` (PK, INT, AUTO_INCREMENT)
- `question_id` (FK → questions.id, UNIQUE, NOT NULL)
- `mentor_id` (FK → alumni.user_id, NOT NULL)
- `response_text` (TEXT, NOT NULL)
- `resources_json` (JSON) # Links, attachments
- `responded_at` (TIMESTAMP)
- `last_edited_at` (TIMESTAMP, NULL)

#### **feedback** - Outcome-based feedback
- `id` (PK, INT, AUTO_INCREMENT)
- `question_id` (FK → questions.id, UNIQUE, NOT NULL)
- `was_relevant` (BOOLEAN)
- `was_implemented` (ENUM: 'yes', 'partially', 'no', 'too_early')
- `outcome` (ENUM: 'got_job', 'interview_calls', 'skills_improved', etc.)
- `rating` (INT, 1-5)
- `comments` (TEXT, NULL)
- `submitted_at` (TIMESTAMP)

#### **referrals** - Referral requests
- `id` (PK, INT, AUTO_INCREMENT)
- `student_id` (FK → students.user_id, NOT NULL)
- `mentor_id` (FK → alumni.user_id, NOT NULL)
- `company_id` (FK → companies.id, NOT NULL)
- `target_role` (VARCHAR(100))
- `portfolio_links_json` (JSON)
- `resume_url` (VARCHAR(255))
- `student_message` (TEXT)
- `status` (ENUM: 'pending', 'approved', 'declined', 'changes_requested')
- `mentor_feedback` (TEXT, NULL)
- `created_at` (TIMESTAMP)
- `reviewed_at` (TIMESTAMP, NULL)

#### **company_insights** - Aggregated intelligence
- `company_id` (PK, FK → companies.id)
- `typical_hiring_months` (JSON)
- `avg_hiring_duration_days` (INT)
- `fresher_salary_min/max` (INT, NULL)
- `interview_difficulty` (INT, 1-10)
- `interview_rounds_json` (JSON)
- `must_have_skills` (JSON)
- `tech_stack_json` (JSON)
- `work_life_balance_rating` (DECIMAL(3,2))
- `remote_policy` (ENUM: 'remote', 'hybrid', 'office')

### 5.3 Indexing Strategy
```sql
-- Performance optimization indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_alumni_company ON alumni(current_company_id);
CREATE INDEX idx_questions_student_status ON questions(student_id, status);
CREATE INDEX idx_questions_mentor_status ON questions(assigned_mentor_id, status);
CREATE INDEX idx_questions_company ON questions(company_id, status);
CREATE INDEX idx_work_history_company ON work_history(company_id);
```

---

## 6. User Interface Specifications

### 6.1 Design Principles

#### Visual Design
- **Color Scheme:**
  - Primary: `#2563EB` (Blue) - Trust, professionalism
  - Secondary: `#10B981` (Green) - Success, positive outcomes
  - Accent: `#F59E0B` (Amber) - Highlights, CTAs
  - Neutral: `#6B7280` (Gray) - Text, backgrounds
  - Error: `#EF4444` (Red) - Alerts, warnings

- **Typography:**
  - Headings: Inter or Poppins (Sans-serif)
  - Body: System fonts (Segoe UI, Roboto)
  - Code: Courier New, monospace

- **Spacing:** 8px grid system (8px, 16px, 24px, 32px)
- **Border Radius:** 8px for cards, 4px for buttons

#### UX Principles
- **Clarity:** Clear labels, no jargon
- **Consistency:** Same UI patterns across pages
- **Feedback:** Visual confirmation for all actions
- **Efficiency:** Minimize clicks to complete tasks
- **Accessibility:** WCAG 2.1 Level AA compliance

### 6.2 Responsive Design
- **Mobile:** <768px
- **Tablet:** 768px-1024px
- **Desktop:** >1024px
- Touch-friendly buttons (min 44px tap target)
- No horizontal scrolling

### 6.3 Key UI Components

#### Global Navigation Bar
```
Desktop:
┌────────────────────────────────────────────────────┐
│ [ASCEND Logo]  Companies  Mentors  Knowledge Base │
│                    [🔍 Search] [🔔3] [Profile ▼]   │
└────────────────────────────────────────────────────┘

Mobile (<768px):
┌────────────────────────────────────────────────────┐
│ [☰]  ASCEND              [🔔3] [Profile ▼]        │
└────────────────────────────────────────────────────┘
```

**Components:**
- Logo (clickable, returns to dashboard)
- Main Links: Companies, Mentors, Knowledge Base
- Search Bar (global search)
- Notifications Bell (badge count)
- Profile Dropdown (My Profile, My Questions, Settings, Logout)

---

## 7. Wireframe Descriptions

> [!NOTE]
> Detailed wireframes will be created as separate image artifacts

### 7.1 Student Dashboard
**Purpose:** Landing page after student login

**Layout:**
- Welcome message with student name
- Quick stats cards (Questions asked, Answers received, Profile completeness)
- "Ask Question" CTA button (prominent)
- Recent activity feed
- Target companies section (max 5)
- Recommended mentors carousel

### 7.2 Company Directory Page
**Purpose:** Browse and search companies

**Layout:**
- Hero section with search bar
- Filter sidebar (Industry, Type, Location, Hiring Status)
- Company cards grid (3 columns desktop, 1 mobile)
  - Each card: Logo, Name, Industry, Alumni count, Active mentors
- Pagination (20 per page)
- Sort dropdown (Most alumni, A-Z, Most active, Fastest response)

### 7.3 Company Detail Page
**Purpose:** View comprehensive company information

**Sections:**
1. **Header:** Logo, name, website, industry, basic stats
2. **Tabs:**
   - **Alumni** (default): List of current/past employees with filters
   - **Company Intel:** Hiring process, tech stack, culture
   - **Q&A Archive:** Top 10 common questions
   - **Success Stories:** Student testimonials
3. **Sidebar:** Quick actions (Ask Question, Bookmark Company)

### 7.4 Ask Question Page
**Purpose:** Submit structured question

**Form Sections:**
1. Target Company (pre-filled if coming from company page)
2. Select Mentor (Top 3 suggested, or Browse All)
3. Question Type (dropdown)
4. Background Context (auto-filled, editable textarea)
5. Current Status (textarea, 100-500 chars)
6. Specific Question (rich text editor, 500-2000 chars)
7. Urgency Level (radio buttons)
8. Attachments (file upload, optional)
9. Preview & Submit buttons
10. Similar questions warning (if detected)

### 7.5 Mentor Profile Page
**Purpose:** View mentor details before asking question

**Layout:**
- Profile header (Photo, Name, Batch, Current role, Company)
- Trust score badge (color-coded)
- Stats (Questions answered, Avg response time, Response rate)
- Work history timeline
- Expertise tags
- Helpful feedback snippets (anonymized)
- Availability status
- "Ask Question" CTA button
- "Request Referral" button (if eligible)

### 7.6 Mentor Queue Dashboard
**Purpose:** Alumni view and manage their question queue

**Layout:**
- Header stats (Pending questions, Answered this month, Trust score)
- Availability toggle switch
- Queue management controls (Max questions setting)
- Question list (FIFO order):
  - Each item: Student info, Question preview, Time in queue
  - Actions: View Details, Answer, Request Clarification
- Tabs: Pending, In Progress, Answered

### 7.7 Question Detail & Answer Page
**Purpose:** Mentor responds to question

**Layout:**
- Student info panel (Name, Year, Branch, Skills, CGPA)
- Question card:
  - Type, Company, Urgency
  - Context section
  - Full question text
  - Attachments
- Response editor (rich text, 200-5000 chars)
- Resource links section
- Preview & Submit buttons
- Save Draft option

### 7.8 Student My Questions Page
**Purpose:** Track question status

**Layout:**
- Tabs: Active (default), Answered, Closed
- Question cards showing:
  - Company logo & name
  - Question type & text preview
  - Assigned mentor (photo, name, trust score)
  - Status badge (Queued/In Progress/Answered)
  - Queue position (if queued)
  - Timestamp
  - Actions: View Details, Provide Feedback (if answered), Ask Follow-up

### 7.9 Knowledge Base Search Page
**Purpose:** Search previously answered questions

**Layout:**
- Hero search bar with placeholder "Search questions..."
- Filter sidebar (Company, Question Type, Date Range)
- Sort dropdown (Relevance, Most Helpful, Recent)
- Results list:
  - Each item: Question preview, Company, Type, Helpfulness votes
  - Click to expand full Q&A
- "Was this helpful?" voting buttons
- Related questions suggestions

### 7.10 Referral Request Page
**Purpose:** Student requests job referral

**Layout:**
- Eligibility check results (checkmarks/crosses)
- Mentor info card (reminder of who they're requesting from)
- Form:
  - Target Role (text input)
  - Why You're Ready (textarea, 500-1000 chars)
  - Resume Upload (PDF, max 2MB)
  - Portfolio Links (GitHub, LinkedIn, Live Demo)
  - Additional Notes (textarea, optional)
- Preview & Submit buttons
- Warning: "Mentor will review within 7 days"

### 7.11 Admin Dashboard
**Purpose:** Platform management and analytics

**Layout:**
- Overview cards (Total users, Active today, Questions answered, Avg response time)
- Charts:
  - User growth over time (line chart)
  - Questions per company (bar chart)
  - Mentor leaderboard (table)
- Quick actions:
  - Pending alumni verifications (badge count)
  - Flagged content moderation (badge count)
  - System health status
- Navigation: Users, Content, Analytics, Settings

### 7.12 Admin Alumni Verification Page
**Purpose:** Approve/reject alumni registrations

**Layout:**
- Queue of pending registrations
- Each card:
  - Alumni info (Name, Email, Batch, Current Company)
  - LinkedIn profile link
  - Uploaded documents viewer
  - Verification checklist
  - Actions: Approve, Reject, Request More Info
- Bulk actions toolbar

---

## 8. Non-Functional Requirements

### 8.1 Performance
- **Page Load Time:** <2 seconds on 4G connection
- **Database Queries:** <100ms execution time
- **Concurrent Users:** Support 500 simultaneous users
- **API Response:** <200ms (95th percentile)

### 8.2 Security
- **Password Hashing:** bcrypt with salt (cost factor: 12)
- **Password Policy:** Min 8 chars, 1 uppercase, 1 number, 1 special char
- **Session Timeout:** 24 hours
- **Account Lockout:** 5 failed attempts → 15-minute cooldown
- **HTTPS:** Enforced in production (TLS 1.2+)
- **SQL Injection:** Prevented via SQLAlchemy ORM (no raw SQL)
- **XSS Protection:** HTML sanitization in user inputs
- **CSRF Protection:** Tokens on all forms
- **Rate Limiting:** 
  - Login: 5 attempts/min/IP
  - Question submission: 1/hour/student
  - Search API: 100 requests/hour/user

### 8.3 Scalability
- **User Growth:** Scale to 5,000 users within 2 years
- **Data Growth:** Handle 10,000+ questions without degradation
- **Architecture:** Stateless design allows horizontal scaling
- **Caching:** Redis for sessions and frequently accessed data
- **Database:** Proper indexing, pagination on all lists

### 8.4 Reliability
- **Uptime:** 99% uptime target
- **Backup:** Daily full backup + 6-hour incremental
- **Recovery:** RPO: 6 hours, RTO: 2 hours
- **Error Handling:** Graceful degradation, user-friendly messages
- **Monitoring:** Health checks every 60 seconds

### 8.5 Maintainability
- **Code Quality:** PEP 8 compliance (Pylint, Flake8)
- **Documentation:** Docstrings for all functions, README, API docs
- **Modularity:** Blueprint-based Flask app
- **Testing:** Min 80% test coverage
- **Version Control:** Git with feature branches

---

## 9. Success Metrics (6-Month Post-Launch)

### User Adoption
- ✅ 500+ active students
- ✅ 100+ verified alumni
- ✅ 70% monthly active user rate

### Engagement
- ✅ 1,000+ questions answered
- ✅ 70%+ mentor response rate
- ✅ Avg response time <3 days
- ✅ 40% reduction in duplicate questions

### Quality
- ✅ Student satisfaction >4.2/5
- ✅ Mentor trust score avg >75/100
- ✅ 60%+ report "advice was actionable"

### Outcomes
- ✅ 20+ successful referrals processed
- ✅ 10+ job placements via platform
- ✅ 5+ documented success stories

---

## 10. Project Timeline

### Phase 1: MVP (Weeks 1-8)
- User authentication & profiles
- Company directory & search
- Question submission & queue
- Basic mentor matching
- Response system

### Phase 2: Core Features (Weeks 9-12)
- Trust score system
- Knowledge base
- Referral workflow
- Admin panel
- Email notifications

### Phase 3: Polish & Launch (Weeks 13-16)
- UI/UX refinements
- Testing & bug fixes
- Performance optimization
- Documentation
- Deployment

---

## 11. Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Low alumni signup | High | Early outreach, alumni ambassador program |
| Mentor burnout | Medium | Queue limits, pause functionality, gamification |
| Low question quality | Medium | AI checker, mandatory structure, admin moderation |
| Scalability issues | Medium | Cloud hosting, caching, proper indexing |
| Data privacy concerns | High | Clear privacy policy, GDPR-inspired controls |
| Duplicate questions | Medium | TF-IDF detection, knowledge base promotion |

---

## Next Steps

1. ✅ Review and approve design document
2. 📐 Create detailed wireframes (UI mockups)
3. 🎨 Design high-fidelity mockups (Figma)
4. 💻 Begin implementation (start with authentication)
5. 🧪 Setup testing infrastructure
6. 🚀 Deploy MVP to college

---

**Document Version:** 1.0  
**Last Updated:** January 25, 2026  
**Status:** Ready for Review
