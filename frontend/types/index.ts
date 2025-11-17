// Type definitions for StudyHero app

export interface User {
  id: number;
  email: string;
  full_name?: string;
  school_level?: string;
  subscription_status: 'free' | 'premium';
  trial_ends_at?: string;
  subscription_expires_at?: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface HomeworkScan {
  id: number;
  question_text: string;
  subject: string;
  solution_text?: string;
  explanation_steps?: ExplanationStep[];
  confidence_score?: number;
  created_at: string;
}

export interface ExplanationStep {
  step: number;
  action: string;
  expression?: string;
  explanation: string;
}

export interface Quiz {
  id: number;
  topic: string;
  subject: string;
  difficulty: string;
  questions: QuizQuestion[];
  score?: number;
  completed: boolean;
  created_at: string;
}

export interface QuizQuestion {
  id: number;
  type: 'multiple_choice' | 'true_false' | 'fill_blank';
  question: string;
  options?: string[];
  correct_answer: string;
  explanation: string;
}

export interface StudyNote {
  id: number;
  title: string;
  topic: string;
  subject: string;
  keywords?: string[];
  bullets?: string[];
  formulas?: Formula[];
  definitions?: Record<string, string>;
  flashcards?: Flashcard[];
  created_at: string;
}

export interface Formula {
  name: string;
  formula: string;
  explanation: string;
}

export interface Flashcard {
  front: string;
  back: string;
}

export interface Progress {
  current_streak: number;
  longest_streak: number;
  total_minutes_studied: number;
  total_questions_solved: number;
  total_quizzes_completed: number;
  total_notes_created: number;
  level: number;
  experience_points: number;
  topics_learned: string[];
  achievement_badges: string[];
  subject_breakdown: Record<string, number>;
  last_7_days: {
    scans: number;
    quizzes: number;
    notes: number;
  };
  weekly_breakdown: Record<string, any>;
}

export interface Achievement {
  id: string;
  name: string;
  description: string;
  icon: string;
  requirement: boolean;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  created_at?: string;
}

export interface Conversation {
  conversation_id: string;
  last_message: string;
  message_count: number;
  preview: string;
}

export interface SubscriptionPlan {
  id: string;
  name: string;
  price: number;
  currency: string;
  interval: string;
  features: string[];
}

export interface SubscriptionStatus {
  subscription_status: string;
  is_premium: boolean;
  in_trial: boolean;
  trial_ends_at?: string;
  subscription_expires_at?: string;
}

export type SchoolLevel = 'elementary' | 'middle' | 'high' | 'college';
export type Subject = 'math' | 'science' | 'history' | 'english' | 'general';
export type Difficulty = 'easy' | 'medium' | 'hard';
