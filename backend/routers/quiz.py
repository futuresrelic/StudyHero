from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from database import get_db
from models import User, Quiz, Progress
from auth import get_current_user
from quizgen import quiz_generator

router = APIRouter(prefix="/quiz", tags=["Quiz"])


class QuizCreate(BaseModel):
    topic: str
    subject: str
    difficulty: str = "medium"
    num_questions: int = 10


class QuizSubmit(BaseModel):
    quiz_id: int
    answers: List[str]


class QuizResponse(BaseModel):
    id: int
    topic: str
    subject: str
    difficulty: str
    questions: List[dict]
    score: Optional[float]
    completed: bool
    created_at: datetime


@router.post("/generate", response_model=QuizResponse)
async def generate_quiz(
    quiz_data: QuizCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate a new quiz"""
    try:
        # Generate quiz using AI
        result = quiz_generator.generate_quiz(
            topic=quiz_data.topic,
            subject=quiz_data.subject,
            difficulty=quiz_data.difficulty,
            num_questions=quiz_data.num_questions
        )

        if not result.get('success'):
            raise HTTPException(status_code=500, detail=result.get('error'))

        quiz_content = result.get('quiz', {})
        questions = quiz_content.get('questions', [])

        # Save to database
        quiz = Quiz(
            user_id=current_user.id,
            topic=quiz_data.topic,
            subject=quiz_data.subject,
            difficulty=quiz_data.difficulty,
            questions=questions,
            total_questions=len(questions),
            completed=False
        )

        db.add(quiz)
        db.commit()
        db.refresh(quiz)

        return {
            "id": quiz.id,
            "topic": quiz.topic,
            "subject": quiz.subject,
            "difficulty": quiz.difficulty,
            "questions": quiz.questions,
            "score": None,
            "completed": False,
            "created_at": quiz.created_at
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/submit")
async def submit_quiz(
    submission: QuizSubmit,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit quiz answers and get results"""
    # Get quiz
    quiz = db.query(Quiz).filter(
        Quiz.id == submission.quiz_id,
        Quiz.user_id == current_user.id
    ).first()

    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    # Grade quiz
    result = quiz_generator.grade_quiz(quiz.questions, submission.answers)

    if not result.get('success'):
        raise HTTPException(status_code=400, detail=result.get('error'))

    # Update quiz
    quiz.user_answers = submission.answers
    quiz.score = result.get('score')
    quiz.correct_answers = result.get('correct_count')
    quiz.completed = True
    quiz.completed_at = datetime.utcnow()

    db.commit()

    # Update progress
    progress = db.query(Progress).filter(Progress.user_id == current_user.id).first()
    if progress:
        progress.total_quizzes_completed += 1
        progress.last_activity_date = datetime.utcnow()

        # Update experience points
        progress.experience_points += int(result.get('score', 0))

        db.commit()

    return {
        "quiz_id": quiz.id,
        "score": result.get('score'),
        "grade": result.get('grade'),
        "correct_count": result.get('correct_count'),
        "total_questions": result.get('total_questions'),
        "message": result.get('message'),
        "results": result.get('results')
    }


@router.get("/history")
async def get_quiz_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 20,
    offset: int = 0
):
    """Get user's quiz history"""
    quizzes = db.query(Quiz).filter(
        Quiz.user_id == current_user.id
    ).order_by(Quiz.created_at.desc()).offset(offset).limit(limit).all()

    return {
        "quizzes": [
            {
                "id": q.id,
                "topic": q.topic,
                "subject": q.subject,
                "difficulty": q.difficulty,
                "score": q.score,
                "completed": q.completed,
                "total_questions": q.total_questions,
                "correct_answers": q.correct_answers,
                "created_at": q.created_at.isoformat(),
                "completed_at": q.completed_at.isoformat() if q.completed_at else None
            }
            for q in quizzes
        ],
        "total": db.query(Quiz).filter(Quiz.user_id == current_user.id).count()
    }


@router.get("/{quiz_id}", response_model=QuizResponse)
async def get_quiz(
    quiz_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific quiz"""
    quiz = db.query(Quiz).filter(
        Quiz.id == quiz_id,
        Quiz.user_id == current_user.id
    ).first()

    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    return {
        "id": quiz.id,
        "topic": quiz.topic,
        "subject": quiz.subject,
        "difficulty": quiz.difficulty,
        "questions": quiz.questions,
        "score": quiz.score,
        "completed": quiz.completed,
        "created_at": quiz.created_at
    }


@router.post("/practice")
async def generate_practice_problems(
    topic: str,
    difficulty: str = "medium",
    count: int = 5,
    current_user: User = Depends(get_current_user)
):
    """Generate practice problems for a topic"""
    try:
        result = quiz_generator.generate_practice_problems(topic, difficulty, count)

        if not result.get('success'):
            raise HTTPException(status_code=500, detail=result.get('error'))

        return result.get('practice_problems')

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
