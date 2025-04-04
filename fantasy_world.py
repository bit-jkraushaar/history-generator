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
                    "creature_diversity": 35  # Neues Attribut
                },
                "Southern Plains": {
                    "fertility": 70,
                    "trade": 60,
                    "magical_energy": 20,
                    "creature_diversity": 30  # Neues Attribut
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
                    "creature_diversity": 25  # Neues Attribut
                },
                "Central Valley": {
                    "magical_energy": 50,
                    "fertility": 80,
                    "trade": 70,
                    "creature_diversity": 45  # Neues Attribut
                },
                "Coastal Regions": {
                    "trade": 80,
                    "magical_energy": 30,
                    "fertility": 60,
                    "creature_diversity": 50  # Neues Attribut
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
        # Priorität für Folgeereignisse (sinkt mit jedem Jahr)
        initial_priority = 3
        for event_id in followup_events:
            self.active_events[event_id] = initial_priority

    def update_active_events(self):
        # Reduziere die Priorität aller aktiven Ereignisse um 1
        events_to_remove = []
        for event_id, priority in self.active_events.items():
            if priority > 1:
                self.active_events[event_id] = priority - 1
            else:
                # Entferne Ereignisse mit Priorität 0
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
        
        # Dictionary zum Speichern der Event-IDs für später
        event_id_map = {}
        
        # Check for natural events
        for event_id, event in self.events['natural'].items():
            if self.check_event_conditions(event):
                # Kategorie und ID zum Ereignis hinzufügen
                event['category'] = 'natural'
                event['id'] = event_id
                event_id_map[event_id] = event
                possible_events.append(event)
        
        # Check for magical events
        for event_id, event in self.events['magical'].items():
            if self.check_event_conditions(event):
                # Kategorie und ID zum Ereignis hinzufügen
                event['category'] = 'magical'
                event['id'] = event_id
                event_id_map[event_id] = event
                possible_events.append(event)
        
        # Check for political events
        for event_id, event in self.events['political'].items():
            if self.check_event_conditions(event):
                # Kategorie und ID zum Ereignis hinzufügen
                event['category'] = 'political'
                event['id'] = event_id
                event_id_map[event_id] = event
                possible_events.append(event)
        
        # Randomly select some events based on their type
        selected_events = []
        if possible_events:
            # Reduzierte Wahrscheinlichkeiten für alle Ereignistypen
            natural_chance = 0.005  # Reduziert von 0.01 auf 0.005 (0.5%)
            magical_chance = 0.002  # Reduziert von 0.005 auf 0.002 (0.2%)
            political_chance = 0.004  # Reduziert von 0.01 auf 0.004 (0.4%)
            
            # Erhöhter Bonus für aktive Ereignisse
            active_event_bonus_multiplier = 5.0
            
            for event in possible_events:
                event_id = event.get('id', '')
                category = event.get('category', '')
                
                # Standardwahrscheinlichkeit basierend auf Kategorie
                base_chance = 0
                if category == 'natural':
                    base_chance = natural_chance
                elif category == 'magical':
                    base_chance = magical_chance
                elif category == 'political':
                    base_chance = political_chance
                
                # Erhöhe die Wahrscheinlichkeit für aktive Ereignisse
                final_chance = base_chance
                if event_id in self.active_events:
                    # Wahrscheinlichkeit wird erhöht basierend auf der Priorität des Ereignisses
                    priority = self.active_events[event_id]
                    final_chance = base_chance * (active_event_bonus_multiplier * priority)
                
                # Prüfe, ob das Ereignis eintritt
                if random.random() < final_chance:
                    selected_events.append(event)
        
        # Apply effects and track followup events
        for event in selected_events:
            self._apply_effect(event['effects'])
            # Neue Methode zum Hinzufügen von Folgeereignissen verwenden
            self._add_followup_events(event['followup_events'])
        
        # Aktualisiere die Prioritäten aktiver Ereignisse für das nächste Jahr
        self.update_active_events()
        
        return selected_events