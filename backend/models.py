from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, JSON, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from typing import Optional

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    school_level = Column(String, nullable=True)  # elementary, middle, high, college
    subscription_status = Column(String, default="free")  # free, premium
    subscription_id = Column(String, nullable=True)
    subscription_expires_at = Column(DateTime, nullable=True)
    trial_used = Column(Boolean, default=False)
    trial_ends_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    homework_scans = relationship("HomeworkScan", back_populates="user", cascade="all, delete-orphan")
    study_notes = relationship("StudyNote", back_populates="user", cascade="all, delete-orphan")
    quizzes = relationship("Quiz", back_populates="user", cascade="all, delete-orphan")
    progress = relationship("Progress", back_populates="user", uselist=False, cascade="all, delete-orphan")
    chat_history = relationship("ChatMessage", back_populates="user", cascade="all, delete-orphan")


class HomeworkScan(Base):
    __tablename__ = "homework_scans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    image_url = Column(String, nullable=True)
    subject = Column(String, nullable=True)  # math, science, history, english, etc.
    difficulty = Column(String, nullable=True)  # easy, medium, hard
    solution_text = Column(Text, nullable=True)
    explanation_steps = Column(JSON, nullable=True)  # Array of step objects
    confidence_score = Column(Float, nullable=True)
    processing_time_ms = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="homework_scans")


class StudyNote(Base):
    __tablename__ = "study_notes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    topic = Column(String, nullable=False)
    subject = Column(String, nullable=True)
    keywords = Column(JSON, nullable=True)  # Array of keywords
    bullets = Column(JSON, nullable=True)  # Array of bullet points
    formulas = Column(JSON, nullable=True)  # Array of formulas
    definitions = Column(JSON, nullable=True)  # Dict of term: definition
    flashcards = Column(JSON, nullable=True)  # Array of {front, back}
    source_scan_id = Column(Integer, ForeignKey("homework_scans.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="study_notes")


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic = Column(String, nullable=False)
    subject = Column(String, nullable=True)
    difficulty = Column(String, default="medium")  # easy, medium, hard
    questions = Column(JSON, nullable=False)  # Array of question objects
    user_answers = Column(JSON, nullable=True)  # Array of user's answers
    score = Column(Float, nullable=True)  # 0-100
    total_questions = Column(Integer, nullable=False)
    correct_answers = Column(Integer, nullable=True)
    time_taken_seconds = Column(Integer, nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="quizzes")


class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_activity_date = Column(DateTime, nullable=True)
    total_minutes_studied = Column(Integer, default=0)
    total_questions_solved = Column(Integer, default=0)
    total_quizzes_completed = Column(Integer, default=0)
    total_notes_created = Column(Integer, default=0)
    topics_learned = Column(JSON, default=list)  # Array of topics
    weekly_breakdown = Column(JSON, default=dict)  # {week: {minutes, questions, etc}}
    subject_breakdown = Column(JSON, default=dict)  # {subject: count}
    achievement_badges = Column(JSON, default=list)  # Array of badge names
    level = Column(Integer, default=1)
    experience_points = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="progress")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    conversation_id = Column(String, nullable=False, index=True)
    role = Column(String, nullable=False)  # user, assistant
    content = Column(Text, nullable=False)
    subject = Column(String, nullable=True)
    tokens_used = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="chat_history")


class RateLimit(Base):
    __tablename__ = "rate_limits"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, nullable=False, index=True)
    request_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
