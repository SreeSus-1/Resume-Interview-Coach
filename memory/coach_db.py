from tinydb import TinyDB
from datetime import datetime

db = TinyDB("career_coach_memory.json")

def save_resume_session(career_goal, target_role, resume_text, resume_feedback, role_fit_feedback):
    db.insert({
        "type": "resume_session",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "career_goal": career_goal,
        "target_role": target_role,
        "resume_text": resume_text,
        "resume_feedback": resume_feedback,
        "role_fit_feedback": role_fit_feedback
    })

def save_interview_response(target_role, question, answer, feedback):
    db.insert({
        "type": "interview_response",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "target_role": target_role,
        "question": question,
        "answer": answer,
        "feedback": feedback
    })

def get_all_records():
    return db.all()