import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';
import { API_URL, API_ENDPOINTS } from '@/constants/config';
import { useAuthStore } from '@/state/authStore';

// Create axios instance
const api: AxiosInstance = axios.create({
  baseURL: API_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = useAuthStore.getState().token;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      await useAuthStore.getState().logout();
    }
    return Promise.reject(error);
  }
);

// API functions

export const authAPI = {
  register: async (data: { email: string; password: string; full_name?: string; school_level?: string }) => {
    const response = await api.post(API_ENDPOINTS.register, data);
    return response.data;
  },

  login: async (data: { email: string; password: string }) => {
    const response = await api.post(API_ENDPOINTS.login, data);
    return response.data;
  },

  getMe: async () => {
    const response = await api.get(API_ENDPOINTS.me);
    return response.data;
  },
};

export const homeworkAPI = {
  scanHomework: async (file: File | Blob) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post(API_ENDPOINTS.scanHomework, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  solveHomework: async (id: number) => {
    const response = await api.post(API_ENDPOINTS.solveHomework(id));
    return response.data;
  },

  getHomework: async (id: number) => {
    const response = await api.get(API_ENDPOINTS.getHomework(id));
    return response.data;
  },

  getHistory: async (limit = 20, offset = 0) => {
    const response = await api.get(API_ENDPOINTS.homeworkHistory, {
      params: { limit, offset },
    });
    return response.data;
  },
};

export const quizAPI = {
  generateQuiz: async (data: {
    topic: string;
    subject: string;
    difficulty?: string;
    num_questions?: number;
  }) => {
    const response = await api.post(API_ENDPOINTS.generateQuiz, data);
    return response.data;
  },

  submitQuiz: async (data: { quiz_id: number; answers: string[] }) => {
    const response = await api.post(API_ENDPOINTS.submitQuiz, data);
    return response.data;
  },

  getQuiz: async (id: number) => {
    const response = await api.get(API_ENDPOINTS.getQuiz(id));
    return response.data;
  },

  getHistory: async (limit = 20, offset = 0) => {
    const response = await api.get(API_ENDPOINTS.quizHistory, {
      params: { limit, offset },
    });
    return response.data;
  },

  getPracticeProblems: async (topic: string, difficulty: string, count = 5) => {
    const response = await api.post(API_ENDPOINTS.practiceProblems, null, {
      params: { topic, difficulty, count },
    });
    return response.data;
  },
};

export const notesAPI = {
  createNotes: async (data: {
    title: string;
    topic: string;
    subject: string;
    content: string;
    source_scan_id?: number;
  }) => {
    const response = await api.post(API_ENDPOINTS.createNotes, data);
    return response.data;
  },

  createFromScan: async (scanId: number) => {
    const response = await api.post(API_ENDPOINTS.fromScan(scanId));
    return response.data;
  },

  generateFlashcards: async (data: { content: string; subject?: string; count?: number }) => {
    const response = await api.post(API_ENDPOINTS.generateFlashcards, data);
    return response.data;
  },

  getNotes: async (subject?: string, limit = 20, offset = 0) => {
    const response = await api.get(API_ENDPOINTS.getNotes, {
      params: { subject, limit, offset },
    });
    return response.data;
  },

  getNote: async (id: number) => {
    const response = await api.get(API_ENDPOINTS.getNote(id));
    return response.data;
  },
};

export const tutorAPI = {
  chat: async (data: { message: string; conversation_id?: string; subject?: string }) => {
    const response = await api.post(API_ENDPOINTS.chat, data);
    return response.data;
  },

  getConversations: async () => {
    const response = await api.get(API_ENDPOINTS.conversations);
    return response.data;
  },

  getConversation: async (id: string) => {
    const response = await api.get(API_ENDPOINTS.getConversation(id));
    return response.data;
  },

  rewriteText: async (data: { text: string; style?: string; reading_level?: string }) => {
    const response = await api.post(API_ENDPOINTS.rewrite, data);
    return response.data;
  },

  explainSimple: async (data: { text: string; age?: number }) => {
    const response = await api.post(API_ENDPOINTS.explainSimple, data);
    return response.data;
  },

  createStudyPlan: async (data: { topics: string[]; duration_days?: number }) => {
    const response = await api.post(API_ENDPOINTS.studyPlan, data);
    return response.data;
  },
};

export const subscriptionAPI = {
  createCheckoutSession: async (plan: string) => {
    const response = await api.post(API_ENDPOINTS.createCheckout, { plan });
    return response.data;
  },

  createPortalSession: async (returnUrl: string) => {
    const response = await api.post(API_ENDPOINTS.createPortal, { return_url: returnUrl });
    return response.data;
  },

  getStatus: async () => {
    const response = await api.get(API_ENDPOINTS.subscriptionStatus);
    return response.data;
  },

  getPlans: async () => {
    const response = await api.get(API_ENDPOINTS.plans);
    return response.data;
  },
};

export const progressAPI = {
  getProgress: async () => {
    const response = await api.get(API_ENDPOINTS.progress);
    return response.data;
  },

  logStudyTime: async (minutes: number) => {
    const response = await api.post(API_ENDPOINTS.logStudyTime, null, {
      params: { minutes },
    });
    return response.data;
  },

  getLeaderboard: async (limit = 10) => {
    const response = await api.get(API_ENDPOINTS.leaderboard, {
      params: { limit },
    });
    return response.data;
  },

  getAchievements: async () => {
    const response = await api.get(API_ENDPOINTS.achievements);
    return response.data;
  },

  getStats: async () => {
    const response = await api.get(API_ENDPOINTS.stats);
    return response.data;
  },
};

export default api;
