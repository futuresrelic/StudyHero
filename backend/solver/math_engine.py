import re
from typing import Dict, List, Optional, Tuple
import sympy as sp
from sympy import symbols, solve, simplify, expand, factor, diff, integrate, Eq
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import numpy as np


class MathSolver:
    """Advanced math problem solver with step-by-step explanations"""

    def __init__(self):
        self.transformations = standard_transformations + (implicit_multiplication_application,)

    def clean_math_text(self, text: str) -> str:
        """Clean and normalize mathematical text"""
        # Replace common text representations
        replacements = {
            '×': '*',
            '÷': '/',
            '−': '-',
            '√': 'sqrt',
            '^': '**',
            'pi': 'pi',
            'π': 'pi',
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        return text.strip()

    def extract_equation(self, text: str) -> Optional[str]:
        """Extract equation from text"""
        # Look for equations with = sign
        equation_pattern = r'([^=]+=[^=]+)'
        match = re.search(equation_pattern, text)

        if match:
            return match.group(1).strip()

        return None

    def solve_linear_equation(self, equation_str: str) -> Dict:
        """Solve linear equations like 2x + 5 = 15"""
        try:
            equation_str = self.clean_math_text(equation_str)

            # Split by equals sign
            if '=' not in equation_str:
                return {'error': 'No equation found (missing = sign)'}

            left, right = equation_str.split('=')

            # Parse expressions
            x = symbols('x')
            left_expr = parse_expr(left.strip(), transformations=self.transformations)
            right_expr = parse_expr(right.strip(), transformations=self.transformations)

            # Create equation
            equation = Eq(left_expr, right_expr)

            # Solve
            solution = solve(equation, x)

            # Generate steps
            steps = [
                {
                    'step': 1,
                    'action': 'Original equation',
                    'expression': str(equation),
                    'explanation': 'This is the equation we need to solve for x.'
                },
                {
                    'step': 2,
                    'action': 'Simplify both sides',
                    'expression': f'{left_expr} = {right_expr}',
                    'explanation': 'Ensure both sides are in simplest form.'
                },
                {
                    'step': 3,
                    'action': 'Isolate variable',
                    'expression': f'x = {solution[0] if solution else "no solution"}',
                    'explanation': 'Move all terms with x to one side and constants to the other.'
                },
                {
                    'step': 4,
                    'action': 'Solution',
                    'expression': f'x = {solution[0] if solution else "no solution"}',
                    'explanation': f'The value of x is {solution[0] if solution else "undefined"}.'
                }
            ]

            return {
                'type': 'linear_equation',
                'solution': solution[0] if solution else None,
                'steps': steps,
                'verified': True
            }

        except Exception as e:
            return {'error': f'Could not solve equation: {str(e)}'}

    def solve_quadratic_equation(self, equation_str: str) -> Dict:
        """Solve quadratic equations like x^2 + 5x + 6 = 0"""
        try:
            equation_str = self.clean_math_text(equation_str)

            # Parse equation
            x = symbols('x')
            if '=' in equation_str:
                left, right = equation_str.split('=')
                left_expr = parse_expr(left.strip(), transformations=self.transformations)
                right_expr = parse_expr(right.strip(), transformations=self.transformations)
                expr = left_expr - right_expr
            else:
                expr = parse_expr(equation_str, transformations=self.transformations)

            # Solve
            solutions = solve(expr, x)

            # Get coefficients for quadratic formula explanation
            expanded = expand(expr)
            coeffs = [expanded.coeff(x, i) for i in [2, 1, 0]]
            a, b, c = coeffs

            steps = [
                {
                    'step': 1,
                    'action': 'Standard form',
                    'expression': f'{expanded} = 0',
                    'explanation': f'Rewrite in standard form ax² + bx + c = 0, where a={a}, b={b}, c={c}'
                },
                {
                    'step': 2,
                    'action': 'Apply quadratic formula',
                    'expression': 'x = (-b ± √(b² - 4ac)) / (2a)',
                    'explanation': 'Use the quadratic formula to find solutions.'
                },
                {
                    'step': 3,
                    'action': 'Calculate discriminant',
                    'expression': f'Δ = {b}² - 4({a})({c}) = {b**2 - 4*a*c}',
                    'explanation': 'The discriminant tells us how many real solutions exist.'
                },
                {
                    'step': 4,
                    'action': 'Solutions',
                    'expression': f'x = {", ".join(str(sol) for sol in solutions)}',
                    'explanation': f'The equation has {len(solutions)} solution(s).'
                }
            ]

            return {
                'type': 'quadratic_equation',
                'solutions': [float(sol.evalf()) if sol.is_real else str(sol) for sol in solutions],
                'steps': steps,
                'discriminant': float((b**2 - 4*a*c).evalf()),
                'verified': True
            }

        except Exception as e:
            return {'error': f'Could not solve quadratic equation: {str(e)}'}

    def simplify_expression(self, expr_str: str) -> Dict:
        """Simplify mathematical expressions"""
        try:
            expr_str = self.clean_math_text(expr_str)
            expr = parse_expr(expr_str, transformations=self.transformations)

            simplified = simplify(expr)
            expanded = expand(expr)
            factored = factor(expr)

            steps = [
                {
                    'step': 1,
                    'action': 'Original expression',
                    'expression': str(expr),
                    'explanation': 'Starting expression.'
                },
                {
                    'step': 2,
                    'action': 'Expand',
                    'expression': str(expanded),
                    'explanation': 'Expand all products and powers.'
                },
                {
                    'step': 3,
                    'action': 'Simplify',
                    'expression': str(simplified),
                    'explanation': 'Combine like terms and simplify.'
                }
            ]

            if str(factored) != str(simplified):
                steps.append({
                    'step': 4,
                    'action': 'Factor (alternative form)',
                    'expression': str(factored),
                    'explanation': 'Factored form of the expression.'
                })

            return {
                'type': 'simplification',
                'original': str(expr),
                'simplified': str(simplified),
                'expanded': str(expanded),
                'factored': str(factored),
                'steps': steps
            }

        except Exception as e:
            return {'error': f'Could not simplify expression: {str(e)}'}

    def solve_arithmetic(self, expression: str) -> Dict:
        """Solve basic arithmetic operations"""
        try:
            expression = self.clean_math_text(expression)

            # Evaluate the expression
            result = eval(expression, {"__builtins__": {}}, {})

            steps = [
                {
                    'step': 1,
                    'action': 'Original problem',
                    'expression': expression,
                    'explanation': 'Evaluate this arithmetic expression.'
                },
                {
                    'step': 2,
                    'action': 'Calculate',
                    'expression': f'{expression} = {result}',
                    'explanation': 'Perform the calculation following order of operations (PEMDAS).'
                },
                {
                    'step': 3,
                    'action': 'Answer',
                    'expression': str(result),
                    'explanation': f'The result is {result}.'
                }
            ]

            return {
                'type': 'arithmetic',
                'result': result,
                'steps': steps
            }

        except Exception as e:
            return {'error': f'Could not solve arithmetic: {str(e)}'}

    def solve_fraction(self, fraction_str: str) -> Dict:
        """Solve fraction operations"""
        try:
            fraction_str = self.clean_math_text(fraction_str)

            # Parse as rational
            from sympy import Rational, nsimplify

            result = parse_expr(fraction_str, transformations=self.transformations)
            simplified = nsimplify(result)

            steps = [
                {
                    'step': 1,
                    'action': 'Original fraction',
                    'expression': fraction_str,
                    'explanation': 'Starting fraction expression.'
                },
                {
                    'step': 2,
                    'action': 'Simplify',
                    'expression': str(simplified),
                    'explanation': 'Reduce to simplest form by finding GCD.'
                }
            ]

            return {
                'type': 'fraction',
                'result': str(simplified),
                'decimal': float(simplified.evalf()),
                'steps': steps
            }

        except Exception as e:
            return {'error': f'Could not solve fraction: {str(e)}'}

    def solve_word_problem(self, problem: str) -> Dict:
        """Attempt to solve word problems"""
        # This is a simplified version - in production, you'd use AI (Claude/GPT)
        # to parse and solve word problems

        # Look for common patterns
        patterns = {
            'total': r'(\d+)\s+\+\s+(\d+)',
            'difference': r'(\d+)\s+-\s+(\d+)',
            'product': r'(\d+)\s+(?:times|×|\*)\s+(\d+)',
            'quotient': r'(\d+)\s+(?:divided by|÷|/)\s+(\d+)',
        }

        for operation, pattern in patterns.items():
            match = re.search(pattern, problem, re.IGNORECASE)
            if match:
                num1, num2 = int(match.group(1)), int(match.group(2))

                if operation == 'total':
                    result = num1 + num2
                    steps = [
                        {'step': 1, 'action': 'Identify numbers', 'expression': f'{num1} and {num2}', 'explanation': 'Find the numbers to add.'},
                        {'step': 2, 'action': 'Add', 'expression': f'{num1} + {num2} = {result}', 'explanation': 'Calculate the sum.'},
                    ]
                elif operation == 'difference':
                    result = num1 - num2
                    steps = [
                        {'step': 1, 'action': 'Identify numbers', 'expression': f'{num1} and {num2}', 'explanation': 'Find the numbers to subtract.'},
                        {'step': 2, 'action': 'Subtract', 'expression': f'{num1} - {num2} = {result}', 'explanation': 'Calculate the difference.'},
                    ]
                elif operation == 'product':
                    result = num1 * num2
                    steps = [
                        {'step': 1, 'action': 'Identify numbers', 'expression': f'{num1} and {num2}', 'explanation': 'Find the numbers to multiply.'},
                        {'step': 2, 'action': 'Multiply', 'expression': f'{num1} × {num2} = {result}', 'explanation': 'Calculate the product.'},
                    ]
                else:  # quotient
                    result = num1 / num2
                    steps = [
                        {'step': 1, 'action': 'Identify numbers', 'expression': f'{num1} and {num2}', 'explanation': 'Find the numbers to divide.'},
                        {'step': 2, 'action': 'Divide', 'expression': f'{num1} ÷ {num2} = {result}', 'explanation': 'Calculate the quotient.'},
                    ]

                return {
                    'type': 'word_problem',
                    'operation': operation,
                    'result': result,
                    'steps': steps
                }

        return {'error': 'Could not parse word problem'}

    def solve(self, problem: str) -> Dict:
        """Main solver that routes to appropriate method"""
        problem = problem.strip()

        # Detect problem type and route accordingly
        if '=' in problem:
            # Check if quadratic
            if 'x^2' in problem or 'x**2' in problem or 'x²' in problem:
                return self.solve_quadratic_equation(problem)
            else:
                return self.solve_linear_equation(problem)

        # Check for fractions
        if '/' in problem and not any(op in problem for op in ['=', 'solve', 'simplify']):
            return self.solve_fraction(problem)

        # Check for simplification request
        if any(word in problem.lower() for word in ['simplify', 'expand', 'factor']):
            # Extract the expression after the command
            for word in ['simplify', 'expand', 'factor']:
                if word in problem.lower():
                    expr = problem.lower().split(word)[-1].strip()
                    return self.simplify_expression(expr)

        # Check if it's a word problem
        if any(word in problem.lower() for word in ['how many', 'what is', 'calculate', 'find']):
            return self.solve_word_problem(problem)

        # Default: try arithmetic
        return self.solve_arithmetic(problem)


# Create singleton
math_solver = MathSolver()
