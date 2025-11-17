// App Configuration

import Constants from 'expo-constants';

// Get environment variables
const ENV = Constants.expoConfig?.extra || {};

export const API_URL = ENV.API_URL || 'http://localhost:8000';
export const STRIPE_PUBLISHABLE_KEY = ENV.STRIPE_PUBLISHABLE_KEY || 'pk_test_';

export const APP_NAME = 'StudyHero';
export const APP_VERSION = '1.0.0';

// API Endpoints
export const API_ENDPOINTS = {
  // Auth
  register: '/auth/register',
  login: '/auth/login',
  me: '/auth/me',

  // Homework
  scanHomework: '/homework/scan',
  solveHomework: (id: number) => `/homework/solve/${id}`,
  getHomework: (id: number) => `/homework/${id}`,
  homeworkHistory: '/homework/history',

  // Quiz
  generateQuiz: '/quiz/generate',
  submitQuiz: '/quiz/submit',
  getQuiz: (id: number) => `/quiz/${id}`,
  quizHistory: '/quiz/history',
  practicePro blems: '/quiz/practice',

  // Notes
  createNotes: '/notes/create',
  fromScan: (id: number) => `/notes/from-scan/${id}`,
  generateFlashcards: '/notes/flashcards',
  getNotes: '/notes/',
  getNote: (id: number) => `/notes/${id}`,

  // Tutor
  chat: '/tutor/chat',
  conversations: '/tutor/conversations',
  getConversation: (id: string) => `/tutor/conversations/${id}`,
  rewrite: '/tutor/rewrite',
  explainSimple: '/tutor/explain-simple',
  studyPlan: '/tutor/study-plan',

  // Subscription
  createCheckout: '/subscription/create-checkout-session',
  createPortal: '/subscription/create-portal-session',
  subscriptionStatus: '/subscription/status',
  plans: '/subscription/plans',

  // Progress
  progress: '/progress/',
  logStudyTime: '/progress/log-study-time',
  leaderboard: '/progress/leaderboard',
  achievements: '/progress/achievements',
  stats: '/progress/stats',
};

// School Levels
export const SCHOOL_LEVELS = [
  { value: 'elementary', label: 'Elementary School', icon: '🎒' },
  { value: 'middle', label: 'Middle School', icon: '📚' },
  { value: 'high', label: 'High School', icon: '🎓' },
  { value: 'college', label: 'College', icon: '🏛️' },
];

// Subjects
export const SUBJECTS = [
  { value: 'math', label: 'Math', icon: '➗', color: '#FF6B6B' },
  { value: 'science', label: 'Science', icon: '🔬', color: '#4ECDC4' },
  { value: 'history', label: 'History', icon: '📜', color: '#FFE66D' },
  { value: 'english', label: 'English', icon: '📖', color: '#95E1D3' },
  { value: 'general', label: 'General', icon: '📝', color: '#A8DADC' },
];

// Difficulties
export const DIFFICULTIES = [
  { value: 'easy', label: 'Easy', icon: '😊' },
  { value: 'medium', label: 'Medium', icon: '🤔' },
  { value: 'hard', label: 'Hard', icon: '😰' },
];

// Free tier limits
export const FREE_TIER_LIMITS = {
  dailyScans: 5,
  quizzes: 3,
};

// Cache keys for AsyncStorage
export const STORAGE_KEYS = {
  authToken: '@studyhero:auth_token',
  user: '@studyhero:user',
  onboardingCompleted: '@studyhero:onboarding_completed',
};
