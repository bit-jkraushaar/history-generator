import json
from enum import Enum
import random
from .logger_config import event_logger, world_logger

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
    def __init__(self, event_file_path):
        self.event_file_path = event_file_path
        self.events = self._load_events()
        self.common_conditions = {
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
                "value": 80
            }
        }
        event_logger.info("EventProcessor initialized")

    def _load_events(self):
        """
        Loads event definitions from the JSON file.
        
        Returns:
            dict: The loaded event definitions or an empty dictionary in case of error
            
        Raises:
            FileNotFoundError: When the event file cannot be found
            json.JSONDecodeError: When the JSON file is invalid
            ValueError: When the event definitions are invalid
        """
        try:
            with open(self.event_file_path, 'r') as file:
                events = json.load(file)
                
            # Validate event structure
            if not isinstance(events, dict):
                raise ValueError("Event definitions must be a dictionary")
                
            if "events" not in events:
                event_logger.warning("No event definitions found, using empty dictionary")
                return {"events": {}}
                
            if not isinstance(events["events"], dict):
                raise ValueError("'events' must be a dictionary")
                
            return events
            
        except FileNotFoundError:
            event_logger.error(f"Event file not found: {self.event_file_path}")
            raise
        except json.JSONDecodeError as e:
            event_logger.error(f"Invalid JSON format in event file: {e}")
            raise
        except ValueError as e:
            event_logger.error(f"Invalid event definitions: {e}")
            raise
        except Exception as e:
            event_logger.error(f"Unexpected error while loading events: {e}")
            raise

    def process_events(self, world_state, current_year):
        triggered_events = []
        world_logger.info(f"Processing events for year {current_year}")
        world_logger.debug(f"Current world state: {world_state}")

        for category, category_events in self.events.get("events", {}).items():
            possible_events = []
            for event_id, event_data in category_events.items():
                if self._check_conditions(event_data.get("conditions", []), world_state):
                    possible_events.append((event_id, event_data))

            if possible_events:
                # Randomly select an event from possible events
                event_id, event_data = random.choice(possible_events)
                event_data['category'] = category  # Add category to event data
                event_logger.info(f"Event triggered: {event_data['name']} ({category})")
                
                # Apply effects
                for effect in event_data.get("effects", []):
                    self._apply_effect(effect, world_state)
                
                triggered_events.append(event_data)
                
                # Check for followup events
                for followup in event_data.get("followup_events", []):
                    if random.random() < followup.get("probability", 0.5):
                        followup_event = self._get_event_by_id(followup["id"])
                        if followup_event:
                            followup_event['category'] = category  # Add category to followup event
                            event_logger.info(f"Followup event triggered: {followup_event['name']}")
                            for effect in followup_event.get("effects", []):
                                self._apply_effect(effect, world_state)
                            triggered_events.append(followup_event)

        return triggered_events

    def _check_conditions(self, conditions, world_state):
        for condition in conditions:
            if not self._evaluate_condition(condition, world_state):
                return False
        return True

    def _evaluate_condition(self, condition, world_state):
        condition_type = condition.get("type")
        
        if condition_type == "common":
            common_condition = self.common_conditions.get(condition.get("value"))
            if common_condition:
                return self._evaluate_condition(common_condition, world_state)
            return False
            
        elif condition_type == "year":
            current_year = world_state.get("current_year", 0)
            operator = condition.get("operator")
            value = condition.get("value", 0)
            
            if operator == ">=":
                return current_year >= value
            elif operator == "<=":
                return current_year <= value
            elif operator == "==":
                return current_year == value
            return False
            
        elif condition_type == "region":
            region = condition.get("region")
            stat = condition.get("stat")
            operator = condition.get("operator")
            value = condition.get("value", 0)
            
            region_data = world_state.get("regions", {}).get(region, {})
            current_value = region_data.get(stat, 0)
            
            if operator == ">=":
                return current_value >= value
            elif operator == "<=":
                return current_value <= value
            elif operator == "==":
                return current_value == value
            return False
            
        elif condition_type == "faction":
            faction = condition.get("faction")
            stat = condition.get("stat")
            operator = condition.get("operator")
            value = condition.get("value", 0)
            
            faction_data = world_state.get("factions", {}).get(faction, {})
            current_value = faction_data.get(stat, 0)
            
            if operator == ">=":
                return current_value >= value
            elif operator == "<=":
                return current_value <= value
            elif operator == "==":
                return current_value == value
            return False
            
        return False

    def _apply_effect(self, effect, world_state):
        effect_type = effect.get("type")
        
        if effect_type == "modify_stat":
            target_type = effect.get("region") or effect.get("faction")
            stat = effect.get("stat")
            value = effect.get("value", 0)
            
            if effect.get("region"):
                current_value = world_state.get("regions", {}).get(target_type, {}).get(stat, 0)
                new_value = max(0, min(100, current_value + value))
                world_state.setdefault("regions", {}).setdefault(target_type, {})[stat] = new_value
                world_logger.debug(f"Region {target_type} {stat}: {current_value} -> {new_value}")
            elif effect.get("faction"):
                current_value = world_state.get("factions", {}).get(target_type, {}).get(stat, 0)
                new_value = max(0, min(100, current_value + value))
                world_state.setdefault("factions", {}).setdefault(target_type, {})[stat] = new_value
                world_logger.debug(f"Faction {target_type} {stat}: {current_value} -> {new_value}")

    def _get_event_by_id(self, event_id):
        for category_events in self.events.get("events", {}).values():
            if event_id in category_events:
                return category_events[event_id]
        return None 