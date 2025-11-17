from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid
from database import get_db
from models import User, ChatMessage
from auth import get_current_user
from ai_tutor import ai_tutor

router = APIRouter(prefix="/tutor", tags=["AI Tutor"])


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    subject: Optional[str] = "general"


class TextRewriteRequest(BaseModel):
    text: str
    style: str = "simplified"
    reading_level: str = "5th grade"


class ExplainRequest(BaseModel):
    text: str
    age: int = 10


class StudyPlanRequest(BaseModel):
    topics: List[str]
    duration_days: int = 7


@router.post("/chat")
async def chat_with_tutor(
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Chat with AI tutor"""
    # Get or create conversation ID
    conversation_id = chat_request.conversation_id or str(uuid.uuid4())

    # Get conversation history
    history_messages = db.query(ChatMessage).filter(
        ChatMessage.user_id == current_user.id,
        ChatMessage.conversation_id == conversation_id
    ).order_by(ChatMessage.created_at.asc()).all()

    conversation_history = [
        {"role": msg.role, "content": msg.content}
        for msg in history_messages
    ]

    try:
        # Get AI response
        result = ai_tutor.chat(
            message=chat_request.message,
            conversation_history=conversation_history,
            subject=chat_request.subject,
            school_level=current_user.school_level or "high"
        )

        if not result.get('success'):
            raise HTTPException(status_code=500, detail=result.get('error'))

        reply = result.get('reply')
        tokens_used = result.get('tokens_used', 0)

        # Save user message
        user_message = ChatMessage(
            user_id=current_user.id,
            conversation_id=conversation_id,
            role="user",
            content=chat_request.message,
            subject=chat_request.subject
        )
        db.add(user_message)

        # Save assistant message
        assistant_message = ChatMessage(
            user_id=current_user.id,
            conversation_id=conversation_id,
            role="assistant",
            content=reply,
            subject=chat_request.subject,
            tokens_used=tokens_used
        )
        db.add(assistant_message)

        db.commit()

        return {
            "conversation_id": conversation_id,
            "message": reply,
            "tokens_used": tokens_used
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations")
async def get_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's conversation history"""
    # Get unique conversation IDs with latest message
    from sqlalchemy import func

    conversations = db.query(
        ChatMessage.conversation_id,
        func.max(ChatMessage.created_at).label('last_message'),
        func.count(ChatMessage.id).label('message_count')
    ).filter(
        ChatMessage.user_id == current_user.id
    ).group_by(ChatMessage.conversation_id).order_by(func.max(ChatMessage.created_at).desc()).all()

    result = []
    for conv in conversations:
        # Get first user message for preview
        first_msg = db.query(ChatMessage).filter(
            ChatMessage.user_id == current_user.id,
            ChatMessage.conversation_id == conv.conversation_id,
            ChatMessage.role == "user"
        ).first()

        result.append({
            "conversation_id": conv.conversation_id,
            "last_message": conv.last_message.isoformat(),
            "message_count": conv.message_count,
            "preview": first_msg.content[:100] if first_msg else ""
        })

    return {"conversations": result}


@router.get("/conversations/{conversation_id}")
async def get_conversation(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific conversation"""
    messages = db.query(ChatMessage).filter(
        ChatMessage.user_id == current_user.id,
        ChatMessage.conversation_id == conversation_id
    ).order_by(ChatMessage.created_at.asc()).all()

    if not messages:
        raise HTTPException(status_code=404, detail="Conversation not found")

    return {
        "conversation_id": conversation_id,
        "messages": [
            {
                "role": msg.role,
                "content": msg.content,
                "created_at": msg.created_at.isoformat()
            }
            for msg in messages
        ]
    }


@router.post("/rewrite")
async def rewrite_text(
    request: TextRewriteRequest,
    current_user: User = Depends(get_current_user)
):
    """Rewrite text in different styles"""
    try:
        result = ai_tutor.rewrite_text(
            text=request.text,
            style=request.style,
            reading_level=request.reading_level
        )

        if not result.get('success'):
            raise HTTPException(status_code=500, detail=result.get('error'))

        return {
            "original": result.get('original'),
            "rewritten": result.get('rewritten'),
            "style": result.get('style')
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/explain-simple")
async def explain_like_im(
    request: ExplainRequest,
    current_user: User = Depends(get_current_user)
):
    """Explain concept in simple terms"""
    try:
        result = ai_tutor.explain_like_im(
            text=request.text,
            age=request.age
        )

        if not result.get('success'):
            raise HTTPException(status_code=500, detail=result.get('error'))

        return {
            "explanation": result.get('explanation'),
            "age_level": result.get('age_level')
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/study-plan")
async def create_study_plan(
    request: StudyPlanRequest,
    current_user: User = Depends(get_current_user)
):
    """Create a personalized study plan"""
    try:
        result = ai_tutor.generate_study_plan(
            topics=request.topics,
            duration_days=request.duration_days,
            school_level=current_user.school_level or "high"
        )

        if not result.get('success'):
            raise HTTPException(status_code=500, detail=result.get('error'))

        return result.get('study_plan')

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
