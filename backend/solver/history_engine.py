from typing import Dict, List
import re


class HistorySolver:
    """History and social studies helper"""

    def __init__(self):
        # Sample historical data
        self.historical_events = {
            '1776': {
                'event': 'American Declaration of Independence',
                'description': 'The United States declared independence from Great Britain.',
                'significance': 'Birth of the United States of America',
                'key_figures': ['Thomas Jefferson', 'Benjamin Franklin', 'John Adams']
            },
            '1789': {
                'event': 'French Revolution begins',
                'description': 'The French Revolution began, overthrowing the monarchy.',
                'significance': 'Major political and social upheaval in France',
                'key_figures': ['King Louis XVI', 'Marie Antoinette', 'Robespierre']
            },
            '1865': {
                'event': 'End of American Civil War',
                'description': 'The Civil War ended with Union victory.',
                'significance': 'Preservation of the United States, end of slavery',
                'key_figures': ['Abraham Lincoln', 'Ulysses S. Grant', 'Robert E. Lee']
            },
            '1945': {
                'event': 'End of World War II',
                'description': 'World War II ended with Allied victory.',
                'significance': 'Defeat of Nazi Germany and Imperial Japan',
                'key_figures': ['Franklin D. Roosevelt', 'Winston Churchill', 'Adolf Hitler']
            }
        }

        self.presidents = {
            'george washington': {'number': 1, 'years': '1789-1797', 'party': 'None'},
            'abraham lincoln': {'number': 16, 'years': '1861-1865', 'party': 'Republican'},
            'theodore roosevelt': {'number': 26, 'years': '1901-1909', 'party': 'Republican'},
            'franklin d. roosevelt': {'number': 32, 'years': '1933-1945', 'party': 'Democratic'},
        }

    def extract_year(self, text: str) -> List[str]:
        """Extract years from text"""
        year_pattern = r'\b(1\d{3}|20\d{2})\b'
        years = re.findall(year_pattern, text)
        return years

    def find_event_by_year(self, year: str) -> Dict:
        """Find historical events by year"""
        if year in self.historical_events:
            return {
                'type': 'historical_event',
                'year': year,
                'event': self.historical_events[year],
                'explanation': f"In {year}, {self.historical_events[year]['event']} occurred. " +
                              f"{self.historical_events[year]['description']}"
            }

        return {
            'type': 'historical_event',
            'year': year,
            'explanation': f'Year {year} - Historical information would be provided by AI in production.'
        }

    def explain_president(self, name: str) -> Dict:
        """Explain about US presidents"""
        name_lower = name.lower()

        for president, info in self.presidents.items():
            if president in name_lower or name_lower in president:
                return {
                    'type': 'president_info',
                    'name': president.title(),
                    'info': info,
                    'explanation': f"{president.title()} was the {info['number']} President " +
                                  f"of the United States ({info['years']}), {info['party']} Party."
                }

        return {
            'type': 'president_info',
            'name': name,
            'explanation': f'Information about {name} would be provided by AI in production.'
        }

    def explain_concept(self, concept: str) -> Dict:
        """Explain historical concepts"""
        concepts = {
            'revolution': 'A revolution is a fundamental change in political power or organizational structures that takes place in a relatively short period of time.',
            'democracy': 'Democracy is a form of government in which power is vested in the people, who rule either directly or through elected representatives.',
            'monarchy': 'Monarchy is a form of government where a single person (monarch) rules, typically inherited through family lineage.',
            'constitution': 'A constitution is a set of fundamental principles or established precedents that constitute the legal basis of a polity, organization, or other type of entity.',
            'amendment': 'An amendment is a formal change or addition to a document, especially a constitution or law.',
            'treaty': 'A treaty is a formally concluded and ratified agreement between countries.',
            'empire': 'An empire is a political unit having an extensive territory or comprising a number of territories or nations under a single supreme authority.',
        }

        concept_lower = concept.lower()
        for key, definition in concepts.items():
            if key in concept_lower:
                return {
                    'type': 'historical_concept',
                    'concept': key,
                    'definition': definition,
                    'explanation': definition
                }

        return {
            'type': 'historical_concept',
            'concept': concept,
            'explanation': f'The concept of {concept} would be explained in detail by AI in production.'
        }

    def create_timeline(self, events: List[str]) -> Dict:
        """Create a timeline of events"""
        # Extract years from events
        timeline = []

        for event in events:
            years = self.extract_year(event)
            if years:
                for year in years:
                    timeline.append({
                        'year': year,
                        'event': event,
                        'details': self.historical_events.get(year, {}).get('event', 'Event details')
                    })

        # Sort by year
        timeline.sort(key=lambda x: x['year'])

        return {
            'type': 'timeline',
            'events': timeline,
            'explanation': 'Timeline of historical events'
        }

    def compare_events(self, event1: str, event2: str) -> Dict:
        """Compare two historical events"""
        return {
            'type': 'comparison',
            'event1': event1,
            'event2': event2,
            'explanation': f'Comparison between {event1} and {event2} would be provided by AI.',
            'similarities': ['To be generated by AI'],
            'differences': ['To be generated by AI']
        }

    def solve(self, question: str) -> Dict:
        """Main solver for history questions"""
        question_lower = question.lower()

        # Check for year queries
        years = self.extract_year(question)
        if years and any(word in question_lower for word in ['what', 'when', 'happened', 'occur']):
            return self.find_event_by_year(years[0])

        # Check for president queries
        if 'president' in question_lower:
            for president in self.presidents.keys():
                if president in question_lower:
                    return self.explain_president(president)

        # Check for concept explanations
        if any(word in question_lower for word in ['what is', 'define', 'explain', 'meaning']):
            for concept in ['revolution', 'democracy', 'monarchy', 'constitution', 'amendment', 'treaty', 'empire']:
                if concept in question_lower:
                    return self.explain_concept(concept)

        # Check for timeline creation
        if 'timeline' in question_lower or 'chronological' in question_lower:
            return self.create_timeline([question])

        # Default response
        return {
            'type': 'history_general',
            'question': question,
            'explanation': 'This history question would be answered in detail using AI in production. ' +
                          'The AI would provide comprehensive historical context, dates, key figures, ' +
                          'and significance of events.',
            'steps': [
                {
                    'step': 1,
                    'action': 'Identify the historical topic',
                    'explanation': 'Determine what aspect of history is being asked about.'
                },
                {
                    'step': 2,
                    'action': 'Provide context',
                    'explanation': 'Give background information about the time period.'
                },
                {
                    'step': 3,
                    'action': 'Answer the question',
                    'explanation': 'Provide a clear, detailed answer with relevant facts.'
                },
                {
                    'step': 4,
                    'action': 'Explain significance',
                    'explanation': 'Describe why this topic is important in history.'
                }
            ]
        }


# Create singleton
history_solver = HistorySolver()
