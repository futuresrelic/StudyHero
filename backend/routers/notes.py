from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime
from database import get_db
from models import User, StudyNote, HomeworkScan, Progress
from auth import get_current_user
from notes_builder import notes_builder

router = APIRouter(prefix="/notes", tags=["Study Notes"])


class NoteCreate(BaseModel):
    title: str
    topic: str
    subject: str
    content: str
    source_scan_id: Optional[int] = None


class FlashcardCreate(BaseModel):
    content: str
    subject: str = "general"
    count: int = 10


class NoteResponse(BaseModel):
    id: int
    title: str
    topic: str
    subject: str
    keywords: Optional[List[str]]
    bullets: Optional[List[str]]
    formulas: Optional[List[Dict]]
    definitions: Optional[Dict]
    flashcards: Optional[List[Dict]]
    created_at: datetime


@router.post("/create", response_model=NoteResponse)
async def create_study_notes(
    note_data: NoteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create study notes from content"""
    try:
        # Generate notes using AI
        result = notes_builder.build_notes(
            content=note_data.content,
            subject=note_data.subject,
            include_flashcards=True
        )

        if not result.get('success'):
            raise HTTPException(status_code=500, detail=result.get('error'))

        notes_data = result.get('notes', {})

        # Save to database
        study_note = StudyNote(
            user_id=current_user.id,
            title=note_data.title,
            topic=note_data.topic,
            subject=note_data.subject,
            keywords=notes_data.get('keywords', []),
            bullets=notes_data.get('key_points', []),
            formulas=notes_data.get('formulas', []),
            definitions=notes_data.get('definitions', {}),
            flashcards=notes_data.get('flashcards', []),
            source_scan_id=note_data.source_scan_id
        )

        db.add(study_note)
        db.commit()
        db.refresh(study_note)

        # Update progress
        progress = db.query(Progress).filter(Progress.user_id == current_user.id).first()
        if progress:
            progress.total_notes_created += 1
            progress.last_activity_date = datetime.utcnow()

            # Add topic to learned topics
            if note_data.topic not in progress.topics_learned:
                topics = progress.topics_learned or []
                topics.append(note_data.topic)
                progress.topics_learned = topics

            db.commit()

        return {
            "id": study_note.id,
            "title": study_note.title,
            "topic": study_note.topic,
            "subject": study_note.subject,
            "keywords": study_note.keywords,
            "bullets": study_note.bullets,
            "formulas": study_note.formulas,
            "definitions": study_note.definitions,
            "flashcards": study_note.flashcards,
            "created_at": study_note.created_at
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/from-scan/{scan_id}", response_model=NoteResponse)
async def create_notes_from_scan(
    scan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create study notes from a homework scan"""
    # Get homework scan
    scan = db.query(HomeworkScan).filter(
        HomeworkScan.id == scan_id,
        HomeworkScan.user_id == current_user.id
    ).first()

    if not scan:
        raise HTTPException(status_code=404, detail="Homework scan not found")

    # Build notes from question and solution
    content = f"{scan.question_text}\n\n"
    if scan.solution_text:
        content += f"Solution: {scan.solution_text}"

    try:
        result = notes_builder.build_notes(
            content=content,
            subject=scan.subject or "general",
            include_flashcards=True
        )

        if not result.get('success'):
            raise HTTPException(status_code=500, detail=result.get('error'))

        notes_data = result.get('notes', {})

        # Save to database
        study_note = StudyNote(
            user_id=current_user.id,
            title=notes_data.get('title', f'Notes from homework'),
            topic=notes_data.get('topic', scan.subject),
            subject=scan.subject,
            keywords=notes_data.get('keywords', []),
            bullets=notes_data.get('key_points', []),
            formulas=notes_data.get('formulas', []),
            definitions=notes_data.get('definitions', {}),
            flashcards=notes_data.get('flashcards', []),
            source_scan_id=scan_id
        )

        db.add(study_note)
        db.commit()
        db.refresh(study_note)

        return {
            "id": study_note.id,
            "title": study_note.title,
            "topic": study_note.topic,
            "subject": study_note.subject,
            "keywords": study_note.keywords,
            "bullets": study_note.bullets,
            "formulas": study_note.formulas,
            "definitions": study_note.definitions,
            "flashcards": study_note.flashcards,
            "created_at": study_note.created_at
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/flashcards")
async def generate_flashcards(
    flashcard_data: FlashcardCreate,
    current_user: User = Depends(get_current_user)
):
    """Generate flashcards from content"""
    try:
        result = notes_builder.create_flashcards(
            content=flashcard_data.content,
            count=flashcard_data.count,
            subject=flashcard_data.subject
        )

        if not result.get('success'):
            raise HTTPException(status_code=500, detail=result.get('error'))

        return {
            "flashcards": result.get('flashcards', [])
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def get_all_notes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    subject: Optional[str] = None,
    limit: int = 20,
    offset: int = 0
):
    """Get user's study notes"""
    query = db.query(StudyNote).filter(StudyNote.user_id == current_user.id)

    if subject:
        query = query.filter(StudyNote.subject == subject)

    notes = query.order_by(StudyNote.created_at.desc()).offset(offset).limit(limit).all()

    return {
        "notes": [
            {
                "id": note.id,
                "title": note.title,
                "topic": note.topic,
                "subject": note.subject,
                "created_at": note.created_at.isoformat()
            }
            for note in notes
        ],
        "total": query.count()
    }


@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific study note"""
    note = db.query(StudyNote).filter(
        StudyNote.id == note_id,
        StudyNote.user_id == current_user.id
    ).first()

    if not note:
        raise HTTPException(status_code=404, detail="Study note not found")

    return {
        "id": note.id,
        "title": note.title,
        "topic": note.topic,
        "subject": note.subject,
        "keywords": note.keywords,
        "bullets": note.bullets,
        "formulas": note.formulas,
        "definitions": note.definitions,
        "flashcards": note.flashcards,
        "created_at": note.created_at
    }


@router.delete("/{note_id}")
async def delete_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a study note"""
    note = db.query(StudyNote).filter(
        StudyNote.id == note_id,
        StudyNote.user_id == current_user.id
    ).first()

    if not note:
        raise HTTPException(status_code=404, detail="Study note not found")

    db.delete(note)
    db.commit()

    return {"message": "Note deleted successfully"}
