"""
Trust Score Calculator for ASCEND
Calculates and updates mentor trust scores based on feedback and outcomes
"""

from app.models import Alumni, Feedback, Response, Question
from app import db
from datetime import datetime, timedelta


class TrustCalculator:
    """Calculate and manage mentor trust scores"""
    
    # Scoring constants
    BASE_SCORE = 50
    MIN_SCORE = 0
    MAX_SCORE = 100
    
    # Score adjustments
    HELPFUL_BONUS = 5
    INTERVIEW_BONUS = 10
    REFERRAL_BONUS = 15
    NOT_HELPFUL_PENALTY = 3
    UNANSWERED_PENALTY = 2
    
    @staticmethod
    def calculate_trust_score(alumni_id):
        """
        Calculate complete trust score for a mentor
        
        Formula:
        Base Score: 50
        + Positive Feedback: +5 per helpful rating
        + Interview Outcomes: +10 per got_interview
        + Referral Success: +15 per successful referral
        - Negative Feedback: -3 per not_helpful
        - Unanswered Questions: -2 per timeout
        
        Min: 0, Max: 100
        """
        score = TrustCalculator.BASE_SCORE
        
        # Get all feedback for this mentor
        feedbacks = Feedback.query.filter_by(mentor_id=alumni_id).all()
        
        for feedback in feedbacks:
            if feedback.outcome == 'helpful':
                score += TrustCalculator.HELPFUL_BONUS
            elif feedback.outcome == 'got_interview':
                score += TrustCalculator.INTERVIEW_BONUS
            elif feedback.outcome == 'got_referral':
                score += TrustCalculator.REFERRAL_BONUS
            elif feedback.outcome == 'not_helpful':
                score -= TrustCalculator.NOT_HELPFUL_PENALTY
        
        # Penalty for unanswered questions (questions assigned but not answered in 7 days)
        unanswered_count = TrustCalculator.get_unanswered_count(alumni_id)
        score -= (unanswered_count * TrustCalculator.UNANSWERED_PENALTY)
        
        # Clamp score between MIN and MAX
        score = max(TrustCalculator.MIN_SCORE, min(TrustCalculator.MAX_SCORE, score))
        
        return score
    
    @staticmethod
    def get_unanswered_count(alumni_id):
        """Count questions that were assigned but not answered within 7 days"""
        alumni = Alumni.query.get(alumni_id)
        if not alumni:
            return 0
        
        # Get questions for this mentor's company that are still pending after 7 days
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        
        unanswered = Question.query.filter(
            Question.company_id == alumni.current_company_id,
            Question.status == 'pending',
            Question.created_at < seven_days_ago
        ).count()
        
        return unanswered
    
    @staticmethod
    def update_trust_score(alumni_id, feedback=None):
        """
        Update mentor's trust score incrementally
        
        Args:
            alumni_id: ID of the alumni/mentor
            feedback: Optional Feedback object for incremental update
        
        Returns:
            New trust score
        """
        alumni = Alumni.query.get(alumni_id)
        if not alumni:
            return None
        
        # Recalculate complete score
        new_score = TrustCalculator.calculate_trust_score(alumni_id)
        
        # Update in database
        alumni.trust_score = new_score
        db.session.commit()
        
        return new_score
    
    @staticmethod
    def get_trust_badge(score):
        """
        Get badge level based on trust score
        
        Returns: 'Bronze', 'Silver', or 'Gold'
        """
        if score >= 75:
            return 'Gold'
        elif score >= 50:
            return 'Silver'
        else:
            return 'Bronze'
    
    @staticmethod
    def get_trust_metrics(alumni_id):
        """
        Get detailed trust metrics for a mentor
        
        Returns: dict with breakdown of score components
        """
        feedbacks = Feedback.query.filter_by(mentor_id=alumni_id).all()
        
        metrics = {
            'total_feedback': len(feedbacks),
            'helpful_count': sum(1 for f in feedbacks if f.outcome == 'helpful'),
            'interview_count': sum(1 for f in feedbacks if f.outcome == 'got_interview'),
            'referral_count': sum(1 for f in feedbacks if f.outcome == 'got_referral'),
            'not_helpful_count': sum(1 for f in feedbacks if f.outcome == 'not_helpful'),
            'unanswered_count': TrustCalculator.get_unanswered_count(alumni_id),
            'average_rating': 0
        }
        
        # Calculate average rating
        ratings = [f.rating for f in feedbacks if f.rating]
        if ratings:
            metrics['average_rating'] = sum(ratings) / len(ratings)
        
        # Calculate current score
        metrics['current_score'] = TrustCalculator.calculate_trust_score(alumni_id)
        metrics['badge'] = TrustCalculator.get_trust_badge(metrics['current_score'])
        
        return metrics
    
    @staticmethod
    def bulk_update_scores():
        """Update trust scores for all mentors (batch operation)"""
        all_alumni = Alumni.query.filter_by(is_verified=True).all()
        
        updated_count = 0
        for alumni in all_alumni:
            new_score = TrustCalculator.calculate_trust_score(alumni.id)
            if alumni.trust_score != new_score:
                alumni.trust_score = new_score
                updated_count += 1
        
        db.session.commit()
        
        return updated_count


class FeedbackManager:
    """Manage feedback submission and processing"""
    
    @staticmethod
    def submit_feedback(question_id, student_id, outcome, rating=None, comment=None):
        """
        Submit feedback for a question/response
        
        Args:
            question_id: ID of the question
            student_id: ID of the student submitting feedback
            outcome: Outcome type ('helpful', 'got_interview', 'got_referral', 'not_helpful')
            rating: Star rating (1-5)
            comment: Optional text comment
        
        Returns:
            Feedback object or None if error
        """
        # Get the question and its response
        question = Question.query.get(question_id)
        if not question or question.status != 'answered':
            return None
        
        # Get the response
        response = Response.query.filter_by(question_id=question_id).first()
        if not response:
            return None
        
        # Check if feedback already exists
        existing = Feedback.query.filter_by(question_id=question_id).first()
        if existing:
            # Update existing feedback
            existing.outcome = outcome
            existing.rating = rating
            existing.comment = comment
            db.session.commit()
            
            # Update trust score
            TrustCalculator.update_trust_score(response.mentor_id)
            
            return existing
        
        # Create new feedback
        feedback = Feedback(
            question_id=question_id,
            response_id=response.id,
            student_id=student_id,
            mentor_id=response.mentor_id,
            outcome=outcome,
            rating=rating,
            comment=comment
        )
        
        db.session.add(feedback)
        db.session.commit()
        
        # Update mentor's trust score
        TrustCalculator.update_trust_score(response.mentor_id)
        
        return feedback
    
    @staticmethod
    def get_feedback_stats():
        """Get overall feedback statistics"""
        total_feedback = Feedback.query.count()
        
        stats = {
            'total_feedback': total_feedback,
            'helpful': Feedback.query.filter_by(outcome='helpful').count(),
            'got_interview': Feedback.query.filter_by(outcome='got_interview').count(),
            'got_referral': Feedback.query.filter_by(outcome='got_referral').count(),
            'not_helpful': Feedback.query.filter_by(outcome='not_helpful').count(),
        }
        
        # Calculate percentages
        if total_feedback > 0:
            for key in ['helpful', 'got_interview', 'got_referral', 'not_helpful']:
                stats[f'{key}_percent'] = (stats[key] / total_feedback) * 100
        
        # Average rating
        avg_rating = db.session.query(db.func.avg(Feedback.rating))\
            .filter(Feedback.rating.isnot(None))\
            .scalar()
        
        stats['average_rating'] = round(avg_rating, 2) if avg_rating else 0
        
        return stats


def calculate_mentor_trust_score(alumni_id):
    """Convenience function to calculate trust score"""
    return TrustCalculator.calculate_trust_score(alumni_id)


def submit_question_feedback(question_id, student_id, outcome, rating=None, comment=None):
    """Convenience function to submit feedback"""
    return FeedbackManager.submit_feedback(question_id, student_id, outcome, rating, comment)


def get_mentor_trust_metrics(alumni_id):
    """Convenience function to get trust metrics"""
    return TrustCalculator.get_trust_metrics(alumni_id)
