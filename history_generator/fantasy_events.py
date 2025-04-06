from .events import Event
from .fantasy_world import FantasyWorld
from typing import List

class FantasyEvent(Event):
    def __init__(self, year: int, event_data: dict):
        self.event_data = event_data
        self.category = event_data.get('category', 'unknown')
        self.name = event_data.get('name', 'Unbekanntes Event')
        self.severity = event_data.get('severity', 'moderate')
        self.region = event_data.get('region', 'unknown')
        self.impact = event_data.get('impact', 'unknown')
        self.faction = event_data.get('faction', 'unknown')
        self.effects = event_data.get('effects', [])  # Store effects directly
        super().__init__(year, self.name)

    def __str__(self):
        details = []
        if self.severity != 'moderate':
            details.append(f"Schweregrad: {self.severity}")
        if self.region != 'unknown':
            details.append(f"Region: {self.region}")
        if self.impact != 'unknown':
            details.append(f"Auswirkung: {self.impact}")
        if self.faction != 'unknown':
            details.append(f"Fraktion: {self.faction}")
        
        base = f"{self.name} ({self.category})"
        if details:
            return f"{base}\n    Details: {', '.join(details)}"
        return base

class NaturalEvent(FantasyEvent):
    def __init__(self, year: int, event_data: dict):
        super().__init__(year, event_data)

class MagicalEvent(FantasyEvent):
    def __init__(self, year: int, event_data: dict):
        super().__init__(year, event_data)

class PoliticalEvent(FantasyEvent):
    def __init__(self, year: int, event_data: dict):
        super().__init__(year, event_data)

class FantasyEventGenerator:
    def __init__(self, fantasy_world: FantasyWorld):
        self.world = fantasy_world

    def generate_events(self, year: int) -> List[FantasyEvent]:
        # Set the year directly
        self.world.year = year
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
            
            # Apply effects
            for effect in event_data.get('effects', []):
                if effect['type'] == 'modify_stat':
                    if 'faction' in effect:
                        self.world.factions[effect['faction']][effect['stat']] += effect['value']
                    elif 'region' in effect:
                        self.world.regions[effect['region']][effect['stat']] += effect['value']
        
        return events