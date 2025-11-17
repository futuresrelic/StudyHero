import pytesseract
from PIL import Image
import cv2
import numpy as np
import re
from typing import Dict, List, Tuple
import os
from config import settings

# Set Tesseract path
if os.path.exists(settings.TESSERACT_CMD):
    pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD


class OCRProcessor:
    """OCR processing for homework questions"""

    def __init__(self):
        self.supported_languages = ['eng']

    def preprocess_image(self, image_path: str) -> np.ndarray:
        """Preprocess image for better OCR results"""
        # Read image
        img = cv2.imread(image_path)

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply denoising
        denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)

        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )

        # Dilation to connect text
        kernel = np.ones((1, 1), np.uint8)
        dilated = cv2.dilate(thresh, kernel, iterations=1)

        return dilated

    def extract_text(self, image_path: str) -> str:
        """Extract text from image using Tesseract OCR"""
        try:
            # Preprocess the image
            processed_img = self.preprocess_image(image_path)

            # Extract text with custom config
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(processed_img, config=custom_config)

            return text.strip()
        except Exception as e:
            print(f"OCR Error: {e}")
            # Fallback: try with original image
            try:
                img = Image.open(image_path)
                text = pytesseract.image_to_string(img)
                return text.strip()
            except Exception as e2:
                print(f"Fallback OCR Error: {e2}")
                return ""

    def detect_math_expressions(self, text: str) -> List[str]:
        """Detect mathematical expressions in text"""
        math_patterns = [
            r'\d+\s*[\+\-\*/÷×]\s*\d+',  # Basic arithmetic
            r'\d+\s*[=]\s*\d+',  # Equations
            r'[xy]\s*[\+\-\*/]\s*\d+',  # Algebraic expressions
            r'\d+x[\+\-]\d+',  # Linear equations
            r'x\^?\d+',  # Powers
            r'\d+/\d+',  # Fractions
            r'√\d+',  # Square roots
            r'\(\s*[\d\+\-\*/xy]+\s*\)',  # Parentheses
        ]

        math_expressions = []
        for pattern in math_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            math_expressions.extend(matches)

        return list(set(math_expressions))

    def classify_subject(self, text: str) -> Tuple[str, float]:
        """Classify the subject of the question"""
        text_lower = text.lower()

        # Subject keywords
        subjects = {
            'math': ['solve', 'equation', 'calculate', 'sum', 'difference', 'product',
                    'quotient', 'factor', 'simplify', 'algebra', 'geometry', 'calculus',
                    'derivative', 'integral', 'trigonometry', 'sine', 'cosine', 'tangent',
                    'graph', 'function', 'polynomial', 'quadratic', 'linear'],
            'science': ['atom', 'molecule', 'element', 'compound', 'reaction', 'chemical',
                       'physics', 'force', 'energy', 'motion', 'velocity', 'acceleration',
                       'biology', 'cell', 'organism', 'photosynthesis', 'mitosis',
                       'electron', 'proton', 'neutron', 'periodic table'],
            'history': ['year', 'century', 'war', 'revolution', 'president', 'king',
                       'empire', 'civilization', 'treaty', 'amendment', 'constitution',
                       'dynasty', 'battle', 'historical', 'ancient', 'medieval'],
            'english': ['write', 'essay', 'paragraph', 'sentence', 'grammar', 'verb',
                       'noun', 'adjective', 'metaphor', 'simile', 'theme', 'author',
                       'poem', 'story', 'narrative', 'literature', 'reading'],
            'geography': ['country', 'continent', 'ocean', 'mountain', 'river', 'capital',
                         'population', 'climate', 'map', 'latitude', 'longitude'],
        }

        scores = {}
        for subject, keywords in subjects.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                scores[subject] = score

        # Check for math expressions
        math_expressions = self.detect_math_expressions(text)
        if math_expressions:
            scores['math'] = scores.get('math', 0) + len(math_expressions) * 2

        if not scores:
            return 'general', 0.5

        # Get subject with highest score
        best_subject = max(scores, key=scores.get)
        confidence = min(scores[best_subject] / 10.0, 1.0)

        return best_subject, confidence

    def detect_question_blocks(self, text: str) -> List[Dict[str, str]]:
        """Detect multiple questions in text"""
        # Split by common question indicators
        lines = text.split('\n')
        questions = []
        current_question = []

        question_indicators = [
            r'^\d+[\.\)]\s',  # 1. or 1)
            r'^[a-z][\.\)]\s',  # a. or a)
            r'^Question\s+\d+',  # Question 1
            r'^Q\d+',  # Q1
        ]

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Check if this line starts a new question
            is_new_question = any(re.match(pattern, line, re.IGNORECASE) for pattern in question_indicators)

            if is_new_question and current_question:
                # Save previous question
                questions.append({
                    'text': ' '.join(current_question),
                    'number': len(questions) + 1
                })
                current_question = [line]
            else:
                current_question.append(line)

        # Add last question
        if current_question:
            questions.append({
                'text': ' '.join(current_question),
                'number': len(questions) + 1
            })

        # If no structured questions found, return whole text as single question
        if not questions:
            questions = [{'text': text, 'number': 1}]

        return questions

    def process_homework_image(self, image_path: str) -> Dict:
        """Complete OCR processing pipeline"""
        # Extract text
        text = self.extract_text(image_path)

        if not text:
            return {
                'success': False,
                'error': 'Could not extract text from image'
            }

        # Classify subject
        subject, confidence = self.classify_subject(text)

        # Detect questions
        questions = self.detect_question_blocks(text)

        # Detect math expressions
        math_expressions = self.detect_math_expressions(text)

        return {
            'success': True,
            'text': text,
            'subject': subject,
            'confidence': confidence,
            'questions': questions,
            'math_expressions': math_expressions,
            'question_count': len(questions)
        }


# Create singleton instance
ocr_processor = OCRProcessor()
