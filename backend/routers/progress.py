from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, date
from typing import Dict, List
from database import get_db
from models import User, Progress, HomeworkScan, Quiz, StudyNote
from auth import get_current_user

router = APIRouter(prefix="/progress", tags=["Progress"])


def calculate_streak(user_id: int, db: Session) -> int:
    """Calculate current streak"""
    # Get all activity dates
    scans = db.query(HomeworkScan.created_at).filter(HomeworkScan.user_id == user_id).all()
    quizzes = db.query(Quiz.created_at).filter(Quiz.user_id == user_id).all()
    notes = db.query(StudyNote.created_at).filter(StudyNote.user_id == user_id).all()

    # Combine and get unique dates
    activity_dates = set()
    for scan in scans:
        activity_dates.add(scan.created_at.date())
    for quiz in quizzes:
        activity_dates.add(quiz.created_at.date())
    for note in notes:
        activity_dates.add(note.created_at.date())

    if not activity_dates:
        return 0

    # Sort dates
    sorted_dates = sorted(activity_dates, reverse=True)

    # Calculate streak
    streak = 0
    current_date = date.today()

    for activity_date in sorted_dates:
        if activity_date == current_date or activity_date == current_date - timedelta(days=1):
            streak += 1
            current_date = activity_date - timedelta(days=1)
        else:
            break

    return streak


def update_weekly_breakdown(progress: Progress, activity_type: str, value: int = 1):
    """Update weekly breakdown"""
    today = date.today()
    week_key = f"{today.year}-W{today.isocalendar()[1]}"

    weekly_data = progress.weekly_breakdown or {}

    if week_key not in weekly_data:
        weekly_data[week_key] = {
            "questions": 0,
            "quizzes": 0,
            "notes": 0,
            "minutes": 0
        }

    weekly_data[week_key][activity_type] = weekly_data[week_key].get(activity_type, 0) + value

    return weekly_data


@router.get("/")
async def get_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's progress and statistics"""
    progress = db.query(Progress).filter(Progress.user_id == current_user.id).first()

    if not progress:
        # Create progress record if not exists
        progress = Progress(user_id=current_user.id)
        db.add(progress)
        db.commit()
        db.refresh(progress)

    # Calculate current streak
    current_streak = calculate_streak(current_user.id, db)

    # Update streak if needed
    if current_streak != progress.current_streak:
        progress.current_streak = current_streak
        if current_streak > progress.longest_streak:
            progress.longest_streak = current_streak
        db.commit()

    # Get recent activity (last 7 days)
    seven_days_ago = datetime.utcnow() - timedelta(days=7)

    recent_scans = db.query(HomeworkScan).filter(
        HomeworkScan.user_id == current_user.id,
        HomeworkScan.created_at >= seven_days_ago
    ).count()

    recent_quizzes = db.query(Quiz).filter(
        Quiz.user_id == current_user.id,
        Quiz.created_at >= seven_days_ago
    ).count()

    recent_notes = db.query(StudyNote).filter(
        StudyNote.user_id == current_user.id,
        StudyNote.created_at >= seven_days_ago
    ).count()

    # Get subject breakdown
    subject_counts = {}
    scans = db.query(HomeworkScan.subject).filter(
        HomeworkScan.user_id == current_user.id
    ).all()

    for scan in scans:
        subject = scan.subject or "general"
        subject_counts[subject] = subject_counts.get(subject, 0) + 1

    return {
        "current_streak": progress.current_streak,
        "longest_streak": progress.longest_streak,
        "total_minutes_studied": progress.total_minutes_studied,
        "total_questions_solved": progress.total_questions_solved,
        "total_quizzes_completed": progress.total_quizzes_completed,
        "total_notes_created": progress.total_notes_created,
        "level": progress.level,
        "experience_points": progress.experience_points,
        "topics_learned": progress.topics_learned or [],
        "achievement_badges": progress.achievement_badges or [],
        "subject_breakdown": subject_counts,
        "last_7_days": {
            "scans": recent_scans,
            "quizzes": recent_quizzes,
            "notes": recent_notes
        },
        "weekly_breakdown": progress.weekly_breakdown or {}
    }


@router.post("/log-study-time")
async def log_study_time(
    minutes: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Log study time"""
    progress = db.query(Progress).filter(Progress.user_id == current_user.id).first()

    if not progress:
        progress = Progress(user_id=current_user.id)
        db.add(progress)

    progress.total_minutes_studied += minutes
    progress.last_activity_date = datetime.utcnow()

    # Update weekly breakdown
    progress.weekly_breakdown = update_weekly_breakdown(progress, "minutes", minutes)

    # Award experience points (1 point per minute)
    progress.experience_points += minutes

    # Check for level up (every 100 XP = 1 level)
    new_level = progress.experience_points // 100 + 1
    if new_level > progress.level:
        progress.level = new_level

    db.commit()

    return {
        "total_minutes": progress.total_minutes_studied,
        "experience_points": progress.experience_points,
        "level": progress.level
    }


@router.get("/leaderboard")
async def get_leaderboard(
    db: Session = Depends(get_db),
    limit: int = 10
):
    """Get top users by experience points"""
    top_users = db.query(Progress).order_by(
        Progress.experience_points.desc()
    ).limit(limit).all()

    leaderboard = []
    for i, progress in enumerate(top_users):
        user = db.query(User).filter(User.id == progress.user_id).first()
        if user:
            leaderboard.append({
                "rank": i + 1,
                "user_name": user.full_name or "Student",
                "level": progress.level,
                "experience_points": progress.experience_points,
                "streak": progress.current_streak
            })

    return {"leaderboard": leaderboard}


@router.get("/achievements")
async def get_achievements(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get available and earned achievements"""
    progress = db.query(Progress).filter(Progress.user_id == current_user.id).first()

    if not progress:
        return {"achievements": [], "earned": []}

    # Define achievements
    all_achievements = [
        {
            "id": "first_scan",
            "name": "Getting Started",
            "description": "Complete your first homework scan",
            "icon": "📸",
            "requirement": progress.total_questions_solved >= 1
        },
        {
            "id": "quiz_master",
            "name": "Quiz Master",
            "description": "Complete 10 quizzes",
            "icon": "🎯",
            "requirement": progress.total_quizzes_completed >= 10
        },
        {
            "id": "note_taker",
            "name": "Note Taker",
            "description": "Create 5 study notes",
            "icon": "📝",
            "requirement": progress.total_notes_created >= 5
        },
        {
            "id": "streak_3",
            "name": "3-Day Streak",
            "description": "Study for 3 days in a row",
            "icon": "🔥",
            "requirement": progress.longest_streak >= 3
        },
        {
            "id": "streak_7",
            "name": "Week Warrior",
            "description": "Study for 7 days in a row",
            "icon": "⚡",
            "requirement": progress.longest_streak >= 7
        },
        {
            "id": "level_5",
            "name": "Level 5",
            "description": "Reach level 5",
            "icon": "⭐",
            "requirement": progress.level >= 5
        },
        {
            "id": "scholar",
            "name": "Scholar",
            "description": "Solve 50 problems",
            "icon": "🎓",
            "requirement": progress.total_questions_solved >= 50
        },
        {
            "id": "dedicated",
            "name": "Dedicated Learner",
            "description": "Study for 10 hours total",
            "icon": "💪",
            "requirement": progress.total_minutes_studied >= 600
        }
    ]

    earned = [ach for ach in all_achievements if ach["requirement"]]
    locked = [ach for ach in all_achievements if not ach["requirement"]]

    return {
        "earned": earned,
        "locked": locked,
        "total_earned": len(earned),
        "total_available": len(all_achievements)
    }


@router.get("/stats")
async def get_detailed_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed statistics"""
    # Average quiz scores
    quizzes = db.query(Quiz).filter(
        Quiz.user_id == current_user.id,
        Quiz.completed == True
    ).all()

    if quizzes:
        avg_score = sum(q.score for q in quizzes if q.score) / len(quizzes)
        total_quiz_questions = sum(q.total_questions for q in quizzes)
        total_correct = sum(q.correct_answers for q in quizzes if q.correct_answers)
    else:
        avg_score = 0
        total_quiz_questions = 0
        total_correct = 0

    # Activity by subject
    scans_by_subject = {}
    all_scans = db.query(HomeworkScan).filter(
        HomeworkScan.user_id == current_user.id
    ).all()

    for scan in all_scans:
        subject = scan.subject or "general"
        if subject not in scans_by_subject:
            scans_by_subject[subject] = {
                "count": 0,
                "with_solution": 0
            }
        scans_by_subject[subject]["count"] += 1
        if scan.solution_text:
            scans_by_subject[subject]["with_solution"] += 1

    return {
        "quiz_stats": {
            "average_score": round(avg_score, 2),
            "total_quizzes": len(quizzes),
            "total_questions": total_quiz_questions,
            "total_correct": total_correct,
            "accuracy": round((total_correct / total_quiz_questions * 100) if total_quiz_questions > 0 else 0, 2)
        },
        "subject_breakdown": scans_by_subject,
        "total_scans": len(all_scans)
    }
