import json
from typing import Dict, Any, List, Tuple
import random
from event_processor import EventProcessor

class FantasyWorld:
    def __init__(self):
        self.state = {
            "year": 1000,
            "regions": {
                "Northern Mountains": {
                    "dragon_activity": 0,
                    "trade": 50,
                    "magical_energy": 30,
                    "fertility": 40,
                    "creature_diversity": 35  # New attribute
                },
                "Southern Plains": {
                    "fertility": 70,
                    "trade": 60,
                    "magical_energy": 20,
                    "creature_diversity": 30  # New attribute
                },
                "Eastern Forests": {
                    "magical_energy": 60,
                    "creature_diversity": 40,
                    "trade": 30,
                    "fertility": 55
                },
                "Western Deserts": {
                    "magical_energy": 40,
                    "trade": 40,
                    "fertility": 20,
                    "creature_diversity": 25  # New attribute
                },
                "Central Valley": {
                    "magical_energy": 50,
                    "fertility": 80,
                    "trade": 70,
                    "creature_diversity": 45  # New attribute
                },
                "Coastal Regions": {
                    "trade": 80,
                    "magical_energy": 30,
                    "fertility": 60,
                    "creature_diversity": 50  # New attribute
                }
            },
            "factions": {
                "Mages' Guild": {
                    "stability": 70,
                    "power": 60,
                    "aggressiveness": 30,
                    "leader": "Archmage Eldrin",
                    "influence": 65
                },
                "Merchant League": {
                    "stability": 80,
                    "trade_income": 70,
                    "influence": 60
                },
                "Noble Houses": {
                    "stability": 75,
                    "power": 65,
                    "influence": 70
                },
                "Temple of Light": {
                    "stability": 85,
                    "influence": 75,
                    "power": 55
                },
                "Dark Brotherhood": {
                    "stability": 40,
                    "power": 50,
                    "influence": 45
                },
                "Rangers' Order": {
                    "stability": 70,
                    "power": 55,
                    "influence": 50
                }
            }
        }
        print("Initialisiere EventProcessor...")
        self.event_processor = EventProcessor('event_definitions.json')
        print("EventProcessor initialisiert")

    def generate_events(self) -> List[Dict[str, Any]]:
        # Update the year in the state
        self.state['year'] = self.state['year'] + 1
        print(f"\nJahr {self.state['year']}:")
        print("Aktueller Zustand:")
        print(f"  Central Valley magical_energy: {self.state['regions']['Central Valley']['magical_energy']}")
        print(f"  Mages' Guild stability: {self.state['factions']['Mages\' Guild']['stability']}")
        
        # Process events using the EventProcessor
        triggered_events = self.event_processor.process_events(self.state)
        
        if triggered_events:
            print("\nAusgelöste Events:")
            for event in triggered_events:
                print(f"  - {event['name']} ({event['category']})")
        else:
            print("\nKeine Events ausgelöst")
        
        return triggered_events