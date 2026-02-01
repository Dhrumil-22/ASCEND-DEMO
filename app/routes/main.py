from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import User, Student, Alumni, Company, Question, Response, Feedback, Referral
from app.trust_calculator import submit_question_feedback

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return redirect(url_for('auth.login'))

@bp.route('/student_dashboard')
@login_required
def student_dashboard():
    if current_user.role != 'student':
        # Provide a basic redirect or different dashboard for alumni later
        return render_template('main/student_dashboard.html') # Placeholder if alumni logs in
    
    # Fetch Data for Dashboard
    question_count = Question.query.filter_by(student_id=current_user.student_profile.id).count()
    answered_count = Question.query.filter_by(student_id=current_user.student_profile.id, status='answered').count()
    companies = Company.query.limit(5).all()
    recent_responses = Response.query.join(Question).filter(Question.student_id == current_user.student_profile.id).order_by(Response.created_at.desc()).limit(3).all()

    return render_template('main/student_dashboard.html', 
                           question_count=question_count, 
                           answered_count=answered_count,
                           companies=companies,
                           recent_responses=recent_responses)

@bp.route('/companies')
@login_required
def company_list():
    page = request.args.get('page', 1, type=int)
    companies = Company.query.paginate(page=page, per_page=12)
    return render_template('main/company_list.html', companies=companies)

@bp.route('/knowledge_base')
@login_required
def knowledge_base():
    page = request.args.get('page', 1, type=int)
    query = request.args.get('q')
    
    if query:
        # Simple search implementation
        questions = Question.query.filter(Question.title.contains(query) | Question.body.contains(query)).filter_by(status='answered').paginate(page=page, per_page=10)
    else:
        questions = Question.query.filter_by(status='answered').order_by(Question.created_at.desc()).paginate(page=page, per_page=10)
        
    return render_template('main/knowledge_base.html', questions=questions)

@bp.route('/ask_question', methods=['GET', 'POST'])
@login_required
def ask_question():
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')
        company_id = request.form.get('company_id')
        category = request.form.get('category')
        urgency = request.form.get('urgency')
        
        question = Question(
            student_id=current_user.student_profile.id,
            company_id=company_id,
            title=title,
            body=body,
            category=category,
            urgency=urgency
        )
        db.session.add(question)
        db.session.commit()
        flash('Your question has been submitted successfully!', 'success')
        return redirect(url_for('main.student_dashboard'))
        
    companies = Company.query.all()
    return render_template('questions/ask.html', companies=companies)

@bp.route('/question/<int:id>')
@login_required
def view_question(id):
    question = Question.query.get_or_404(id)
    return render_template('questions/view.html', question=question)

@bp.route('/mentor_queue')
@login_required
def mentor_queue():
    if current_user.role != 'alumni':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.student_dashboard'))
        
    # Logic to fetch questions relevant to this mentor's company or expertise
    # For MVP: fetch all pending questions
    questions = Question.query.filter_by(status='pending').all()
    return render_template('main/mentor_queue.html', questions=questions)

@bp.route('/mentor_dashboard')
@login_required
def mentor_dashboard():
    if current_user.role != 'alumni':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.student_dashboard'))
    
    alumni = current_user.alumni_profile
    
    # Calculate stats
    pending_count = Question.query.filter_by(
        company_id=alumni.current_company_id, 
        status='pending'
    ).count()
    
    answered_count = Response.query.filter_by(mentor_id=alumni.id).count()
    
    # Get trust badge
    trust_score = alumni.trust_score
    if trust_score >= 75:
        trust_badge = 'Gold'
    elif trust_score >= 50:
        trust_badge = 'Silver'
    else:
        trust_badge = 'Bronze'
    
    # Recent responses
    recent_responses = Response.query.filter_by(mentor_id=alumni.id)\
        .order_by(Response.created_at.desc()).limit(5).all()
    
    return render_template('main/mentor_dashboard.html',
                         pending_count=pending_count,
                         answered_count=answered_count,
                         trust_score=trust_score,
                         trust_badge=trust_badge,
                         is_accepting=alumni.is_accepting_questions,
                         recent_responses=recent_responses)

@bp.route('/answer_question/<int:id>', methods=['GET'])
@login_required
def answer_question(id):
    if current_user.role != 'alumni':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.student_dashboard'))
    
    question = Question.query.get_or_404(id)
    return render_template('questions/answer.html', question=question)

@bp.route('/submit_answer/<int:id>', methods=['POST'])
@login_required
def submit_answer(id):
    if current_user.role != 'alumni':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.student_dashboard'))
    
    question = Question.query.get_or_404(id)
    answer_text = request.form.get('answer')
    
    if not answer_text:
        flash('Answer cannot be empty.', 'danger')
        return redirect(url_for('main.answer_question', id=id))
    
    # Create response
    response = Response(
        question_id=question.id,
        mentor_id=current_user.alumni_profile.id,
        body=answer_text
    )
    
    # Update question status
    question.status = 'answered'
    
    db.session.add(response)
    db.session.commit()
    
    flash('Your answer has been submitted successfully! 🎉', 'success')
    return redirect(url_for('main.mentor_dashboard'))

@bp.route('/mentor/my_responses')
@login_required
def mentor_responses():
    if current_user.role != 'alumni':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.student_dashboard'))
    
    page = request.args.get('page', 1, type=int)
    responses = Response.query.filter_by(mentor_id=current_user.alumni_profile.id)\
        .order_by(Response.created_at.desc())\
        .paginate(page=page, per_page=10)
    
    return render_template('main/mentor_responses.html', responses=responses)

@bp.route('/mentor/toggle_availability', methods=['POST'])
@login_required
def toggle_availability():
    if current_user.role != 'alumni':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.student_dashboard'))
    
    alumni = current_user.alumni_profile
    alumni.is_accepting_questions = not alumni.is_accepting_questions
    db.session.commit()
    
    status = 'active' if alumni.is_accepting_questions else 'paused'
    flash(f'Your status has been updated to {status}.', 'success')
    return redirect(url_for('main.mentor_dashboard'))

@bp.route('/question/<int:id>/feedback', methods=['GET'])
@login_required
def feedback_form(id):
    if current_user.role != 'student':
        flash('Only students can submit feedback.', 'danger')
        return redirect(url_for('main.student_dashboard'))
    
    question = Question.query.get_or_404(id)
    
    # Check if question belongs to current student
    if question.student_id != current_user.student_profile.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('main.student_dashboard'))
    
    # Check if question has been answered
    if question.status != 'answered':
        flash('Cannot submit feedback for unanswered questions.', 'warning')
        return redirect(url_for('main.view_question', id=id))
    
    response = Response.query.filter_by(question_id=id).first()
    return render_template('questions/feedback.html', question=question, response=response)

@bp.route('/question/<int:id>/submit_feedback', methods=['POST'])
@login_required
def submit_feedback(id):
    if current_user.role != 'student':
        flash('Only students can submit feedback.', 'danger')
        return redirect(url_for('main.student_dashboard'))
    
    question = Question.query.get_or_404(id)
    
    outcome = request.form.get('outcome')
    rating = request.form.get('rating', type=int)
    comment = request.form.get('comment')
    
    if not outcome or not rating:
        flash('Please select an outcome and rating.', 'danger')
        return redirect(url_for('main.feedback_form', id=id))
    
    # Submit feedback using trust calculator
    feedback = submit_question_feedback(
        question_id=id,
        student_id=current_user.student_profile.id,
        outcome=outcome,
        rating=rating,
        comment=comment
    )
    
    if feedback:
        flash('Thank you for your feedback! 🎉', 'success')
    else:
        flash('Error submitting feedback.', 'danger')
    
    return redirect(url_for('main.view_question', id=id))

@bp.route('/request_referral/<int:alumni_id>', methods=['GET', 'POST'])
@login_required
def request_referral(alumni_id):
    if current_user.role != 'student':
        flash('Only students can request referrals.', 'danger')
        return redirect(url_for('main.student_dashboard'))
    
    alumni = Alumni.query.get_or_404(alumni_id)
    
    if request.method == 'POST':
        message = request.form.get('message')
        
        if not message:
            flash('Please provide a message.', 'danger')
            return redirect(url_for('main.request_referral', alumni_id=alumni_id))
        
        # Create referral request
        referral = Referral(
            student_id=current_user.student_profile.id,
            mentor_id=alumni_id,
            company_id=alumni.current_company_id,
            message=message
        )
        
        db.session.add(referral)
        db.session.commit()
        
        flash('Referral request sent successfully! 🤝', 'success')
        return redirect(url_for('main.my_referrals'))
    
    return render_template('referrals/request.html', alumni=alumni)

@bp.route('/referrals/my_requests')
@login_required
def my_referrals():
    if current_user.role != 'student':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.student_dashboard'))
    
    referrals = Referral.query.filter_by(student_id=current_user.student_profile.id)\
        .order_by(Referral.requested_at.desc()).all()
    
    return render_template('referrals/student_dashboard.html', referrals=referrals)

@bp.route('/mentor/referrals')
@login_required
def mentor_referrals():
    if current_user.role != 'alumni':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.student_dashboard'))
    
    referrals = Referral.query.filter_by(mentor_id=current_user.alumni_profile.id)\
        .order_by(Referral.requested_at.desc()).all()
    
    return render_template('referrals/mentor_dashboard.html', referrals=referrals)

@bp.route('/referral/<int:id>/respond', methods=['POST'])
@login_required
def respond_referral(id):
    if current_user.role != 'alumni':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.student_dashboard'))
    
    referral = Referral.query.get_or_404(id)
    
    action = request.form.get('action')
    response_text = request.form.get('response')
    
    if action == 'approve':
        referral.status = 'approved'
        referral.mentor_response = response_text
        flash('Referral approved! 🎉', 'success')
    elif action == 'reject':
        referral.status = 'rejected'
        referral.mentor_response = response_text
        flash('Referral request declined.', 'info')
    
    from datetime import datetime
    referral.responded_at = datetime.utcnow()
    db.session.commit()
    
    return redirect(url_for('main.mentor_referrals'))
