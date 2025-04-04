import json
from typing import Dict, Any, List
from enum import Enum
import random

class Season(Enum):
    SPRING = "spring"
    SUMMER = "summer"
    AUTUMN = "autumn"
    WINTER = "winter"

class FantasyWorld:
    def __init__(self):
        self.state = {
            "year": 1000,
            "season": Season.SPRING,
            "regions": {
                "Northern Mountains": {
                    "dragon_activity": 0,
                    "trade": 50,
                    "magical_energy": 30
                },
                "Southern Plains": {
                    "fertility": 70,
                    "trade": 60,
                    "magical_energy": 20
                },
                "Eastern Forests": {
                    "magical_energy": 60,
                    "creature_diversity": 40,
                    "trade": 30
                },
                "Western Deserts": {
                    "magical_energy": 40,
                    "trade": 40,
                    "fertility": 20
                },
                "Central Valley": {
                    "magical_energy": 50,
                    "fertility": 80,
                    "trade": 70
                },
                "Coastal Regions": {
                    "trade": 80,
                    "magical_energy": 30,
                    "fertility": 60
                }
            },
            "factions": {
                "Mages' Guild": {
                    "stability": 70,
                    "power": 60,
                    "aggressiveness": 30,
                    "leader": "Archmage Eldrin"
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
        self.events = self._load_events()
        self.active_events: List[str] = []

    def _load_events(self) -> Dict[str, Any]:
        with open('event_definitions.json', 'r') as f:
            return json.load(f)['events']

    def update_season(self):
        current_season = self.state['season']
        if current_season == Season.WINTER:
            self.state['season'] = Season.SPRING
        else:
            # Get the next season by getting the next enum value
            seasons = list(Season)
            current_index = seasons.index(current_season)
            next_index = (current_index + 1) % len(seasons)
            self.state['season'] = seasons[next_index]

    def _check_condition(self, condition: Dict[str, Any], value: Any) -> bool:
        for op, threshold in condition.items():
            if op == "gte":
                if not (value >= threshold):
                    return False
            elif op == "lte":
                if not (value <= threshold):
                    return False
            elif op == "gt":
                if not (value > threshold):
                    return False
            elif op == "lt":
                if not (value < threshold):
                    return False
            elif op == "eq":
                if not (value == threshold):
                    return False
        return True

    def _get_value(self, path: str) -> Any:
        parts = path.split('.')
        current = self.state
        for part in parts:
            current = current[part]
        return current

    def _set_value(self, path: str, value: Any):
        parts = path.split('.')
        current = self.state
        for part in parts[:-1]:
            current = current[part]
        current[parts[-1]] = value

    def _apply_effect(self, effect: Dict[str, Any]):
        for path, value in effect.items():
            current_value = self._get_value(path)
            if isinstance(value, int):
                # Relative change
                new_value = current_value + value
                self._set_value(path, max(0, min(100, new_value)))
            else:
                # Absolute value
                self._set_value(path, value)

    def check_event_conditions(self, event: Dict[str, Any]) -> bool:
        for path, condition in event['conditions'].items():
            if path == 'year':
                if not self._check_condition(condition, self.state['year']):
                    return False
            elif path == 'season':
                if self.state['season'].value != condition:
                    return False
            else:
                value = self._get_value(path)
                if not self._check_condition(condition, value):
                    return False
        return True

    def generate_events(self) -> List[Dict[str, Any]]:
        possible_events = []
        
        # Check for natural events
        for event_id, event in self.events['natural'].items():
            if self.check_event_conditions(event):
                # Kategorie zum Ereignis hinzufügen
                event['category'] = 'natural'
                possible_events.append(event)
        
        # Check for magical events
        for event_id, event in self.events['magical'].items():
            if self.check_event_conditions(event):
                # Kategorie zum Ereignis hinzufügen
                event['category'] = 'magical'
                possible_events.append(event)
        
        # Check for political events
        for event_id, event in self.events['political'].items():
            if self.check_event_conditions(event):
                # Kategorie zum Ereignis hinzufügen
                event['category'] = 'political'
                possible_events.append(event)
        
        # Randomly select some events based on their type
        selected_events = []
        if possible_events:
            # Reduzierte Wahrscheinlichkeiten für alle Ereignistypen
            natural_chance = 0.01
            magical_chance = 0.005
            political_chance = 0.01
            
            for event in possible_events:
                category = event.get('category', '')
                if category == 'natural' and random.random() < natural_chance:
                    selected_events.append(event)
                elif category == 'magical' and random.random() < magical_chance:
                    selected_events.append(event)
                elif category == 'political' and random.random() < political_chance:
                    selected_events.append(event)
        
        # Apply effects and track followup events
        for event in selected_events:
            self._apply_effect(event['effects'])
            self.active_events.extend(event['followup_events'])
        
        return selected_events