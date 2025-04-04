import random
from events import Event
from typing import List

class FantasyEvent(Event):
    pass

class NaturalEvent(FantasyEvent):
    def __init__(self, year: int, event_type: str, severity: str, region: str):
        self.event_type = event_type
        self.severity = severity
        self.region = region
        message = f"A {severity} {event_type} affects {region}"
        super().__init__(year, message)

class MagicalEvent(FantasyEvent):
    def __init__(self, year: int, event_type: str, impact: str):
        self.event_type = event_type
        self.impact = impact
        message = f"A {event_type} occurs: {impact}"
        super().__init__(year, message)

class PoliticalEvent(FantasyEvent):
    def __init__(self, year: int, event_type: str, faction: str, outcome: str):
        self.event_type = event_type
        self.faction = faction
        self.outcome = outcome
        message = f"{faction} {event_type}: {outcome}"
        super().__init__(year, message)

class FantasyEventGenerator:
    def __init__(self):
        self.regions = [
            "the Northern Mountains", "the Southern Plains", "the Eastern Forests",
            "the Western Deserts", "the Central Valley", "the Coastal Regions"
        ]
        self.factions = [
            "The Mages' Guild", "The Merchant League", "The Noble Houses",
            "The Temple of Light", "The Dark Brotherhood", "The Rangers' Order"
        ]
        self.natural_events = [
            ("dragon migration", "mild", "causes temporary disruption"),
            ("magical storm", "severe", "lasts for weeks"),
            ("earthquake", "catastrophic", "reshapes the landscape"),
            ("meteor shower", "moderate", "brings rare materials"),
            ("volcanic eruption", "devastating", "creates new magical hotspots")
        ]
        self.magical_events = [
            ("mana surge", "enhances magical abilities temporarily"),
            ("dimensional rift", "allows travel to other realms"),
            ("magical plague", "affects spellcasters"),
            ("ley line shift", "alters magical geography"),
            ("ancient artifact awakening", "changes local power dynamics")
        ]
        self.political_events = [
            ("declares war", "shifts regional power"),
            ("forms an alliance", "strengthens diplomatic ties"),
            ("undergoes a coup", "changes leadership"),
            ("discovers ancient knowledge", "gains strategic advantage"),
            ("suffers internal conflict", "weakens their position")
        ]

    def generate_events(self, year: int) -> List[FantasyEvent]:
        events = []
        
        # 30% chance for a natural event
        if random.random() < 0.3:
            event_type, severity, impact = random.choice(self.natural_events)
            region = random.choice(self.regions)
            events.append(NaturalEvent(year, event_type, severity, region))
        
        # 20% chance for a magical event
        if random.random() < 0.2:
            event_type, impact = random.choice(self.magical_events)
            events.append(MagicalEvent(year, event_type, impact))
        
        # 25% chance for a political event
        if random.random() < 0.25:
            event_type, outcome = random.choice(self.political_events)
            faction = random.choice(self.factions)
            events.append(PoliticalEvent(year, event_type, faction, outcome))
        
        return events 