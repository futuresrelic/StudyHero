from typing import Dict, List
import re


class ScienceSolver:
    """Science problem solver for chemistry, physics, and biology"""

    def __init__(self):
        # Periodic table data (simplified)
        self.periodic_table = {
            'H': {'name': 'Hydrogen', 'atomic_number': 1, 'atomic_mass': 1.008},
            'He': {'name': 'Helium', 'atomic_number': 2, 'atomic_mass': 4.003},
            'C': {'name': 'Carbon', 'atomic_number': 6, 'atomic_mass': 12.011},
            'N': {'name': 'Nitrogen', 'atomic_number': 7, 'atomic_mass': 14.007},
            'O': {'name': 'Oxygen', 'atomic_number': 8, 'atomic_mass': 15.999},
            'Na': {'name': 'Sodium', 'atomic_number': 11, 'atomic_mass': 22.990},
            'Cl': {'name': 'Chlorine', 'atomic_number': 17, 'atomic_mass': 35.45},
            'Fe': {'name': 'Iron', 'atomic_number': 26, 'atomic_mass': 55.845},
        }

    def identify_physics_concept(self, text: str) -> str:
        """Identify the physics concept from question"""
        text_lower = text.lower()

        concepts = {
            'kinematics': ['velocity', 'speed', 'acceleration', 'distance', 'time', 'motion'],
            'force': ['force', 'newton', 'mass', 'acceleration', 'f=ma'],
            'energy': ['energy', 'work', 'power', 'kinetic', 'potential', 'joule'],
            'momentum': ['momentum', 'collision', 'impulse'],
            'gravity': ['gravity', 'gravitational', 'g=9.8', 'weight'],
            'electricity': ['current', 'voltage', 'resistance', 'ohm', 'circuit'],
        }

        for concept, keywords in concepts.items():
            if any(keyword in text_lower for keyword in keywords):
                return concept

        return 'general_physics'

    def solve_physics(self, problem: str) -> Dict:
        """Solve basic physics problems"""
        concept = self.identify_physics_concept(problem)

        # Extract numbers from problem
        numbers = re.findall(r'\d+\.?\d*', problem)

        if concept == 'kinematics' and len(numbers) >= 2:
            # Assume distance = speed × time
            if 'speed' in problem.lower() or 'velocity' in problem.lower():
                distance = float(numbers[0])
                time = float(numbers[1]) if len(numbers) > 1 else 1

                speed = distance / time if time != 0 else 0

                steps = [
                    {
                        'step': 1,
                        'action': 'Identify formula',
                        'expression': 'speed = distance / time',
                        'explanation': 'Use the basic kinematics formula.'
                    },
                    {
                        'step': 2,
                        'action': 'Substitute values',
                        'expression': f'speed = {distance} / {time}',
                        'explanation': f'Distance = {distance} units, Time = {time} units'
                    },
                    {
                        'step': 3,
                        'action': 'Calculate',
                        'expression': f'speed = {speed}',
                        'explanation': f'The speed is {speed} units per time.'
                    }
                ]

                return {
                    'type': 'physics_kinematics',
                    'concept': concept,
                    'result': speed,
                    'steps': steps
                }

        elif concept == 'force' and len(numbers) >= 2:
            # F = ma
            mass = float(numbers[0])
            acceleration = float(numbers[1])
            force = mass * acceleration

            steps = [
                {
                    'step': 1,
                    'action': "Newton's Second Law",
                    'expression': 'F = ma',
                    'explanation': 'Force equals mass times acceleration.'
                },
                {
                    'step': 2,
                    'action': 'Substitute values',
                    'expression': f'F = {mass} × {acceleration}',
                    'explanation': f'Mass = {mass} kg, Acceleration = {acceleration} m/s²'
                },
                {
                    'step': 3,
                    'action': 'Calculate',
                    'expression': f'F = {force} N',
                    'explanation': f'The force is {force} Newtons.'
                }
            ]

            return {
                'type': 'physics_force',
                'concept': concept,
                'result': force,
                'unit': 'Newtons',
                'steps': steps
            }

        return {
            'type': 'physics',
            'concept': concept,
            'explanation': f'This is a {concept} problem. ' +
                          'In a full implementation, AI would parse and solve this problem step by step.',
            'steps': []
        }

    def balance_chemical_equation(self, equation: str) -> Dict:
        """Balance chemical equations (simplified)"""
        # This is a simplified version
        # In production, use a proper chemistry library

        steps = [
            {
                'step': 1,
                'action': 'Identify reactants and products',
                'expression': equation,
                'explanation': 'Write out the unbalanced equation.'
            },
            {
                'step': 2,
                'action': 'Count atoms',
                'expression': 'Count atoms of each element on both sides',
                'explanation': 'Make a table of atoms on each side.'
            },
            {
                'step': 3,
                'action': 'Balance',
                'expression': 'Add coefficients to balance',
                'explanation': 'Use trial and error or algebraic method.'
            },
            {
                'step': 4,
                'action': 'Verify',
                'expression': 'Check that all atoms balance',
                'explanation': 'Ensure the law of conservation of mass is satisfied.'
            }
        ]

        return {
            'type': 'chemistry_balancing',
            'original_equation': equation,
            'steps': steps,
            'note': 'Chemical equation balancing requires complex algorithms. ' +
                   'In production, integrate with a chemistry library or AI.'
        }

    def explain_biology_concept(self, concept: str) -> Dict:
        """Explain biology concepts"""
        concepts_db = {
            'photosynthesis': {
                'definition': 'The process by which plants use sunlight, water, and CO2 to produce glucose and oxygen.',
                'equation': '6CO2 + 6H2O + light energy → C6H12O6 + 6O2',
                'key_points': [
                    'Occurs in chloroplasts',
                    'Requires chlorophyll',
                    'Light-dependent and light-independent reactions',
                    'Produces food for the plant'
                ]
            },
            'mitosis': {
                'definition': 'Cell division that produces two identical daughter cells.',
                'phases': ['Prophase', 'Metaphase', 'Anaphase', 'Telophase'],
                'key_points': [
                    'Produces diploid cells',
                    'Used for growth and repair',
                    'Chromosomes duplicate then separate',
                    'Results in genetically identical cells'
                ]
            },
            'cell': {
                'definition': 'The basic unit of life.',
                'components': ['Nucleus', 'Cytoplasm', 'Cell membrane', 'Mitochondria'],
                'key_points': [
                    'All living things are made of cells',
                    'Cells come from pre-existing cells',
                    'Contains genetic material',
                    'Can be prokaryotic or eukaryotic'
                ]
            }
        }

        concept_lower = concept.lower()
        for key, data in concepts_db.items():
            if key in concept_lower:
                return {
                    'type': 'biology_concept',
                    'concept': key,
                    'data': data,
                    'explanation': data.get('definition', 'Concept explanation')
                }

        return {
            'type': 'biology_concept',
            'concept': concept,
            'explanation': f'General biology concept: {concept}. ' +
                          'In production, use AI to provide detailed explanations.'
        }

    def solve(self, problem: str) -> Dict:
        """Main solver for science problems"""
        problem_lower = problem.lower()

        # Detect problem type
        if any(word in problem_lower for word in ['velocity', 'speed', 'force', 'energy', 'mass', 'acceleration']):
            return self.solve_physics(problem)

        elif any(word in problem_lower for word in ['balance', 'equation', 'chemical', 'reaction']):
            return self.balance_chemical_equation(problem)

        elif any(word in problem_lower for word in ['cell', 'mitosis', 'photosynthesis', 'biology', 'organism']):
            # Extract concept
            for concept in ['photosynthesis', 'mitosis', 'cell']:
                if concept in problem_lower:
                    return self.explain_biology_concept(concept)

            return self.explain_biology_concept(problem)

        return {
            'type': 'science_general',
            'explanation': 'Science problem detected. In production, use AI to solve complex science problems.',
            'steps': []
        }


# Create singleton
science_solver = ScienceSolver()
