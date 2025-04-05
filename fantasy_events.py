from events import Event
from fantasy_world import FantasyWorld
from typing import List

class FantasyEvent(Event):
    def __init__(self, year: int, event_data: dict):
        self.event_data = event_data
        self.category = event_data.get('category', 'unknown')
        super().__init__(year, event_data['name'])

class NaturalEvent(FantasyEvent):
    def __init__(self, year: int, event_data: dict):
        super().__init__(year, event_data)
        self.severity = event_data.get('severity', 'moderate')
        self.region = event_data.get('region', 'unknown')

class MagicalEvent(FantasyEvent):
    def __init__(self, year: int, event_data: dict):
        super().__init__(year, event_data)
        self.impact = event_data.get('impact', 'unknown')

class PoliticalEvent(FantasyEvent):
    def __init__(self, year: int, event_data: dict):
        super().__init__(year, event_data)
        self.faction = event_data.get('faction', 'unknown')

class FantasyEventGenerator:
    def __init__(self):
        self.world = FantasyWorld()

    def generate_events(self, year: int) -> List[FantasyEvent]:
        self.world.state['year'] = year
        raw_events = self.world.generate_events()
        
        events = []
        for event_data in raw_events:
            category = event_data.get('category', '')
            if category == 'natural':
                events.append(NaturalEvent(year, event_data))
            elif category == 'magical':
                events.append(MagicalEvent(year, event_data))
            elif category == 'political':
                events.append(PoliticalEvent(year, event_data))
        
        return events