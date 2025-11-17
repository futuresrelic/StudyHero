from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
import os
import time
import shutil
from database import get_db
from models import User, HomeworkScan, RateLimit, Progress
from auth import get_current_user, check_subscription
from config import settings
from ocr import ocr_processor
from solver.math_engine import math_solver
from solver.science_engine import science_solver
from solver.history_engine import history_solver
from ai_tutor import ai_tutor

router = APIRouter(prefix="/homework", tags=["Homework"])

# Upload directory
UPLOAD_DIR = "/tmp/studyhero_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


class ScanRequest(BaseModel):
    question_text: str
    subject: Optional[str] = None


class SolutionResponse(BaseModel):
    id: int
    question_text: str
    subject: str
    solution_text: Optional[str]
    explanation_steps: Optional[List[dict]]
    confidence_score: Optional[float]
    created_at: datetime


def check_rate_limit(user: User, db: Session) -> bool:
    """Check if user has exceeded rate limit"""
    if check_subscription(user):
        return True  # Premium users have unlimited

    today = date.today()
    rate_limit_record = db.query(RateLimit).filter(
        RateLimit.user_id == user.id,
        RateLimit.date >= datetime(today.year, today.month, today.day)
    ).first()

    if not rate_limit_record:
        # Create new record
        rate_limit_record = RateLimit(user_id=user.id, date=datetime.utcnow(), request_count=0)
        db.add(rate_limit_record)
        db.commit()

    if rate_limit_record.request_count >= settings.FREE_TIER_DAILY_LIMIT:
        return False

    return True


def increment_rate_limit(user: User, db: Session):
    """Increment rate limit counter"""
    today = date.today()
    rate_limit_record = db.query(RateLimit).filter(
        RateLimit.user_id == user.id,
        RateLimit.date >= datetime(today.year, today.month, today.day)
    ).first()

    if rate_limit_record:
        rate_limit_record.request_count += 1
        db.commit()


@router.post("/scan", response_model=SolutionResponse)
async def scan_homework(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Scan homework image and extract question"""
    # Check rate limit
    if not check_rate_limit(current_user, db):
        raise HTTPException(
            status_code=429,
            detail="Daily limit reached. Upgrade to Premium for unlimited scans!"
        )

    # Save uploaded file
    file_path = os.path.join(UPLOAD_DIR, f"{current_user.id}_{int(time.time())}_{file.filename}")

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Process with OCR
        start_time = time.time()
        ocr_result = ocr_processor.process_homework_image(file_path)
        processing_time = int((time.time() - start_time) * 1000)

        if not ocr_result.get('success'):
            raise HTTPException(status_code=400, detail=ocr_result.get('error'))

        # Get first question
        questions = ocr_result.get('questions', [])
        if not questions:
            raise HTTPException(status_code=400, detail="No questions detected in image")

        question_text = questions[0]['text']
        subject = ocr_result.get('subject', 'general')

        # Save to database
        homework_scan = HomeworkScan(
            user_id=current_user.id,
            question_text=question_text,
            image_url=file_path,
            subject=subject,
            confidence_score=ocr_result.get('confidence'),
            processing_time_ms=processing_time
        )

        db.add(homework_scan)
        db.commit()
        db.refresh(homework_scan)

        # Increment rate limit
        increment_rate_limit(current_user, db)

        return {
            "id": homework_scan.id,
            "question_text": question_text,
            "subject": subject,
            "solution_text": None,
            "explanation_steps": None,
            "confidence_score": ocr_result.get('confidence'),
            "created_at": homework_scan.created_at
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup temp file (or keep for records)
        pass


@router.post("/solve/{scan_id}", response_model=SolutionResponse)
async def solve_homework(
    scan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Solve a homework problem"""
    # Get homework scan
    scan = db.query(HomeworkScan).filter(
        HomeworkScan.id == scan_id,
        HomeworkScan.user_id == current_user.id
    ).first()

    if not scan:
        raise HTTPException(status_code=404, detail="Homework scan not found")

    # Check if already solved
    if scan.solution_text:
        return {
            "id": scan.id,
            "question_text": scan.question_text,
            "subject": scan.subject,
            "solution_text": scan.solution_text,
            "explanation_steps": scan.explanation_steps,
            "confidence_score": scan.confidence_score,
            "created_at": scan.created_at
        }

    # Solve based on subject
    subject = scan.subject.lower()
    question = scan.question_text

    try:
        if subject == 'math':
            result = math_solver.solve(question)
        elif subject == 'science':
            result = science_solver.solve(question)
        elif subject == 'history':
            result = history_solver.solve(question)
        else:
            # Use AI tutor for general or complex problems
            ai_result = ai_tutor.generate_explanation(
                question,
                subject,
                current_user.school_level or "high"
            )
            if ai_result.get('success'):
                result = ai_result.get('explanation', {})
            else:
                raise HTTPException(status_code=500, detail="Could not generate solution")

        # Update scan with solution
        if 'error' not in result:
            scan.solution_text = str(result.get('result') or result.get('answer') or result.get('explanation'))
            scan.explanation_steps = result.get('steps', [])
            db.commit()

            # Update progress
            progress = db.query(Progress).filter(Progress.user_id == current_user.id).first()
            if progress:
                progress.total_questions_solved += 1
                progress.last_activity_date = datetime.utcnow()
                db.commit()

        return {
            "id": scan.id,
            "question_text": scan.question_text,
            "subject": scan.subject,
            "solution_text": scan.solution_text,
            "explanation_steps": scan.explanation_steps,
            "confidence_score": scan.confidence_score,
            "created_at": scan.created_at
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history")
async def get_homework_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 20,
    offset: int = 0
):
    """Get user's homework history"""
    scans = db.query(HomeworkScan).filter(
        HomeworkScan.user_id == current_user.id
    ).order_by(HomeworkScan.created_at.desc()).offset(offset).limit(limit).all()

    return {
        "scans": [
            {
                "id": scan.id,
                "question_text": scan.question_text,
                "subject": scan.subject,
                "has_solution": scan.solution_text is not None,
                "created_at": scan.created_at.isoformat()
            }
            for scan in scans
        ],
        "total": db.query(HomeworkScan).filter(HomeworkScan.user_id == current_user.id).count()
    }


@router.get("/{scan_id}", response_model=SolutionResponse)
async def get_homework(
    scan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific homework scan"""
    scan = db.query(HomeworkScan).filter(
        HomeworkScan.id == scan_id,
        HomeworkScan.user_id == current_user.id
    ).first()

    if not scan:
        raise HTTPException(status_code=404, detail="Homework scan not found")

    return {
        "id": scan.id,
        "question_text": scan.question_text,
        "subject": scan.subject,
        "solution_text": scan.solution_text,
        "explanation_steps": scan.explanation_steps,
        "confidence_score": scan.confidence_score,
        "created_at": scan.created_at
    }
