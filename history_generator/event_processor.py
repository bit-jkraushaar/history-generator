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
    COMMON = "common"

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

    def _validate_event_structure(self, events: dict) -> None:
        """
        Validates the basic structure of event definitions.
        
        Args:
            events: The event definitions to validate
            
        Raises:
            ValueError: If the event structure is invalid
        """
        if not isinstance(events, dict):
            raise ValueError("Event definitions must be a dictionary")
            
        if "events" not in events:
            event_logger.warning("No event definitions found, using empty dictionary")
            return
            
        if not isinstance(events["events"], dict):
            raise ValueError("'events' must be a dictionary")
            
        for category, category_events in events["events"].items():
            if not isinstance(category_events, dict):
                raise ValueError(f"Category '{category}' must contain a dictionary of events")
                
            for event_id, event_data in category_events.items():
                self._validate_event(event_id, event_data)
                
    def _validate_event(self, event_id: str, event_data: dict) -> None:
        """
        Validates a single event definition.
        
        Args:
            event_id: The ID of the event
            event_data: The event data to validate
            
        Raises:
            ValueError: If the event data is invalid
        """
        required_fields = ["name", "effects"]
        if not event_data.get("is_followup", False):  # Only require conditions for non-followup events
            required_fields.append("conditions")
            
        for field in required_fields:
            if field not in event_data:
                raise ValueError(f"Event '{event_id}' is missing required field '{field}'")
                
        if "conditions" in event_data and not isinstance(event_data["conditions"], list):
            raise ValueError(f"Event '{event_id}' conditions must be a list")
            
        if not isinstance(event_data["effects"], list):
            raise ValueError(f"Event '{event_id}' effects must be a list")
            
        if "conditions" in event_data:
            for condition in event_data["conditions"]:
                self._validate_condition(event_id, condition)
            
        for effect in event_data["effects"]:
            self._validate_effect(event_id, effect)
            
        # Validate followup events structure
        if "followup_events" in event_data:
            if not isinstance(event_data["followup_events"], list):
                raise ValueError(f"Event '{event_id}' followup_events must be a list")
                
            for followup in event_data["followup_events"]:
                if "id" not in followup:
                    raise ValueError(f"Event '{event_id}' followup event is missing 'id'")
                    
                # Validate delay and probability if present
                if "delay" in followup and not isinstance(followup["delay"], (int, float)):
                    raise ValueError(f"Event '{event_id}' followup event '{followup['id']}' has invalid delay")
                    
                if "probability" in followup:
                    prob = followup["probability"]
                    if not isinstance(prob, (int, float)) or prob < 0 or prob > 1:
                        raise ValueError(f"Event '{event_id}' followup event '{followup['id']}' has invalid probability")
            
    def _validate_condition(self, event_id: str, condition: dict) -> None:
        """
        Validates a condition.
        
        Args:
            event_id: The ID of the event containing the condition
            condition: The condition to validate
            
        Raises:
            ValueError: If the condition is invalid
        """
        if "type" not in condition:
            raise ValueError(f"Event '{event_id}' condition is missing 'type'")
            
        condition_type = condition["type"]
        if condition_type not in [t.value for t in ConditionType]:
            raise ValueError(f"Event '{event_id}' has invalid condition type '{condition_type}'")
            
        if condition_type == "region":
            if "region" not in condition:
                raise ValueError(f"Event '{event_id}' region condition is missing 'region'")
            if "stat" not in condition:
                raise ValueError(f"Event '{event_id}' region condition is missing 'stat'")
            if "operator" not in condition:
                raise ValueError(f"Event '{event_id}' region condition is missing 'operator'")
                
        elif condition_type == "faction":
            if "faction" not in condition:
                raise ValueError(f"Event '{event_id}' faction condition is missing 'faction'")
            if "stat" not in condition:
                raise ValueError(f"Event '{event_id}' faction condition is missing 'stat'")
            if "operator" not in condition:
                raise ValueError(f"Event '{event_id}' faction condition is missing 'operator'")
                
        elif condition_type == "year":
            if "operator" not in condition:
                raise ValueError(f"Event '{event_id}' year condition is missing 'operator'")
                
        elif condition_type == "common":
            if "value" not in condition:
                raise ValueError(f"Event '{event_id}' common condition is missing 'value'")
            
        if "operator" in condition and condition["operator"] not in ["==", "!=", ">", ">=", "<", "<="]:
            raise ValueError(f"Event '{event_id}' has invalid operator '{condition['operator']}'")
            
    def _validate_effect(self, event_id: str, effect: dict) -> None:
        """
        Validates an effect.
        
        Args:
            event_id: The ID of the event containing the effect
            effect: The effect to validate
            
        Raises:
            ValueError: If the effect is invalid
        """
        if "type" not in effect:
            raise ValueError(f"Event '{event_id}' effect is missing 'type'")
            
        effect_type = effect["type"]
        if effect_type not in [t.value for t in EffectType]:
            raise ValueError(f"Event '{event_id}' has invalid effect type '{effect_type}'")
            
        if effect_type == "modify_stat":
            if not (effect.get("region") or effect.get("faction")):
                raise ValueError(f"Event '{event_id}' modify_stat effect must specify region or faction")
            if "stat" not in effect:
                raise ValueError(f"Event '{event_id}' modify_stat effect is missing 'stat'")
            if "value" not in effect:
                raise ValueError(f"Event '{event_id}' modify_stat effect is missing 'value'")
                
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
            if not self.event_file_path:
                event_logger.warning("No event file path provided, using empty event definitions")
                return {"events": {}}
                
            with open(self.event_file_path, 'r') as file:
                events = json.load(file)
                
            # Validate event structure
            self._validate_event_structure(events)
            
            # Validate followup event references
            for category_events in events.get("events", {}).values():
                for event_id, event_data in category_events.items():
                    if "followup_events" in event_data:
                        for followup in event_data["followup_events"]:
                            referenced_event = None
                            for cat_events in events.get("events", {}).values():
                                if followup["id"] in cat_events:
                                    referenced_event = cat_events[followup["id"]]
                                    break
                                    
                            if referenced_event is None:
                                raise ValueError(f"Event '{event_id}' references non-existent followup event '{followup['id']}'")
            
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
        """
        Process events for the current year.
        
        Args:
            world_state: The current state of the world
            current_year: The current year
            
        Returns:
            list: The triggered events
        """
        triggered_events = []
        world_logger.info(f"Processing events for year {current_year}")
        world_logger.debug(f"Current world state: {world_state}")

        # Process delayed events first
        delayed_events = world_state.get("delayed_events", [])
        new_delayed_events = []
        
        for delayed_event in delayed_events:
            if delayed_event["trigger_year"] <= current_year:
                if random.random() < delayed_event.get("probability", 0.5):
                    event_data = self._get_event_by_id(delayed_event["event_id"])
                    if event_data:
                        event_data['category'] = delayed_event.get('category', 'unknown')
                        event_logger.info(f"Delayed event triggered: {event_data['name']}")
                        for effect in event_data.get("effects", []):
                            self._apply_effect(effect, world_state)
                        triggered_events.append(event_data)
            else:
                new_delayed_events.append(delayed_event)
        
        world_state["delayed_events"] = new_delayed_events

        # Process regular events
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
                
                # Schedule followup events
                for followup in event_data.get("followup_events", []):
                    delay = followup.get("delay", 0)
                    if delay > 0:
                        # Schedule for future
                        delayed_event = {
                            "event_id": followup["id"],
                            "trigger_year": current_year + delay,
                            "probability": followup.get("probability", 0.5),
                            "category": category
                        }
                        world_state.setdefault("delayed_events", []).append(delayed_event)
                    else:
                        # Trigger immediately
                        if random.random() < followup.get("probability", 0.5):
                            followup_event = self._get_event_by_id(followup["id"])
                            if followup_event:
                                followup_event['category'] = category
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
        """
        Gets an event by its ID and marks it as a followup event.
        
        Args:
            event_id: The ID of the event to get
            
        Returns:
            dict: The event data, or None if not found
        """
        for category_events in self.events.get("events", {}).values():
            if event_id in category_events:
                event_data = category_events[event_id].copy()  # Create a copy to avoid modifying the original
                event_data["is_followup"] = True  # Mark as followup event
                return event_data
        return None 