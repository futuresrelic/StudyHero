import pytest
from solver.math_engine import math_solver


class TestMathSolver:
    """Tests for math solving engine"""

    def test_solve_linear_equation(self):
        """Test linear equation solving"""
        result = math_solver.solve_linear_equation("2x + 5 = 15")
        assert result.get('solution') == 5
        assert result.get('type') == 'linear_equation'
        assert 'steps' in result

    def test_solve_quadratic_equation(self):
        """Test quadratic equation solving"""
        result = math_solver.solve_quadratic_equation("x^2 - 5x + 6 = 0")
        assert result.get('type') == 'quadratic_equation'
        solutions = result.get('solutions', [])
        assert len(solutions) == 2
        assert 2.0 in solutions or 3.0 in solutions

    def test_simplify_expression(self):
        """Test expression simplification"""
        result = math_solver.simplify_expression("2*x + 3*x")
        assert result.get('type') == 'simplification'
        assert 'simplified' in result

    def test_solve_arithmetic(self):
        """Test basic arithmetic"""
        result = math_solver.solve_arithmetic("5 + 3 * 2")
        assert result.get('result') == 11
        assert result.get('type') == 'arithmetic'

    def test_solve_fraction(self):
        """Test fraction operations"""
        result = math_solver.solve_fraction("1/2 + 1/4")
        assert 'result' in result
        assert result.get('type') == 'fraction'

    def test_invalid_equation(self):
        """Test handling of invalid equations"""
        result = math_solver.solve("invalid equation xyz")
        assert 'error' in result or result.get('type') is not None

    def test_clean_math_text(self):
        """Test text cleaning"""
        cleaned = math_solver.clean_math_text("2 × 3 ÷ 4")
        assert '×' not in cleaned
        assert '÷' not in cleaned
        assert '*' in cleaned
        assert '/' in cleaned
