import json
from typing import Dict, Any, List, Tuple
import random

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
        self.events = self._load_events()
        self.active_events: Dict[str, int] = {}

    def _load_events(self) -> Dict[str, Any]:
        with open('event_definitions.json', 'r') as f:
            return json.load(f)['events']

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

    def _add_followup_events(self, followup_events: List[str]):
        # Priority for follow-up events (decreases each year)
        initial_priority = 3
        for event_id in followup_events:
            self.active_events[event_id] = initial_priority

    def update_active_events(self):
        # Reduce the priority of all active events by 1
        events_to_remove = []
        for event_id, priority in self.active_events.items():
            if priority > 1:
                self.active_events[event_id] = priority - 1
            else:
                # Remove events with priority 0
                events_to_remove.append(event_id)
        
        for event_id in events_to_remove:
            self.active_events.pop(event_id)

    def check_event_conditions(self, event: Dict[str, Any]) -> bool:
        for path, condition in event['conditions'].items():
            if path == 'year':
                if not self._check_condition(condition, self.state['year']):
                    return False
            else:
                value = self._get_value(path)
                if not self._check_condition(condition, value):
                    return False
        return True

    def generate_events(self) -> List[Dict[str, Any]]:
        possible_events = []
        
        # Dictionary to store event IDs for later
        event_id_map = {}
        
        # Check for natural events
        for event_id, event in self.events['natural'].items():
            if self.check_event_conditions(event):
                # Add category and ID to the event
                event['category'] = 'natural'
                event['id'] = event_id
                event_id_map[event_id] = event
                possible_events.append(event)
        
        # Check for magical events
        for event_id, event in self.events['magical'].items():
            if self.check_event_conditions(event):
                # Add category and ID to the event
                event['category'] = 'magical'
                event['id'] = event_id
                event_id_map[event_id] = event
                possible_events.append(event)
        
        # Check for political events
        for event_id, event in self.events['political'].items():
            if self.check_event_conditions(event):
                # Add category and ID to the event
                event['category'] = 'political'
                event['id'] = event_id
                event_id_map[event_id] = event
                possible_events.append(event)
        
        # Randomly select some events based on their type
        selected_events = []
        if possible_events:
            # Reduced probabilities for all event types
            natural_chance = 0.005  # Reduced from 0.01 to 0.005 (0.5%)
            magical_chance = 0.002  # Reduced from 0.005 to 0.002 (0.2%)
            political_chance = 0.004  # Reduced from 0.01 to 0.004 (0.4%)
            
            # Increased bonus for active events
            active_event_bonus_multiplier = 5.0
            
            for event in possible_events:
                event_id = event.get('id', '')
                category = event.get('category', '')
                
                # Base probability based on category
                base_chance = 0
                if category == 'natural':
                    base_chance = natural_chance
                elif category == 'magical':
                    base_chance = magical_chance
                elif category == 'political':
                    base_chance = political_chance
                
                # Increase probability for active events
                final_chance = base_chance
                if event_id in self.active_events:
                    # Probability is increased based on the priority of the event
                    priority = self.active_events[event_id]
                    final_chance = base_chance * (active_event_bonus_multiplier * priority)
                
                # Check if the event occurs
                if random.random() < final_chance:
                    selected_events.append(event)
        
        # Apply effects and track followup events
        for event in selected_events:
            self._apply_effect(event['effects'])
            # Use new method to add follow-up events
            self._add_followup_events(event['followup_events'])
        
        # Update priorities of active events for the next year
        self.update_active_events()
        
        return selected_events