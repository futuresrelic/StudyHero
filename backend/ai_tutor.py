from anthropic import Anthropic
from typing import List, Dict
from config import settings
import json


class AITutor:
    """AI-powered tutor using Claude API"""

    def __init__(self):
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = "claude-3-5-sonnet-20241022"

    def generate_explanation(
        self,
        question: str,
        subject: str,
        school_level: str = "high",
        detail_level: str = "medium"
    ) -> Dict:
        """Generate step-by-step explanation for a question"""

        system_prompt = f"""You are StudyHero, an expert AI tutor for students.
You help {school_level} school students understand homework questions.
Your explanations should be:
- Clear and age-appropriate for {school_level} school
- Step-by-step and easy to follow
- Encouraging and supportive
- Free from profanity and inappropriate content

Subject area: {subject}
Detail level: {detail_level}"""

        user_prompt = f"""Please explain how to solve this problem step by step:

{question}

Provide:
1. A brief overview of the concept
2. Step-by-step solution with explanations
3. The final answer
4. A tip or trick to remember

Format your response as JSON with this structure:
{{
  "concept": "brief concept explanation",
  "steps": [
    {{"step": 1, "action": "what to do", "explanation": "why we do it"}},
    ...
  ],
  "answer": "final answer",
  "tip": "helpful tip"
}}"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )

            content = response.content[0].text

            # Try to parse as JSON
            try:
                result = json.loads(content)
            except json.JSONDecodeError:
                # If not JSON, structure the response
                result = {
                    "concept": "Problem explanation",
                    "steps": [],
                    "answer": content,
                    "tip": "Review similar problems to strengthen understanding."
                }

            return {
                'success': True,
                'explanation': result,
                'tokens_used': response.usage.input_tokens + response.usage.output_tokens
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def chat(
        self,
        message: str,
        conversation_history: List[Dict],
        subject: str = "general",
        school_level: str = "high"
    ) -> Dict:
        """Have a conversation with the AI tutor"""

        system_prompt = f"""You are StudyHero, a friendly AI tutor for {school_level} school students.
You help students learn and understand difficult concepts.
You are:
- Patient and encouraging
- Clear and concise
- Age-appropriate for {school_level} school students
- Safe (no profanity, inappropriate content, or unsafe advice)
- Focused on education and learning

Subject focus: {subject}

Remember conversation context and build upon previous messages.
If students seem frustrated, offer encouragement.
If they're doing well, celebrate their progress!"""

        # Format conversation history for Claude
        messages = []
        for msg in conversation_history[-10:]:  # Last 10 messages for context
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

        # Add current message
        messages.append({
            "role": "user",
            "content": message
        })

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                system=system_prompt,
                messages=messages
            )

            reply = response.content[0].text

            return {
                'success': True,
                'reply': reply,
                'tokens_used': response.usage.input_tokens + response.usage.output_tokens
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def rewrite_text(
        self,
        text: str,
        style: str = "simplified",
        reading_level: str = "5th grade"
    ) -> Dict:
        """Rewrite text in different styles"""

        style_prompts = {
            "simplified": f"Rewrite this text in simple, clear language appropriate for {reading_level}.",
            "expanded": "Expand this text with more details and examples.",
            "summarized": "Summarize this text into key points.",
            "kid_friendly": "Rewrite this text in a fun, easy-to-understand way for kids.",
            "academic": "Rewrite this text in a formal, academic style.",
            "bullet_points": "Convert this text into clear bullet points."
        }

        prompt = style_prompts.get(style, style_prompts["simplified"])

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                messages=[
                    {
                        "role": "user",
                        "content": f"{prompt}\n\nOriginal text:\n{text}"
                    }
                ]
            )

            rewritten = response.content[0].text

            return {
                'success': True,
                'original': text,
                'rewritten': rewritten,
                'style': style,
                'tokens_used': response.usage.input_tokens + response.usage.output_tokens
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def explain_like_im(self, text: str, age: int = 10) -> Dict:
        """Explain concept like explaining to a child"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                messages=[
                    {
                        "role": "user",
                        "content": f"Explain this concept like I'm {age} years old. Use simple words, fun examples, and maybe an analogy:\n\n{text}"
                    }
                ]
            )

            explanation = response.content[0].text

            return {
                'success': True,
                'explanation': explanation,
                'age_level': age,
                'tokens_used': response.usage.input_tokens + response.usage.output_tokens
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def generate_study_plan(
        self,
        topics: List[str],
        duration_days: int = 7,
        school_level: str = "high"
    ) -> Dict:
        """Generate a personalized study plan"""

        topics_str = "\n".join(f"- {topic}" for topic in topics)

        prompt = f"""Create a {duration_days}-day study plan for a {school_level} school student covering these topics:

{topics_str}

Provide a day-by-day breakdown with:
- What to study each day
- Estimated time needed
- Practice activities
- Review sessions

Format as JSON:
{{
  "plan": [
    {{"day": 1, "topic": "...", "activities": [...], "duration_minutes": 30}},
    ...
  ],
  "tips": ["tip1", "tip2"]
}}"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            content = response.content[0].text

            try:
                plan = json.loads(content)
            except json.JSONDecodeError:
                plan = {
                    "plan": [],
                    "tips": ["Review the generated plan carefully"],
                    "raw_content": content
                }

            return {
                'success': True,
                'study_plan': plan,
                'tokens_used': response.usage.input_tokens + response.usage.output_tokens
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


# Create singleton
ai_tutor = AITutor()
