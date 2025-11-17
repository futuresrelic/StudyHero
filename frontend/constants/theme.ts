// Design System - Colors, Typography, Spacing

export const Colors = {
  // Primary Colors
  primary: '#4A6FFF',
  primaryDark: '#3A5FEF',
  primaryLight: '#6A8FFF',

  // Secondary Colors
  secondary: '#7F56D9',
  secondaryDark: '#6F46C9',
  secondaryLight: '#8F66E9',

  // Accent
  accent: '#00E676', // Neon green
  accentDark: '#00C766',
  accentLight: '#20F686',

  // Background
  background: '#FFFFFF',
  backgroundDark: '#F5F7FA',
  backgroundDarker: '#E5E7EA',

  // Text
  text: '#1A1A1A',
  textSecondary: '#6B7280',
  textTertiary: '#9CA3AF',
  textLight: '#FFFFFF',

  // Status
  success: '#10B981',
  warning: '#F59E0B',
  error: '#EF4444',
  info: '#3B82F6',

  // UI Elements
  border: '#E5E7EB',
  borderDark: '#D1D5DB',
  shadow: 'rgba(0, 0, 0, 0.1)',
  overlay: 'rgba(0, 0, 0, 0.5)',

  // Dark Mode
  dark: {
    background: '#1A1A1A',
    backgroundDark: '#121212',
    backgroundLighter: '#2A2A2A',
    text: '#FFFFFF',
    textSecondary: '#9CA3AF',
    border: '#374151',
  }
};

export const Typography = {
  // Font Families
  fontFamily: {
    regular: 'System',
    medium: 'System',
    semibold: 'System',
    bold: 'System',
  },

  // Font Sizes
  fontSize: {
    xs: 12,
    sm: 14,
    base: 16,
    lg: 18,
    xl: 20,
    '2xl': 24,
    '3xl': 30,
    '4xl': 36,
    '5xl': 48,
  },

  // Font Weights
  fontWeight: {
    regular: '400' as const,
    medium: '500' as const,
    semibold: '600' as const,
    bold: '700' as const,
    extrabold: '800' as const,
  },

  // Line Heights
  lineHeight: {
    tight: 1.2,
    normal: 1.5,
    relaxed: 1.75,
  }
};

export const Spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  '2xl': 48,
  '3xl': 64,
};

export const BorderRadius = {
  xs: 4,
  sm: 8,
  md: 12,
  lg: 16,
  xl: 20,
  full: 9999,
};

export const Shadow = {
  sm: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 2,
    elevation: 2,
  },
  md: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 4,
  },
  lg: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.15,
    shadowRadius: 8,
    elevation: 8,
  },
  xl: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.2,
    shadowRadius: 16,
    elevation: 16,
  },
};

export const Layout = {
  screenPadding: Spacing.md,
  cardPadding: Spacing.md,
  maxWidth: 600,
};

// Subject Colors
export const SubjectColors = {
  math: '#FF6B6B',
  science: '#4ECDC4',
  history: '#FFE66D',
  english: '#95E1D3',
  general: '#A8DADC',
};

// Grade/Score Colors
export const GradeColors = {
  A: '#10B981',
  B: '#3B82F6',
  C: '#F59E0B',
  D: '#EF4444',
  F: '#991B1B',
};
