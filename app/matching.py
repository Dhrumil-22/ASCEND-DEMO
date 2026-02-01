"""
Mentor Matching Algorithm for ASCEND
Intelligently matches students' questions with the best available mentors
"""

from app.models import Alumni, Question, Company, Response
from app import db


class MentorMatcher:
    """Intelligent mentor matching system"""
    
    @staticmethod
    def find_best_mentor(question):
        """
        Find the best mentor for a question using multi-criteria matching
        
        Matching Criteria (in priority order):
        1. Company match (exact)
        2. Verified alumni only
        3. Currently accepting questions
        4. Lowest pending question count (load balancing)
        5. Highest trust score (tie-breaker)
        
        Returns: Alumni object or None
        """
        company_id = question.company_id
        
        # Get available mentors for this company
        mentors = MentorMatcher.get_available_mentors(company_id)
        
        if not mentors:
            # Try fallback matching
            return MentorMatcher.fallback_matching(question)
        
        # Score and rank mentors
        scored_mentors = []
        
        for mentor in mentors:
            score = MentorMatcher.calculate_match_score(mentor, question)
            scored_mentors.append((score, mentor))
        
        # Sort by score (descending)
        scored_mentors.sort(key=lambda x: x[0], reverse=True)
        
        # Return best match
        return scored_mentors[0][1] if scored_mentors else None
    
    @staticmethod
    def get_available_mentors(company_id):
        """
        Get all available mentors for a specific company
        
        Filters:
        - Exact company match
        - Verified status
        - Accepting questions
        """
        mentors = Alumni.query.filter_by(
            current_company_id=company_id,
            is_verified=True,
            is_accepting_questions=True
        ).all()
        
        return mentors
    
    @staticmethod
    def calculate_match_score(mentor, question):
        """
        Calculate match score for a mentor-question pair
        
        Score components:
        - Base score: 100
        - Load penalty: -5 per pending question
        - Trust bonus: +trust_score
        - Response rate bonus: +10 if >80% response rate
        
        Returns: int (score)
        """
        score = 100
        
        # Load balancing - penalize mentors with many pending questions
        pending_count = MentorMatcher.get_pending_count(mentor.id)
        score -= (pending_count * 5)
        
        # Trust score bonus
        score += mentor.trust_score
        
        # Response rate bonus
        response_rate = MentorMatcher.calculate_response_rate(mentor.id)
        if response_rate > 0.8:
            score += 10
        
        return score
    
    @staticmethod
    def get_pending_count(mentor_id):
        """Get count of questions currently pending for this mentor"""
        # Count questions in mentor's company that are pending
        mentor = Alumni.query.get(mentor_id)
        if not mentor:
            return 0
        
        pending = Question.query.filter_by(
            company_id=mentor.current_company_id,
            status='pending'
        ).count()
        
        return pending
    
    @staticmethod
    def calculate_response_rate(mentor_id):
        """Calculate mentor's response rate (answered / total assigned)"""
        total_responses = Response.query.filter_by(mentor_id=mentor_id).count()
        
        if total_responses == 0:
            return 0.5  # Neutral score for new mentors
        
        # For simplicity, assume all responses mean questions were answered
        # In production, you'd track assigned vs answered separately
        return min(1.0, total_responses / max(1, total_responses))
    
    @staticmethod
    def fallback_matching(question):
        """
        Fallback matching when no exact company match exists
        
        Strategy:
        1. Find mentors in same industry
        2. Find any available verified mentor
        3. Return None if no mentors available
        """
        company = Company.query.get(question.company_id)
        
        if company and company.industry:
            # Try to find mentors in same industry
            industry_companies = Company.query.filter_by(
                industry=company.industry
            ).all()
            
            for comp in industry_companies:
                if comp.id == company.id:
                    continue
                
                mentors = MentorMatcher.get_available_mentors(comp.id)
                if mentors:
                    # Return mentor with highest trust score
                    return max(mentors, key=lambda m: m.trust_score)
        
        # Last resort: any available mentor
        any_mentor = Alumni.query.filter_by(
            is_verified=True,
            is_accepting_questions=True
        ).order_by(Alumni.trust_score.desc()).first()
        
        return any_mentor
    
    @staticmethod
    def get_mentor_recommendations(student_id, limit=5):
        """
        Get recommended mentors for a student based on their profile
        
        Considers:
        - Student's target companies (from past questions)
        - Student's skills
        - Mentor availability and trust score
        
        Returns: List of Alumni objects
        """
        from app.models import Student
        
        student = Student.query.get(student_id)
        if not student:
            return []
        
        # Get companies student has asked about
        target_companies = db.session.query(Question.company_id)\
            .filter_by(student_id=student_id)\
            .distinct()\
            .all()
        
        company_ids = [c[0] for c in target_companies]
        
        if not company_ids:
            # Return top mentors by trust score
            return Alumni.query.filter_by(
                is_verified=True,
                is_accepting_questions=True
            ).order_by(Alumni.trust_score.desc()).limit(limit).all()
        
        # Get mentors from these companies
        mentors = Alumni.query.filter(
            Alumni.current_company_id.in_(company_ids),
            Alumni.is_verified == True,
            Alumni.is_accepting_questions == True
        ).order_by(Alumni.trust_score.desc()).limit(limit).all()
        
        return mentors


class CompanyMentorMap:
    """HashMap-based data structure for fast company-to-mentor lookup"""
    
    def __init__(self):
        self._map = {}
        self._build_map()
    
    def _build_map(self):
        """Build the company -> mentors mapping"""
        companies = Company.query.all()
        
        for company in companies:
            mentors = Alumni.query.filter_by(
                current_company_id=company.id,
                is_verified=True
            ).all()
            
            self._map[company.id] = {
                'company_name': company.name,
                'mentors': mentors,
                'available_count': sum(1 for m in mentors if m.is_accepting_questions)
            }
    
    def get_mentors(self, company_id):
        """Get all mentors for a company"""
        return self._map.get(company_id, {}).get('mentors', [])
    
    def get_available_mentors(self, company_id):
        """Get only available mentors for a company"""
        mentors = self.get_mentors(company_id)
        return [m for m in mentors if m.is_accepting_questions]
    
    def get_company_stats(self, company_id):
        """Get statistics for a company"""
        return self._map.get(company_id, {})
    
    def refresh(self):
        """Refresh the mapping (call after mentor updates)"""
        self._map = {}
        self._build_map()


# Global mentor map instance
mentor_map = CompanyMentorMap()


def match_question_to_mentor(question_id):
    """
    Main function to match a question to a mentor
    
    Args:
        question_id: ID of the question to match
    
    Returns:
        Alumni object or None
    """
    question = Question.query.get(question_id)
    if not question:
        return None
    
    return MentorMatcher.find_best_mentor(question)


def get_matching_stats():
    """Get statistics about mentor matching"""
    stats = {
        'total_mentors': Alumni.query.filter_by(is_verified=True).count(),
        'available_mentors': Alumni.query.filter_by(
            is_verified=True,
            is_accepting_questions=True
        ).count(),
        'companies_with_mentors': db.session.query(Alumni.current_company_id)\
            .filter(Alumni.is_verified == True)\
            .distinct()\
            .count(),
        'avg_trust_score': db.session.query(db.func.avg(Alumni.trust_score))\
            .filter(Alumni.is_verified == True)\
            .scalar() or 50
    }
    
    return stats
