"""
FIFO Queue Management System for ASCEND
Handles question distribution to mentors using FIFO and priority queues
"""

from collections import deque
import heapq
from datetime import datetime
from app.models import Question, Alumni, Company
from app import db


class QuestionNode:
    """Node for priority queue with question data"""
    def __init__(self, question, priority=0):
        self.question = question
        self.priority = priority
        self.timestamp = question.created_at
    
    def __lt__(self, other):
        # Higher priority first, then older questions first
        if self.priority != other.priority:
            return self.priority > other.priority
        return self.timestamp < other.timestamp


class MentorQueue:
    """Manages question queues for mentors"""
    
    def __init__(self):
        # Company-wise FIFO queues
        self.company_queues = {}
        # Priority queue for urgent questions
        self.priority_queue = []
        # Track mentor load (mentor_id -> pending count)
        self.mentor_load = {}
    
    def enqueue_question(self, question):
        """Add question to appropriate queue"""
        company_id = question.company_id
        
        # Determine priority (0=normal, 1=high)
        priority = 1 if question.urgency == 'High' else 0
        
        if priority == 1:
            # Add to priority queue
            node = QuestionNode(question, priority=1)
            heapq.heappush(self.priority_queue, node)
        else:
            # Add to company-specific FIFO queue
            if company_id not in self.company_queues:
                self.company_queues[company_id] = deque()
            self.company_queues[company_id].append(question)
    
    def get_next_question(self, mentor_id, company_id):
        """Get next question for a specific mentor"""
        # First check priority queue for this company
        for i, node in enumerate(self.priority_queue):
            if node.question.company_id == company_id:
                # Remove and return this question
                self.priority_queue.pop(i)
                heapq.heapify(self.priority_queue)
                return node.question
        
        # Then check company FIFO queue
        if company_id in self.company_queues and self.company_queues[company_id]:
            return self.company_queues[company_id].popleft()
        
        return None
    
    def get_queue_size(self, company_id):
        """Get total pending questions for a company"""
        size = 0
        
        # Count from FIFO queue
        if company_id in self.company_queues:
            size += len(self.company_queues[company_id])
        
        # Count from priority queue
        for node in self.priority_queue:
            if node.question.company_id == company_id:
                size += 1
        
        return size
    
    def requeue_question(self, question_id):
        """Re-add a question to queue (if mentor didn't answer)"""
        question = Question.query.get(question_id)
        if question and question.status == 'pending':
            self.enqueue_question(question)


class QueueAllocator:
    """Allocates questions to mentors using load balancing"""
    
    @staticmethod
    def get_available_mentors(company_id):
        """Get all available mentors for a company"""
        return Alumni.query.filter_by(
            current_company_id=company_id,
            is_verified=True,
            is_accepting_questions=True
        ).all()
    
    @staticmethod
    def calculate_mentor_load(mentor_id):
        """Calculate current pending question load for a mentor"""
        from app.models import Response
        
        # Count questions assigned but not answered
        pending_responses = Response.query.filter_by(
            mentor_id=mentor_id
        ).join(Question).filter(
            Question.status == 'pending'
        ).count()
        
        return pending_responses
    
    @staticmethod
    def assign_to_mentor(question):
        """Smart assignment of question to best available mentor"""
        company_id = question.company_id
        
        # Get available mentors
        mentors = QueueAllocator.get_available_mentors(company_id)
        
        if not mentors:
            # No mentors available for this company
            return None
        
        # Find mentor with lowest load
        best_mentor = None
        min_load = float('inf')
        
        for mentor in mentors:
            load = QueueAllocator.calculate_mentor_load(mentor.id)
            
            # Tie-breaker: higher trust score
            if load < min_load or (load == min_load and mentor.trust_score > best_mentor.trust_score):
                best_mentor = mentor
                min_load = load
        
        return best_mentor
    
    @staticmethod
    def distribute_questions():
        """Distribute all pending questions to mentors (batch processing)"""
        pending_questions = Question.query.filter_by(status='pending').all()
        
        assignments = []
        for question in pending_questions:
            mentor = QueueAllocator.assign_to_mentor(question)
            if mentor:
                assignments.append({
                    'question_id': question.id,
                    'mentor_id': mentor.id,
                    'mentor_name': mentor.user.name
                })
        
        return assignments


# Global queue instance
global_queue = MentorQueue()


def initialize_queue():
    """Initialize queue with all pending questions"""
    pending_questions = Question.query.filter_by(status='pending').all()
    
    for question in pending_questions:
        global_queue.enqueue_question(question)
    
    return len(pending_questions)


def get_mentor_queue_questions(mentor_id):
    """Get all questions in queue for a specific mentor"""
    alumni = Alumni.query.get(mentor_id)
    if not alumni:
        return []
    
    company_id = alumni.current_company_id
    
    # Get questions from both queues
    questions = []
    
    # Priority questions
    for node in global_queue.priority_queue:
        if node.question.company_id == company_id:
            questions.append(node.question)
    
    # FIFO questions
    if company_id in global_queue.company_queues:
        questions.extend(list(global_queue.company_queues[company_id]))
    
    # Sort by priority then timestamp
    questions.sort(key=lambda q: (
        0 if q.urgency == 'High' else 1,
        q.created_at
    ))
    
    return questions


def get_queue_stats():
    """Get overall queue statistics"""
    stats = {
        'total_pending': Question.query.filter_by(status='pending').count(),
        'high_priority': Question.query.filter_by(status='pending', urgency='High').count(),
        'companies_with_questions': len(global_queue.company_queues),
        'available_mentors': Alumni.query.filter_by(
            is_verified=True,
            is_accepting_questions=True
        ).count()
    }
    
    return stats
