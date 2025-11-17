import { useEffect } from 'react';
import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useAuthStore } from '@/state/authStore';
import { Colors } from '@/constants/theme';

// Create React Query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 2,
      staleTime: 1000 * 60 * 5, // 5 minutes
    },
  },
});

export default function RootLayout() {
  const loadAuth = useAuthStore((state) => state.loadAuth);

  useEffect(() => {
    loadAuth();
  }, []);

  return (
    <QueryClientProvider client={queryClient}>
      <StatusBar style="auto" />
      <Stack
        screenOptions={{
          headerStyle: {
            backgroundColor: Colors.primary,
          },
          headerTintColor: Colors.textLight,
          headerTitleStyle: {
            fontWeight: '600',
          },
        }}
      >
        <Stack.Screen name="index" options={{ headerShown: false }} />
        <Stack.Screen name="(auth)" options={{ headerShown: false }} />
        <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
        <Stack.Screen name="scan" options={{ title: 'Scan Homework', presentation: 'modal' }} />
        <Stack.Screen name="solution/[id]" options={{ title: 'Solution' }} />
        <Stack.Screen name="quiz/[id]" options={{ title: 'Quiz' }} />
        <Stack.Screen name="notes/[id]" options={{ title: 'Study Notes' }} />
        <Stack.Screen name="paywall" options={{ title: 'Go Premium', presentation: 'modal' }} />
      </Stack>
    </QueryClientProvider>
  );
}
