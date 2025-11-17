from anthropic import Anthropic
from typing import Dict, List
from config import settings
import json
import random


class QuizGenerator:
    """Generate quizzes from topics or content"""

    def __init__(self):
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = "claude-3-5-sonnet-20241022"

    def generate_quiz(
        self,
        topic: str,
        subject: str,
        difficulty: str = "medium",
        num_questions: int = 10,
        question_types: List[str] = None
    ) -> Dict:
        """Generate a quiz on a given topic"""

        if question_types is None:
            question_types = ["multiple_choice", "true_false", "fill_blank"]

        prompt = f"""Generate a {difficulty} difficulty quiz on the topic: {topic} (Subject: {subject})

Create {num_questions} questions with these types: {', '.join(question_types)}

Requirements:
- Mix question types
- Include clear, unambiguous questions
- Provide 4 options for multiple choice (A, B, C, D)
- Include the correct answer
- Add brief explanations for answers
- Make questions age-appropriate and educational

Format as JSON:
{{
  "quiz_title": "Quiz title",
  "questions": [
    {{
      "id": 1,
      "type": "multiple_choice",
      "question": "What is...?",
      "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
      "correct_answer": "A",
      "explanation": "Because..."
    }},
    {{
      "id": 2,
      "type": "true_false",
      "question": "Statement is true or false?",
      "correct_answer": "true",
      "explanation": "This is true because..."
    }},
    {{
      "id": 3,
      "type": "fill_blank",
      "question": "The process of ___ is important.",
      "correct_answer": "photosynthesis",
      "explanation": "Photosynthesis is..."
    }}
  ]
}}"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=3000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            content = response.content[0].text

            # Parse JSON
            try:
                quiz_data = json.loads(content)
            except json.JSONDecodeError:
                # Fallback: create structured response
                quiz_data = {
                    "quiz_title": f"Quiz: {topic}",
                    "questions": [],
                    "error": "Could not parse quiz format",
                    "raw_content": content
                }

            return {
                'success': True,
                'quiz': quiz_data,
                'topic': topic,
                'difficulty': difficulty,
                'tokens_used': response.usage.input_tokens + response.usage.output_tokens
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def generate_from_content(
        self,
        content: str,
        num_questions: int = 5,
        difficulty: str = "medium"
    ) -> Dict:
        """Generate quiz questions from provided content/notes"""

        prompt = f"""Based on this content, generate {num_questions} quiz questions at {difficulty} difficulty:

{content}

Create a mix of multiple choice, true/false, and fill-in-the-blank questions.
Focus on key concepts and important information from the content.

Format as JSON:
{{
  "quiz_title": "Title based on content",
  "questions": [
    {{
      "id": 1,
      "type": "multiple_choice",
      "question": "...",
      "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
      "correct_answer": "A",
      "explanation": "..."
    }},
    ...
  ]
}}"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            content_result = response.content[0].text

            try:
                quiz_data = json.loads(content_result)
            except json.JSONDecodeError:
                quiz_data = {
                    "quiz_title": "Generated Quiz",
                    "questions": [],
                    "raw_content": content_result
                }

            return {
                'success': True,
                'quiz': quiz_data,
                'tokens_used': response.usage.input_tokens + response.usage.output_tokens
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def grade_quiz(
        self,
        questions: List[Dict],
        user_answers: List[str]
    ) -> Dict:
        """Grade a quiz submission"""

        if len(questions) != len(user_answers):
            return {
                'success': False,
                'error': 'Number of answers does not match number of questions'
            }

        total_questions = len(questions)
        correct_count = 0
        results = []

        for i, (question, user_answer) in enumerate(zip(questions, user_answers)):
            correct_answer = question.get('correct_answer', '').lower().strip()
            user_answer_clean = user_answer.lower().strip()

            # For multiple choice, accept just the letter or full option
            if question.get('type') == 'multiple_choice':
                if len(user_answer_clean) == 1:  # Just letter
                    is_correct = user_answer_clean == correct_answer.lower()
                else:  # Full option
                    is_correct = user_answer_clean.startswith(correct_answer.lower())
            else:
                is_correct = user_answer_clean == correct_answer

            if is_correct:
                correct_count += 1

            results.append({
                'question_id': question.get('id', i + 1),
                'question': question.get('question', ''),
                'user_answer': user_answer,
                'correct_answer': question.get('correct_answer', ''),
                'is_correct': is_correct,
                'explanation': question.get('explanation', '')
            })

        score = (correct_count / total_questions) * 100

        # Determine grade
        if score >= 90:
            grade = 'A'
            message = '🌟 Excellent work!'
        elif score >= 80:
            grade = 'B'
            message = '👍 Great job!'
        elif score >= 70:
            grade = 'C'
            message = '✓ Good effort!'
        elif score >= 60:
            grade = 'D'
            message = 'Keep practicing!'
        else:
            grade = 'F'
            message = 'Review the material and try again!'

        return {
            'success': True,
            'score': score,
            'grade': grade,
            'correct_count': correct_count,
            'total_questions': total_questions,
            'message': message,
            'results': results
        }

    def generate_practice_problems(
        self,
        topic: str,
        difficulty: str,
        count: int = 5
    ) -> Dict:
        """Generate practice problems for a topic"""

        prompt = f"""Generate {count} practice problems for: {topic}
Difficulty: {difficulty}

For each problem:
1. State the problem clearly
2. Provide a detailed solution
3. Include step-by-step explanation

Format as JSON:
{{
  "problems": [
    {{
      "id": 1,
      "problem": "...",
      "solution": "...",
      "steps": ["step1", "step2", ...]
    }},
    ...
  ]
}}"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            content = response.content[0].text

            try:
                problems_data = json.loads(content)
            except json.JSONDecodeError:
                problems_data = {
                    "problems": [],
                    "raw_content": content
                }

            return {
                'success': True,
                'practice_problems': problems_data,
                'tokens_used': response.usage.input_tokens + response.usage.output_tokens
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


# Create singleton
quiz_generator = QuizGenerator()
