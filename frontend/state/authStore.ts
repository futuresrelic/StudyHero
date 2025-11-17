import { create } from 'zustand';
import * as SecureStore from 'expo-secure-store';
import { User, AuthResponse } from '@/types';
import { STORAGE_KEYS } from '@/constants/config';

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;

  // Actions
  setAuth: (data: AuthResponse) => Promise<void>;
  setUser: (user: User) => void;
  logout: () => Promise<void>;
  loadAuth: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: null,
  isAuthenticated: false,
  isLoading: true,

  setAuth: async (data: AuthResponse) => {
    const { access_token, user } = data;

    // Save to secure storage
    await SecureStore.setItemAsync(STORAGE_KEYS.authToken, access_token);
    await SecureStore.setItemAsync(STORAGE_KEYS.user, JSON.stringify(user));

    set({
      token: access_token,
      user,
      isAuthenticated: true,
      isLoading: false,
    });
  },

  setUser: (user: User) => {
    set({ user });
  },

  logout: async () => {
    // Clear secure storage
    await SecureStore.deleteItemAsync(STORAGE_KEYS.authToken);
    await SecureStore.deleteItemAsync(STORAGE_KEYS.user);

    set({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,
    });
  },

  loadAuth: async () => {
    try {
      const token = await SecureStore.getItemAsync(STORAGE_KEYS.authToken);
      const userJson = await SecureStore.getItemAsync(STORAGE_KEYS.user);

      if (token && userJson) {
        const user = JSON.parse(userJson);
        set({
          token,
          user,
          isAuthenticated: true,
          isLoading: false,
        });
      } else {
        set({ isLoading: false });
      }
    } catch (error) {
      console.error('Failed to load auth:', error);
      set({ isLoading: false });
    }
  },
}));
