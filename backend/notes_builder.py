from anthropic import Anthropic
from typing import Dict, List
from config import settings
import json
import re


class NotesBuilder:
    """Automatically build study notes from content"""

    def __init__(self):
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = "claude-3-5-sonnet-20241022"

    def build_notes(
        self,
        content: str,
        subject: str = "general",
        include_flashcards: bool = True
    ) -> Dict:
        """Build comprehensive study notes from content"""

        prompt = f"""Analyze this {subject} content and create comprehensive study notes:

{content}

Generate structured study notes with:
1. **Title**: A clear title for this topic
2. **Topic**: Main topic/concept
3. **Keywords**: 5-10 important keywords
4. **Summary**: 2-3 sentence overview
5. **Key Points**: 5-10 bullet points covering main ideas
6. **Formulas**: Any important formulas or equations (if applicable)
7. **Definitions**: Key terms and their definitions
8. **Flashcards**: 5-10 question/answer pairs for memorization (if requested)

Format as JSON:
{{
  "title": "...",
  "topic": "...",
  "subject": "{subject}",
  "keywords": ["keyword1", "keyword2", ...],
  "summary": "...",
  "key_points": [
    "Point 1: ...",
    "Point 2: ...",
    ...
  ],
  "formulas": [
    {{"name": "Formula name", "formula": "x = y + z", "explanation": "..."}},
    ...
  ],
  "definitions": {{
    "term1": "definition1",
    "term2": "definition2",
    ...
  }},
  "flashcards": [
    {{"front": "Question?", "back": "Answer"}},
    ...
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

            content_result = response.content[0].text

            # Parse JSON
            try:
                notes_data = json.loads(content_result)
            except json.JSONDecodeError:
                # Try to extract components manually
                notes_data = self._extract_notes_from_text(content_result, subject)

            return {
                'success': True,
                'notes': notes_data,
                'tokens_used': response.usage.input_tokens + response.usage.output_tokens
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def _extract_notes_from_text(self, text: str, subject: str) -> Dict:
        """Fallback: Extract notes structure from text"""
        return {
            'title': 'Study Notes',
            'topic': subject,
            'subject': subject,
            'keywords': self._extract_keywords(text),
            'summary': text[:200] + '...' if len(text) > 200 else text,
            'key_points': self._extract_bullet_points(text),
            'formulas': [],
            'definitions': {},
            'flashcards': [],
            'raw_content': text
        }

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract potential keywords from text"""
        # Simple keyword extraction - in production use NLP
        words = re.findall(r'\b[A-Z][a-z]+\b', text)
        return list(set(words))[:10]

    def _extract_bullet_points(self, text: str) -> List[str]:
        """Extract bullet points from text"""
        lines = text.split('\n')
        bullets = []
        for line in lines:
            line = line.strip()
            if line.startswith(('-', '•', '*', '+')):
                bullets.append(line[1:].strip())
            elif re.match(r'^\d+\.', line):
                bullets.append(re.sub(r'^\d+\.\s*', '', line))

        return bullets[:10] if bullets else [text[:100]]

    def create_flashcards(
        self,
        content: str,
        count: int = 10,
        subject: str = "general"
    ) -> Dict:
        """Create flashcards from content"""

        prompt = f"""Create {count} flashcards from this {subject} content:

{content}

Each flashcard should:
- Have a clear question on the front
- Have a concise answer on the back
- Focus on key concepts, definitions, or facts
- Be useful for memorization

Format as JSON:
{{
  "flashcards": [
    {{"front": "Question 1?", "back": "Answer 1"}},
    {{"front": "Question 2?", "back": "Answer 2"}},
    ...
  ]
}}"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            content_result = response.content[0].text

            try:
                flashcards_data = json.loads(content_result)
            except json.JSONDecodeError:
                flashcards_data = {
                    "flashcards": [],
                    "raw_content": content_result
                }

            return {
                'success': True,
                'flashcards': flashcards_data.get('flashcards', []),
                'tokens_used': response.usage.input_tokens + response.usage.output_tokens
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def summarize_content(
        self,
        content: str,
        length: str = "medium"
    ) -> Dict:
        """Summarize content into key points"""

        length_instructions = {
            "short": "in 2-3 sentences",
            "medium": "in 1 paragraph (5-7 sentences)",
            "long": "in 2-3 paragraphs with detailed key points"
        }

        instruction = length_instructions.get(length, length_instructions["medium"])

        prompt = f"""Summarize this content {instruction}:

{content}

Focus on the most important information and key takeaways."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            summary = response.content[0].text

            return {
                'success': True,
                'original_length': len(content),
                'summary_length': len(summary),
                'summary': summary,
                'tokens_used': response.usage.input_tokens + response.usage.output_tokens
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def extract_key_concepts(
        self,
        content: str,
        subject: str = "general"
    ) -> Dict:
        """Extract key concepts and definitions"""

        prompt = f"""Extract the key concepts from this {subject} content:

{content}

For each concept, provide:
1. The concept name
2. A clear definition
3. Why it's important

Format as JSON:
{{
  "concepts": [
    {{
      "name": "Concept 1",
      "definition": "...",
      "importance": "..."
    }},
    ...
  ]
}}"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            content_result = response.content[0].text

            try:
                concepts_data = json.loads(content_result)
            except json.JSONDecodeError:
                concepts_data = {
                    "concepts": [],
                    "raw_content": content_result
                }

            return {
                'success': True,
                'concepts': concepts_data.get('concepts', []),
                'tokens_used': response.usage.input_tokens + response.usage.output_tokens
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def create_study_guide(
        self,
        topics: List[str],
        subject: str,
        school_level: str = "high"
    ) -> Dict:
        """Create a comprehensive study guide for multiple topics"""

        topics_str = "\n".join(f"- {topic}" for topic in topics)

        prompt = f"""Create a comprehensive study guide for {school_level} school students covering these {subject} topics:

{topics_str}

For each topic, include:
1. Overview
2. Key concepts
3. Important formulas/facts
4. Common mistakes to avoid
5. Study tips

Format as JSON with sections for each topic."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=3500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            content_result = response.content[0].text

            try:
                guide_data = json.loads(content_result)
            except json.JSONDecodeError:
                guide_data = {
                    "study_guide": content_result,
                    "topics": topics
                }

            return {
                'success': True,
                'study_guide': guide_data,
                'tokens_used': response.usage.input_tokens + response.usage.output_tokens
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


# Create singleton
notes_builder = NotesBuilder()
