from typing import Dict, List, Optional, Any
import json
from enum import Enum
import random

class ConditionType(Enum):
    SEASON = "season"
    YEAR = "year"
    STAT = "stat"
    FACTION = "faction"
    REGION = "region"

class EffectType(Enum):
    MODIFY_STAT = "modify_stat"
    CHANGE_LEADER = "change_leader"
    TRIGGER_EVENT = "trigger_event"

class EventProcessor:
    def __init__(self, event_file: str):
        self.event_definitions = self._load_events(event_file)
        self.pending_events = []
        self.common_conditions = self._load_common_conditions()
        self.validate_events()

    def _load_events(self, event_file: str) -> Dict:
        with open(event_file, 'r') as f:
            return json.load(f)

    def _load_common_conditions(self) -> Dict:
        return {
            "realm_in_crisis": {
                "type": "faction",
                "faction": "Noble Houses",
                "stat": "stability",
                "operator": "<=",
                "value": 30
            },
            "magical_instability": {
                "type": "region",
                "region": "Central Valley",
                "stat": "magical_energy",
                "operator": ">=",
                "value": 30
            }
        }

    def validate_events(self):
        """Validiert die Event-Definitionen auf Vollständigkeit und Korrektheit."""
        required_fields = ["id", "name", "conditions", "effects"]
        
        for category in self.event_definitions["events"].values():
            for event_id, event in category.items():
                # Prüfe erforderliche Felder
                for field in required_fields:
                    if field not in event:
                        raise ValueError(f"Event {event_id} missing required field: {field}")
                
                # Prüfe Bedingungen
                for condition in event["conditions"]:
                    if not all(k in condition for k in ["type", "operator", "value"]):
                        raise ValueError(f"Invalid condition in {event_id}")
                
                # Prüfe Effekte
                for effect in event["effects"]:
                    if "type" not in effect:
                        raise ValueError(f"Effect missing type in {event_id}")
                
                # Prüfe Folgeereignisse
                for followup in event.get("followup_events", []):
                    if not self._event_exists(followup["id"]):
                        raise ValueError(f"Followup event {followup['id']} not found in {event_id}")

    def _event_exists(self, event_id: str) -> bool:
        """Prüft, ob ein Event mit der gegebenen ID existiert."""
        for category in self.event_definitions["events"].values():
            if event_id in category:
                return True
        return False

    def _evaluate_condition(self, condition: Dict, world_state: Dict) -> bool:
        """Wertet eine einzelne Bedingung aus."""
        condition_type = condition["type"]
        operator = condition["operator"]
        value = condition["value"]
        
        if condition_type == "common":
            common_condition = self.common_conditions.get(value)
            if common_condition:
                return self._evaluate_condition(common_condition, world_state)
            return False
            
        if condition_type == "season":
            current_season = world_state.get("season")
            return self._compare_values(current_season, operator, value)
            
        if condition_type == "year":
            current_year = world_state.get("year")
            return self._compare_values(current_year, operator, value)
            
        if condition_type in ["faction", "region"]:
            entity_type = "factions" if condition_type == "faction" else "regions"
            entity = condition[condition_type]
            stat = condition["stat"]
            current_value = world_state.get(entity_type, {}).get(entity, {}).get(stat)
            return self._compare_values(current_value, operator, value)
            
            result = self._compare_values(current_value, operator, value)
            print(f"    {condition_type} {entity} {stat}: {current_value} {operator} {value} -> {result}")
            return result
            
        return False

    def _compare_values(self, a: Any, operator: str, b: Any) -> bool:
        """Vergleicht zwei Werte basierend auf dem Operator."""
        if operator == "==":
            return a == b
        elif operator == "!=":
            return a != b
        elif operator == ">":
            return a > b
        elif operator == ">=":
            return a >= b
        elif operator == "<":
            return a < b
        elif operator == "<=":
            return a <= b
        return False

    def _apply_effect(self, effect: Dict, world_state: Dict):
        """Wendet einen einzelnen Effekt an."""
        effect_type = effect["type"]
        
        if effect_type == "modify_stat":
            entity_type = "factions" if "faction" in effect else "regions"
            entity = effect.get("faction") or effect.get("region")
            stat = effect["stat"]
            value = effect["value"]
            
            if entity_type not in world_state:
                world_state[entity_type] = {}
            if entity not in world_state[entity_type]:
                world_state[entity_type][entity] = {}
                
            current_value = world_state[entity_type][entity].get(stat, 0)
            new_value = current_value + value
            
            # Begrenze die Werte auf einen sinnvollen Bereich (0-100)
            new_value = max(0, min(100, new_value))
            
            world_state[entity_type][entity][stat] = new_value
            print(f"    {entity_type}.{entity}.{stat}: {current_value} -> {new_value}")
            
        elif effect_type == "change_leader":
            faction = effect["faction"]
            new_leader = effect["new_leader"]
            if "factions" in world_state and faction in world_state["factions"]:
                world_state["factions"][faction]["leader"] = new_leader

    def process_events(self, world_state: Dict) -> List[Dict]:
        """Verarbeitet alle Events für den aktuellen Zustand."""
        triggered_events = []
        
        # Verarbeite reguläre Events
        for category_name, category in self.event_definitions["events"].items():
            possible_events = []
            
            # Sammle alle möglichen Events
            for event_id, event in category.items():
                if self.check_conditions(event["conditions"], world_state):
                    possible_events.append(event)
            
            # Wähle zufällig maximal 1 Event pro Kategorie aus
            if possible_events:
                # Reduzierte Wahrscheinlichkeit für Events
                if random.random() < 0.3:  # 30% Chance pro Kategorie
                    selected_events = random.sample(possible_events, min(1, len(possible_events)))
                    for event in selected_events:
                        self.apply_effects(event["effects"], world_state)
                        self.schedule_followups(event, world_state["year"])
                        triggered_events.append({
                            "id": event["id"],
                            "name": event["name"],
                            "category": category_name
                        })
        
        # Verarbeite ausstehende Events
        self._process_pending_events(world_state, triggered_events)
        
        return triggered_events

    def check_conditions(self, conditions: List[Dict], world_state: Dict) -> bool:
        """Prüft, ob alle Bedingungen erfüllt sind."""
        return all(self._evaluate_condition(condition, world_state) for condition in conditions)

    def apply_effects(self, effects: List[Dict], world_state: Dict):
        """Wendet alle Effekte an."""
        for effect in effects:
            self._apply_effect(effect, world_state)

    def schedule_followups(self, event: Dict, current_year: int):
        """Plant Folgeereignisse ein."""
        for followup in event.get("followup_events", []):
            self.pending_events.append({
                "event_id": followup["id"],
                "trigger_year": current_year + followup.get("delay", 1),
                "probability": followup.get("probability", 1.0)
            })

    def _process_pending_events(self, world_state: Dict, triggered_events: List[Dict]):
        """Verarbeitet ausstehende Events."""
        current_year = world_state["year"]
        remaining_events = []
        
        for pending in self.pending_events:
            if pending["trigger_year"] == current_year:
                if random.random() <= pending["probability"]:
                    event = self._get_event_by_id(pending["event_id"])
                    if event and self.check_conditions(event["conditions"], world_state):
                        self.apply_effects(event["effects"], world_state)
                        self.schedule_followups(event, current_year)
                        triggered_events.append({
                            "id": event["id"],
                            "name": event["name"],
                            "category": event.get("category", "unknown")
                        })
            else:
                remaining_events.append(pending)
                
        self.pending_events = remaining_events

    def _get_event_by_id(self, event_id: str) -> Optional[Dict]:
        """Sucht ein Event anhand seiner ID."""
        for category in self.event_definitions["events"].values():
            if event_id in category:
                return category[event_id]
        return None 