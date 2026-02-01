# ASCEND - Wireframes Documentation
## UI/UX Mockups for Alumni-Student Mentorship Platform

> [!NOTE]
> This document contains visual wireframe mockups for all key user flows in the ASCEND platform. Each wireframe is designed following modern SaaS UI principles with emphasis on usability and clarity.

---

## Design System Quick Reference

### Colors
- **Primary Blue:** `#2563EB` - CTAs, links, active states
- **Success Green:** `#10B981` - Trust scores, positive indicators
- **Warning Amber:** `#F59E0B` - Alerts, high priority items
- **Neutral Gray:** `#6B7280` - Text, backgrounds
- **Error Red:** `#EF4444` - Errors, critical warnings

### Typography
- **Headings:** Inter / Poppins (Sans-serif, 16-32px)
- **Body:** System fonts (14-16px)
- **Spacing:** 8px grid system

### Components
- **Cards:** 8px border radius, subtle shadow
- **Buttons:** 4px border radius, min 44px height
- **Forms:** Clear labels, inline validation

---

## 1. Student Dashboard

**Purpose:** Landing page showing student's overview and quick actions

![Student Dashboard](C:/Users/91940/.gemini/antigravity/brain/bb092cbf-1693-4c2d-b4cc-0e6c6d86f685/student_dashboard_wireframe_1769334113504.png)

### Key Features:
- **Welcome Header:** Personalized greeting with student photo
- **Stats Cards:** Questions Asked (5), Answers Received (3), Profile Completion (85%)
- **Primary CTA:** Large "Ask a Question" button
- **Target Companies:** Horizontal carousel of 5 company logos (Google, Odoo, TCS, Amazon, Microsoft)
- **Recent Activity:** Timeline of question statuses and mentor responses
- **Recommended Mentors:** Carousel of top 3 suggested mentors with trust scores

### User Actions:
- Click "Ask a Question" → Navigate to question submission
- Click company logo → View company detail page
- Click mentor card → View mentor profile
- View activity items → See question details

---

## 2. Company Directory

**Purpose:** Browse and search companies where alumni work

![Company Directory](C:/Users/91940/.gemini/antigravity/brain/bb092cbf-1693-4c2d-b4cc-0e6c6d86f685/company_directory_wireframe_1769334136926.png)

### Key Features:
- **Hero Search Bar:** Large search input for company names
- **Filter Sidebar (Left 25%):**
  - Industry checkboxes (IT Services, Product, Consulting, Finance)
  - Company Type radio buttons (Startup, Mid-size, Large, MNC)
  - Location dropdown
  - "Actively Hiring" checkbox
  - "Apply Filters" button
- **Company Grid (Right 75%):**
  - Sort dropdown (Most Alumni, A-Z, Most Active, Fastest Response)
  - 3-column grid of company cards
  - Each card: Logo, Name, Industry tag, Alumni count, Active mentors (green badge)
  - "View Details" link on each card
- **Pagination:** Page numbers at bottom

### Company Card Shows:
- Company logo (large, centered)
- Company name (bold)
- Industry tag (gray pill)
- "12 Alumni" count
- "5 Active Mentors" with green checkmark badge
- "View Details" link (blue)

---

## 3. Ask Question Page

**Purpose:** Structured form for submitting questions to mentors

![Ask Question Page](C:/Users/91940/.gemini/antigravity/brain/bb092cbf-1693-4c2d-b4cc-0e6c6d86f685/ask_question_page_wireframe_1769334162067.png)

### Key Features:
- **Breadcrumb Navigation:** Home > Companies > Odoo > Ask Question
- **Form Sections:**
  1. **Target Company:** Dropdown (pre-filled if from company page)
  2. **Select Mentor:** 
     - "Top 3 Suggested Mentors" cards with radio buttons
     - Shows: Photo, Name "Rahul Patel", Role "SDE-2", Trust Score "94/100" (green)
     - "Browse All Mentors" link
  3. **Question Type:** Dropdown (Interview Prep, Roadmap, Culture, Salary, etc.)
  4. **Background Context:** Gray auto-filled box (Year: 3rd | Branch: CS | Skills: Python, Django, PostgreSQL) with edit button
  5. **Current Status:** Textarea (100-500 chars)
  6. **Your Question:** Rich text editor with formatting toolbar (500-2000 chars)
  7. **Urgency Level:** Radio buttons (Normal, High, Urgent)
  8. **Attachments:** File upload for resume (PDF only)
- **Duplicate Warning:** Yellow banner if similar question found
- **Action Buttons:** Gray "Preview" and blue "Submit Question"

### Validation Features:
- Character count indicators
- Required field markers
- Real-time quality checks
- Duplicate question detection

---

## 4. Mentor Profile Page

**Purpose:** View mentor details, stats, and expertise

![Mentor Profile](C:/Users/91940/.gemini/antigravity/brain/bb092cbf-1693-4c2d-b4cc-0e6c6d86f685/mentor_profile_wireframe_1769334185823.png)

### Key Features:
- **Profile Header:**
  - Large circular profile photo (left)
  - Name "Rahul Patel" (large, bold)
  - Current role "Senior Software Developer at Odoo"
  - Batch "2020, Computer Engineering"
  - Trust Score badge "94/100" (green background, star icon)
  - "Available" status badge (green)

- **Stats Row (4 cards):**
  - Questions Answered: 47 (with icon)
  - Avg Response Time: 1.8 days (with clock icon)
  - Response Rate: 96% (with graph icon)
  - Helpful Feedback: 42/47 (with thumbs up icon)

- **Work History (Vertical Timeline):**
  - Current: "Odoo - Senior SDE (2022-Present) - 2 years"
  - Past: "Odoo - SDE (2020-2022) - 2 years"
  - Tech stack tags: Python, PostgreSQL, Odoo Framework

- **Expertise Tags:**
  - Row of blue pill-shaped tags
  - Python, Django, PostgreSQL, System Design, Interview Prep, Career Guidance

- **What Students Say:**
  - 2 testimonial cards (anonymized)
  - "Student from 3rd Year CS: 'Very detailed roadmap. Following it helped me get interview call!' ⭐⭐⭐⭐⭐"
  - Star ratings visible

- **Action Buttons:**
  - Large blue "Ask Question" (primary CTA)
  - Gray outlined "Request Referral" (secondary)

---

## 5. Mentor Queue Dashboard

**Purpose:** Alumni view and manage their question queue

![Mentor Queue Dashboard](C:/Users/91940/.gemini/antigravity/brain/bb092cbf-1693-4c2d-b4cc-0e6c6d86f685/mentor_queue_dashboard_wireframe_1769334209784.png)

### Key Features:
- **Header Section:**
  - Title "My Queue"
  - Stats: "Pending: 3" | "Answered This Month: 12" | "Trust Score: 94/100" (green badge)
  - Availability toggle: "Accepting Questions: ON" (green toggle switch)
  - Settings icon: "Queue Settings: Max 10 questions/month"

- **Tab Navigation:**
  - "Pending (3)" (active, blue underline)
  - "In Progress (1)"
  - "Answered (47)"

- **Queue List (FIFO Order):**
  
  **Position #1 Card:**
  - Left: Student info box (photo, "Rohan Shah, 3rd Year CS, Skills: Python, Django")
  - Center: 
    - Question preview "How should I prepare for Odoo SDE interview? I've done some LeetCode and built a few Django projects..."
    - "View Full Question" link
    - Company logo "Odoo"
    - Type badge "Interview Prep" (blue)
    - Time "Submitted 1 day ago"
  - Right: Blue "Answer Question" button
  
  **Position #2 Card:**
  - Similar layout
  - Orange "High Priority" badge
  - Time "Submitted 2 days ago"
  
  **Position #3 Card:**
  - Similar layout
  - Time "Submitted 3 days ago"

### Design Notes:
- FIFO order clearly visible with position numbers
- Each card is a horizontal layout for scannability
- CTAs prominently placed on right
- Student context visible at a glance

---

## 6. Knowledge Base Search

**Purpose:** Search and browse previously answered questions

![Knowledge Base](C:/Users/91940/.gemini/antigravity/brain/bb092cbf-1693-4c2d-b4cc-0e6c6d86f685/knowledge_base_wireframe_1769334237425.png)

### Key Features:
- **Hero Search Section:**
  - Large search bar "Search previously answered questions..."
  - Blue search icon button
  - Quick filter chips below: "All Companies" | "Interview Prep" | "Roadmaps" | "Last 30 Days"

- **Left Sidebar (25%):**
  - Company multiselect dropdown (Odoo, Google, TCS checked)
  - Question Type checkboxes (Interview Prep, Roadmap, Culture, Salary)
  - Date Range dropdown "Last 6 months"
  - Blue "Apply Filters" button

- **Main Content (75%):**
  - Sort dropdown (top-right): "Most Relevant"
  - Results count: "Showing 24 results for 'Odoo interview'"
  
  **Q&A Result Cards:**
  
  **Card 1:**
  - Header: Company logo "Odoo" | Badge "Interview Prep" (blue) | "3 months ago"
  - Question (bold): "How should I prepare for Odoo's technical interview rounds?"
  - Answer preview: "Based on my experience, Odoo focuses heavily on Python OOP concepts and PostgreSQL. Here's a month-by-month roadmap..." (truncated with ellipsis)
  - Tags: Python, PostgreSQL, Interview (gray pills)
  - Bottom: "👍 47 students found this helpful" | Green "View Full Answer" link
  
  **Cards 2 & 3:**
  - Similar structure with different questions
  - "Roadmaps" (card 2) and "Culture" (card 3) badges
  - Different helpfulness vote counts

- **Pagination:** < 1 2 3 > at bottom

### Design Notes:
- Search-first interface
- Stack Overflow-inspired Q&A cards
- Helpful voting system prominently displayed
- Tag-based navigation
- Clear visual hierarchy

---

## 7. Admin Dashboard

**Purpose:** Platform management, analytics, and moderation

![Admin Dashboard](C:/Users/91940/.gemini/antigravity/brain/bb092cbf-1693-4c2d-b4cc-0e6c6d86f685/admin_dashboard_wireframe_1769334293897.png)

### Key Features:
- **Top Navbar:**
  - Profile with "Admin" badge (blue)
  - Same global navigation

- **Overview Stats (4 Cards):**
  - "Total Users: 623" (user icon, green "+45 this month" indicator)
  - "Active Today: 89" (green dot icon)
  - "Questions Answered: 1,247" (checkmark icon)
  - "Avg Response Time: 2.3 days" (clock icon)

- **Two-Column Layout:**
  
  **Left Column (60%):**
  - **User Growth Chart:**
    - Line chart showing upward trend
    - X-axis: Jan, Feb, Mar, Apr, May, Jun
    - Y-axis: 500, 530, 565, 580, 610, 623
    - Blue line with shaded area under curve
  
  - **Questions by Company:**
    - Horizontal bar chart
    - Odoo: 45 questions (longest bar)
    - Google: 38
    - TCS: 32
    - Amazon: 28
    - Microsoft: 24
  
  **Right Column (40%):**
  - **Pending Actions Card:**
    - Red badge indicators
    - "Alumni Verifications: 8 pending" + "Review" button
    - "Flagged Content: 3 items" + "Moderate" button
    - "System Health: All systems operational" (green checkmark)
  
  - **Top Mentors Leaderboard:**
    - Table with columns: Rank, Mentor, Trust Score, Questions Answered
    - Rank 1 (Sarah Lee): 98 trust, 120 answered (trophy icon)
    - Rank 2-5 with decreasing scores
    - Small mentor photos in table

- **Bottom Controls:**
  - Date range selector "Jun 1, 2024 - Jun 30, 2024"
  - Blue "Export Report" button

### Design Notes:
- Data-first dashboard
- Action items clearly flagged
- Visual charts for trends
- Quick access to moderation tasks

---

## 8. Referral Request Page

**Purpose:** Student requests job referral from mentor

![Referral Request](C:/Users/91940/.gemini/antigravity/brain/bb092cbf-1693-4c2d-b4cc-0e6c6d86f685/referral_request_wireframe_1769334320364.png)

### Key Features:
- **Breadcrumb:** Home > Mentors > Rahul Patel > Request Referral
- **Page Title:** "Request Referral from Rahul Patel"

- **Mentor Reminder Card:**
  - Small photo
  - "Rahul Patel - Senior SDE at Odoo"
  - Trust Score badge "94/100" (blue circle)

- **Eligibility Check Section:**
  - ✅ "You have received guidance from this mentor (2 questions answered)"
  - ✅ "Your trust level with mentor: 85/100 (Required: >70)"
  - ✅ "Your profile completeness: 90% (Required: >80%)"
  - ✅ "Portfolio projects: 3 projects showcased"
  - ✅ "No pending unanswered questions"
  - Green success banner: "✅ You are eligible to request a referral!"

- **Referral Request Form:**
  
  1. **Target Role:**
     - Text input: "e.g., Junior Python Developer at Odoo"
  
  2. **Why You're Ready:**
     - Large textarea (500-1000 chars)
     - Helper text with bullet points:
       - Preparation completed
       - Projects built
       - Skills acquired
     - Character counter "0/1000 chars"
  
  3. **Resume Upload:**
     - Dashed border upload area
     - "Upload Resume (PDF, max 2MB)"
     - Upload cloud icon
     - "Choose File" button
  
  4. **Portfolio Links:**
     - GitHub: Text input with GitHub icon
     - LinkedIn: Text input with LinkedIn icon
     - Live Demo/Website: Text input with link icon
  
  5. **Additional Notes (Optional):**
     - Textarea

- **Info Banner:**
  - Blue background with info icon
  - "⚠️ Mentor will review your request within 7 business days. Make sure your portfolio clearly demonstrates your skills."

- **Action Buttons:**
  - Gray "Cancel" button (left)
  - Blue "Submit Referral Request" button (right, primary)

### Design Notes:
- Clear eligibility indicators build confidence
- Form guidance helps students prepare better
- Reminder of mentor context keeps request focused
- Professional, trust-building layout

---

## Responsive Design Considerations

All wireframes are designed with mobile-first principles:

### Mobile (<768px):
- Single column layouts
- Collapsible filters in sidebar
- Hamburger menu navigation
- Touch-friendly buttons (min 44px)
- Stacked stat cards
- Simplified mentor cards (vertical)

### Tablet (768px-1024px):
- 2-column grids where applicable
- Condensed navigation
- Optimized card sizes

### Desktop (>1024px):
- Full layouts as shown in wireframes
- 3-column grids for company cards
- Side-by-side comparisons
- Expanded navigation

---

## Accessibility Features

All wireframes incorporate:
- **Semantic HTML5:** Proper heading hierarchy
- **ARIA Labels:** Screen reader support
- **Keyboard Navigation:** Tab order, focus states
- **Color Contrast:** WCAG 2.1 Level AA (4.5:1 minimum)
- **Touch Targets:** Minimum 44×44px for mobile
- **Alt Text:** All images and icons
- **Form Labels:** Clear, descriptive labels

---

## Key User Flows

### Flow 1: Student Asks Question
1. Student Dashboard → Click "Ask a Question"
2. Ask Question Page → Select company (e.g., Odoo)
3. System suggests top 3 mentors → Student selects mentor
4. Fill structured form → Submit
5. See confirmation → Question enters mentor's queue

### Flow 2: Student Requests Referral
1. Browse Mentors / Search Company → Find mentor
2. Mentor Profile → Click "Request Referral"
3. Referral Request Page → Check eligibility (all green ✅)
4. Fill form with portfolio → Submit
5. Mentor reviews → Approves/Declines → Student notified

### Flow 3: Mentor Responds to Question
1. Mentor Queue Dashboard → See "Pending: 3" notification
2. Click Position #1 question → View full details
3. Read student context & question
4. Click "Answer Question" → Rich text editor
5. Write comprehensive response → Submit
6. Question moves to "Answered" → Student notified

### Flow 4: Student Searches Knowledge Base
1. Knowledge Base Search → Type "Odoo interview preparation"
2. Apply filters (Company: Odoo, Type: Interview Prep)
3. Browse results → Click "View Full Answer"
4. Read Q&A thread → Vote "Helpful" if useful
5. Optionally: Ask new question if not satisfied

---

## Design Patterns Used

### 1. **Card-Based Layouts**
- Company cards, mentor cards, question cards
- Consistent spacing, shadows, and hover states
- Clear visual hierarchy within cards

### 2. **Badge System**
- Trust scores (green: excellent, yellow: good)
- Status indicators (Available, Pending, Answered)
- Priority flags (High Priority, Urgent)
- Role badges (Admin, Mentor, Student)

### 3. **Progressive Disclosure**
- Collapsed filters that expand
- "View Full Question" links
- Expandable Q&A cards
- Dropdown menus for advanced options

### 4. **Empty States**
- "No questions in this tab" messages
- Helpful illustrations or icons
- Clear CTAs to take action

### 5. **Feedback Mechanisms**
- Success messages (green banners)
- Warning alerts (yellow banners)
- Error messages (red, inline)
- Toast notifications (optional)

---

## Next Steps

1. ✅ **Review Wireframes** - Stakeholder approval
2. 🎨 **High-Fidelity Mockups** - Create Figma designs
3. 🖼️ **Design Assets** - Export icons, logos, images
4. 💻 **Frontend Development** - Implement HTML/CSS/JS
5. 🔌 **Backend Integration** - Connect to Flask API
6. 🧪 **User Testing** - Validate with real users
7. 🚀 **Launch MVP** - Deploy to college

---

## Wireframe Summary

| Page | Purpose | Key Components | Priority |
|------|---------|---------------|----------|
| Student Dashboard | Landing page | Stats, CTA, Companies, Activity | P0 |
| Company Directory | Browse companies | Search, Filters, Grid, Pagination | P0 |
| Ask Question | Submit questions | Structured form, Mentor selection | P0 |
| Mentor Profile | View mentor details | Stats, History, Expertise, CTAs | P0 |
| Mentor Queue | Manage questions | FIFO queue, Response interface | P0 |
| Knowledge Base | Search Q&A | Search, Filters, Voting | P1 |
| Admin Dashboard | Platform analytics | Charts, Stats, Moderation | P1 |
| Referral Request | Request referrals | Eligibility check, Portfolio form | P1 |

---

**Document Version:** 1.0  
**Last Updated:** January 25, 2026  
**Total Wireframes:** 8 core pages  
**Status:** Ready for Review & Development
