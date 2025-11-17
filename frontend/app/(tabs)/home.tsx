import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { useRouter } from 'expo-router';
import { useQuery } from '@tanstack/react-query';
import { Card } from '@/components/Card';
import { Button } from '@/components/Button';
import { useAuthStore } from '@/state/authStore';
import { progressAPI, homeworkAPI } from '@/utils/api';
import { Colors, Typography, Spacing } from '@/constants/theme';

export default function HomeScreen() {
  const router = useRouter();
  const user = useAuthStore((state) => state.user);

  const { data: progress } = useQuery({
    queryKey: ['progress'],
    queryFn: progressAPI.getProgress,
  });

  const { data: recentScans } = useQuery({
    queryKey: ['homework', 'recent'],
    queryFn: () => homeworkAPI.getHistory(5, 0),
  });

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.greeting}>Hello, {user?.full_name || 'Student'}! 👋</Text>
        <Text style={styles.subheading}>Ready to learn today?</Text>
      </View>

      {/* Quick Stats */}
      <View style={styles.statsRow}>
        <Card style={styles.statCard}>
          <Text style={styles.statValue}>{progress?.current_streak || 0}🔥</Text>
          <Text style={styles.statLabel}>Day Streak</Text>
        </Card>
        <Card style={styles.statCard}>
          <Text style={styles.statValue}>{progress?.total_questions_solved || 0}</Text>
          <Text style={styles.statLabel}>Problems Solved</Text>
        </Card>
        <Card style={styles.statCard}>
          <Text style={styles.statValue}>Lv {progress?.level || 1}</Text>
          <Text style={styles.statLabel}>Level</Text>
        </Card>
      </View>

      {/* Main Actions */}
      <Card style={styles.actionCard}>
        <Text style={styles.sectionTitle}>Get Started</Text>

        <TouchableOpacity
          style={styles.actionButton}
          onPress={() => router.push('/scan')}
        >
          <Text style={styles.actionIcon}>📸</Text>
          <View style={styles.actionContent}>
            <Text style={styles.actionTitle}>Scan Homework</Text>
            <Text style={styles.actionSubtitle}>Take a photo to get instant help</Text>
          </View>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.actionButton}
          onPress={() => router.push('/quiz')}
        >
          <Text style={styles.actionIcon}>🎯</Text>
          <View style={styles.actionContent}>
            <Text style={styles.actionTitle}>Take a Quiz</Text>
            <Text style={styles.actionSubtitle}>Test your knowledge</Text>
          </View>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.actionButton}
          onPress={() => router.push('/tutor')}
        >
          <Text style={styles.actionIcon}>💬</Text>
          <View style={styles.actionContent}>
            <Text style={styles.actionTitle}>AI Tutor</Text>
            <Text style={styles.actionSubtitle}>Chat with your study assistant</Text>
          </View>
        </TouchableOpacity>
      </Card>

      {/* Recent Activity */}
      {recentScans?.scans && recentScans.scans.length > 0 && (
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Recent Problems</Text>
          {recentScans.scans.map((scan: any) => (
            <Card
              key={scan.id}
              style={styles.scanCard}
            >
              <TouchableOpacity
                onPress={() => router.push(`/solution/${scan.id}`)}
              >
                <Text style={styles.scanSubject}>{scan.subject}</Text>
                <Text style={styles.scanQuestion} numberOfLines={2}>
                  {scan.question_text}
                </Text>
                <Text style={styles.scanDate}>
                  {new Date(scan.created_at).toLocaleDateString()}
                </Text>
              </TouchableOpacity>
            </Card>
          ))}
        </View>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.backgroundDark,
  },
  header: {
    padding: Spacing.lg,
    backgroundColor: Colors.primary,
  },
  greeting: {
    fontSize: Typography.fontSize['2xl'],
    fontWeight: Typography.fontWeight.bold,
    color: Colors.textLight,
  },
  subheading: {
    fontSize: Typography.fontSize.base,
    color: Colors.textLight,
    opacity: 0.9,
    marginTop: Spacing.xs,
  },
  statsRow: {
    flexDirection: 'row',
    padding: Spacing.md,
    gap: Spacing.sm,
  },
  statCard: {
    flex: 1,
    alignItems: 'center',
    padding: Spacing.md,
  },
  statValue: {
    fontSize: Typography.fontSize['2xl'],
    fontWeight: Typography.fontWeight.bold,
    color: Colors.primary,
  },
  statLabel: {
    fontSize: Typography.fontSize.sm,
    color: Colors.textSecondary,
    marginTop: Spacing.xs,
  },
  actionCard: {
    margin: Spacing.md,
    marginTop: 0,
  },
  sectionTitle: {
    fontSize: Typography.fontSize.lg,
    fontWeight: Typography.fontWeight.semibold,
    color: Colors.text,
    marginBottom: Spacing.md,
  },
  actionButton: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: Spacing.md,
    backgroundColor: Colors.backgroundDark,
    borderRadius: 12,
    marginBottom: Spacing.sm,
  },
  actionIcon: {
    fontSize: 32,
    marginRight: Spacing.md,
  },
  actionContent: {
    flex: 1,
  },
  actionTitle: {
    fontSize: Typography.fontSize.base,
    fontWeight: Typography.fontWeight.semibold,
    color: Colors.text,
  },
  actionSubtitle: {
    fontSize: Typography.fontSize.sm,
    color: Colors.textSecondary,
    marginTop: 2,
  },
  section: {
    padding: Spacing.md,
  },
  scanCard: {
    marginBottom: Spacing.sm,
  },
  scanSubject: {
    fontSize: Typography.fontSize.sm,
    fontWeight: Typography.fontWeight.semibold,
    color: Colors.primary,
    textTransform: 'uppercase',
  },
  scanQuestion: {
    fontSize: Typography.fontSize.base,
    color: Colors.text,
    marginTop: Spacing.xs,
  },
  scanDate: {
    fontSize: Typography.fontSize.sm,
    color: Colors.textSecondary,
    marginTop: Spacing.xs,
  },
});
