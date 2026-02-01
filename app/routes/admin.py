from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models import User, Student, Alumni, Question

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.before_request
@login_required
def require_admin():
    if current_user.role != 'admin':
        abort(403)

@bp.route('/')
@bp.route('/dashboard')
def dashboard():
    student_count = Student.query.count()
    alumni_count = Alumni.query.count()
    verified_alumni_count = Alumni.query.filter_by(is_verified=True).count()
    question_count = Question.query.count()
    
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                           student_count=student_count,
                           alumni_count=alumni_count,
                           verified_alumni_count=verified_alumni_count,
                           question_count=question_count,
                           recent_users=recent_users)

@bp.route('/users')
def user_list():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)

@bp.route('/alumni/approve/<int:id>')
def approve_alumni(id):
    alumni = Alumni.query.get_or_404(id)
    alumni.is_verified = True
    db.session.commit()
    flash(f'Alumni {alumni.user.name} has been verified.', 'success')
    return redirect(url_for('admin.user_list'))

@bp.route('/alumni/revoke/<int:id>')
def revoke_alumni(id):
    alumni = Alumni.query.get_or_404(id)
    alumni.is_verified = False
    db.session.commit()
    flash(f'Alumni {alumni.user.name} verification revoked.', 'warning')
    return redirect(url_for('admin.user_list'))
