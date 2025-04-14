from .logger_config import world_logger
import random
from typing import Dict, List, Any

# Blueprint for all faction types
class FactionTemplate:
    def __init__(self, 
                 faction_type: str, 
                 name_patterns: List[str], 
                 base_stats: Dict[str, int], 
                 specific_stats: Dict[str, int],
                 event_templates: Dict[str, Dict] = None):
        self.faction_type = faction_type
        self.name_patterns = name_patterns
        self.base_stats = base_stats  # power, influence, stability
        self.specific_stats = specific_stats  # type-specific statistics
        self.event_templates = event_templates or {}  # faction-specific events

    def generate_faction(self, name: str = None) -> Dict[str, Any]:
        """Generates a faction based on this blueprint"""
        # If no name was provided, generate a random name
        if not name:
            pattern = random.choice(self.name_patterns)
            name = pattern.replace("{type}", self.faction_type)
            # More complex name replacements could happen here later
        
        # Create base statistics with some variation
        faction_data = {}
        for stat, base_value in self.base_stats.items():
            variation = random.randint(-10, 10)
            faction_data[stat] = max(10, min(100, base_value + variation))
        
        # Add type-specific statistics
        for stat, base_value in self.specific_stats.items():
            variation = random.randint(-10, 10)
            faction_data[stat] = max(10, min(100, base_value + variation))
            
        # Add metadata
        faction_data["type"] = self.faction_type
        
        return faction_data
        
    def get_events_for_faction(self, faction_name: str) -> Dict[str, Dict]:
        """
        Generate faction-specific events based on the templates
        
        Args:
            faction_name: The name of the faction to generate events for
            
        Returns:
            dict: A dictionary of event IDs to event data
        """
        if not self.event_templates:
            return {}
            
        events = {}
        
        for event_id, event_template in self.event_templates.items():
            # Create a deep copy to avoid modifying the template
            event = event_template.copy()
            
            # Replace faction placeholders with actual faction name
            if "conditions" in event:
                for condition in event["conditions"]:
                    if condition.get("type") == "faction" and condition.get("faction") == "{faction}":
                        condition["faction"] = faction_name
            
            if "effects" in event:
                for effect in event["effects"]:
                    if effect.get("type") == "modify_stat" and effect.get("faction") == "{faction}":
                        effect["faction"] = faction_name
            
            # Create a unique ID for this faction's event
            unique_id = f"{faction_name}_{event_id}"
            events[unique_id] = event
            
        return events

# Collection of all available faction blueprints
class FactionTemplates:
    def __init__(self):
        self.templates = {
            "magic_guild": FactionTemplate(
                faction_type="Mages Guild",
                name_patterns=[
                    "The {type} of Arkania", 
                    "High {type}", 
                    "{type} of Knowledge",
                    "Arcane {type}"
                ],
                base_stats={
                    "power": 60,
                    "influence": 65,
                    "stability": 70
                },
                specific_stats={
                    "magical_knowledge": 75,
                    "arcane_influence": 70,
                    "research_capacity": 80
                },
                event_templates={
                    "arcane_breakthrough": {
                        "name": "Arkaner Durchbruch",
                        "description": "Die Magier machen einen bahnbrechenden Fortschritt in der arkanen Forschung",
                        "conditions": [
                            {
                                "type": "faction",
                                "faction": "{faction}",
                                "stat": "research_capacity",
                                "operator": ">=",
                                "value": 70
                            },
                            {
                                "type": "faction",
                                "faction": "{faction}",
                                "stat": "stability",
                                "operator": ">=",
                                "value": 60
                            }
                        ],
                        "effects": [
                            {
                                "type": "modify_stat",
                                "faction": "{faction}",
                                "stat": "power",
                                "value": 15
                            },
                            {
                                "type": "modify_stat",
                                "faction": "{faction}",
                                "stat": "influence",
                                "value": 10
                            }
                        ]
                    },
                    "magical_experiment_failure": {
                        "name": "Fehlgeschlagenes magisches Experiment",
                        "description": "Ein gefährliches Experiment geht schief und schadet dem Ansehen der Gilde",
                        "conditions": [
                            {
                                "type": "faction",
                                "faction": "{faction}",
                                "stat": "stability",
                                "operator": "<=",
                                "value": 40
                            }
                        ],
                        "effects": [
                            {
                                "type": "modify_stat",
                                "faction": "{faction}",
                                "stat": "stability",
                                "value": -15
                            },
                            {
                                "type": "modify_stat",
                                "faction": "{faction}",
                                "stat": "influence",
                                "value": -10
                            }
                        ]
                    }
                }
            ),
            
            "noble_house": FactionTemplate(
                faction_type="Noble House",
                name_patterns=[
                    "House {type}",
                    "The {type} Dynasty",
                    "Lordly {type}"
                ],
                base_stats={
                    "power": 65,
                    "influence": 70,
                    "stability": 75
                },
                specific_stats={
                    "legitimacy": 70,
                    "wealth": 80,
                    "military_strength": 65
                },
                event_templates={
                    "lavish_feast": {
                        "name": "Prächtiges Bankett",
                        "description": "Das Adelshaus veranstaltet ein opulentes Fest für Verbündete und Rivalen",
                        "conditions": [
                            {
                                "type": "faction",
                                "faction": "{faction}",
                                "stat": "wealth",
                                "operator": ">=",
                                "value": 70
                            }
                        ],
                        "effects": [
                            {
                                "type": "modify_stat",
                                "faction": "{faction}",
                                "stat": "influence",
                                "value": 15
                            },
                            {
                                "type": "modify_stat",
                                "faction": "{faction}",
                                "stat": "wealth",
                                "value": -10
                            }
                        ]
                    },
                    "military_campaign": {
                        "name": "Militärische Kampagne",
                        "description": "Das Adelshaus startet eine Kampagne, um seinen Einfluss zu erweitern",
                        "conditions": [
                            {
                                "type": "faction",
                                "faction": "{faction}",
                                "stat": "military_strength",
                                "operator": ">=",
                                "value": 60
                            },
                            {
                                "type": "faction",
                                "faction": "{faction}",
                                "stat": "stability",
                                "operator": ">=",
                                "value": 50
                            }
                        ],
                        "effects": [
                            {
                                "type": "modify_stat",
                                "faction": "{faction}",
                                "stat": "power",
                                "value": 15
                            },
                            {
                                "type": "modify_stat",
                                "faction": "{faction}",
                                "stat": "stability",
                                "value": -5
                            }
                        ]
                    }
                }
            ),
            
            "merchant_guild": FactionTemplate(
                faction_type="Merchant League",
                name_patterns=[
                    "{type} of the Golden Road",
                    "United {type}",
                    "{type} of the Rich Coasts"
                ],
                base_stats={
                    "power": 55,
                    "influence": 60,
                    "stability": 80
                },
                specific_stats={
                    "trade_income": 85,
                    "market_control": 75,
                    "diplomatic_network": 70
                },
                event_templates={
                    "new_trade_route": {
                        "name": "Neue Handelsroute",
                        "description": "Die Handelsgilde eröffnet eine profitable neue Handelsroute",
                        "conditions": [
                            {
                                "type": "faction",
                                "faction": "{faction}",
                                "stat": "diplomatic_network",
                                "operator": ">=",
                                "value": 65
                            }
                        ],
                        "effects": [
                            {
                                "type": "modify_stat",
                                "faction": "{faction}",
                                "stat": "trade_income",
                                "value": 20
                            },
                            {
                                "type": "modify_stat",
                                "faction": "{faction}",
                                "stat": "influence",
                                "value": 10
                            }
                        ]
                    },
                    "trade_monopoly": {
                        "name": "Handelsmonopol",
                        "description": "Die Gilde sichert sich ein Monopol auf wichtige Waren",
                        "conditions": [
                            {
                                "type": "faction",
                                "faction": "{faction}",
                                "stat": "market_control",
                                "operator": ">=",
                                "value": 70
                            },
                            {
                                "type": "faction",
                                "faction": "{faction}",
                                "stat": "influence",
                                "operator": ">=",
                                "value": 60
                            }
                        ],
                        "effects": [
                            {
                                "type": "modify_stat",
                                "faction": "{faction}",
                                "stat": "power",
                                "value": 10
                            },
                            {
                                "type": "modify_stat",
                                "faction": "{faction}",
                                "stat": "market_control",
                                "value": 15
                            }
                        ],
                        "followup_events": [
                            {
                                "id": "monopoly_backlash",
                                "probability": 0.4,
                                "delay": 2
                            }
                        ]
                    },
                    "monopoly_backlash": {
                        "name": "Widerstand gegen Monopol",
                        "description": "Andere Händler und die Bevölkerung wenden sich gegen das Monopol",
                        "is_followup": true,
                        "effects": [
                            {
                                "type": "modify_stat",
                                "faction": "{faction}",
                                "stat": "stability",
                                "value": -15
                            },
                            {
                                "type": "modify_stat",
                                "faction": "{faction}",
                                "stat": "influence",
                                "value": -10
                            }
                        ]
                    }
                }
            ),
            
            "religious_order": FactionTemplate(
                faction_type="Religious Order",
                name_patterns=[
                    "{type} of Light",
                    "Holy {type}",
                    "{type} of the Eternal Flame"
                ],
                base_stats={
                    "power": 55,
                    "influence": 75,
                    "stability": 85
                },
                specific_stats={
                    "faith_strength": 90,
                    "divine_favor": 70,
                    "healing_capacity": 65
                }
            ),
            
            "warrior_order": FactionTemplate(
                faction_type="Warrior Order",
                name_patterns=[
                    "{type} of the Brave",
                    "Honorable {type}",
                    "{type} of the Sword"
                ],
                base_stats={
                    "power": 70,
                    "influence": 50,
                    "stability": 75
                },
                specific_stats={
                    "martial_prowess": 85,
                    "discipline": 80,
                    "fortress_control": 70
                }
            ),
            
            "druid_circle": FactionTemplate(
                faction_type="Druid Circle",
                name_patterns=[
                    "{type} of the Ancient Forest",
                    "Nature-bonded {type}",
                    "{type} of the Four Seasons"
                ],
                base_stats={
                    "power": 50,
                    "influence": 45,
                    "stability": 80
                },
                specific_stats={
                    "nature_attunement": 90,
                    "animal_influence": 85,
                    "wilderness_control": 75
                }
            ),
            
            "thieves_guild": FactionTemplate(
                faction_type="Thieves Guild",
                name_patterns=[
                    "The Shadowy {type}",
                    "{type} of the Night",
                    "Hidden {type}"
                ],
                base_stats={
                    "power": 45,
                    "influence": 50,
                    "stability": 40
                },
                specific_stats={
                    "stealth": 90,
                    "information_network": 85,
                    "urban_control": 70
                }
            ),
            
            "assassins_brotherhood": FactionTemplate(
                faction_type="Assassins Brotherhood",
                name_patterns=[
                    "Dark {type}",
                    "{type} of Silent Death",
                    "Shadowy {type}"
                ],
                base_stats={
                    "power": 50,
                    "influence": 40,
                    "stability": 40
                },
                specific_stats={
                    "assassination_skill": 95,
                    "fear_factor": 85,
                    "secrecy": 90
                }
            ),
            
            "arcane_university": FactionTemplate(
                faction_type="Arcane University",
                name_patterns=[
                    "{type} of Thaumaturgica",
                    "Royal {type}",
                    "{type} of Higher Knowledge"
                ],
                base_stats={
                    "power": 55,
                    "influence": 70,
                    "stability": 75
                },
                specific_stats={
                    "arcane_knowledge": 90,
                    "research_output": 85,
                    "education_quality": 80
                }
            ),
            
            "monster_hunters": FactionTemplate(
                faction_type="Monster Hunters",
                name_patterns=[
                    "{type} Guild",
                    "The Silver {type}",
                    "Order of {type}"
                ],
                base_stats={
                    "power": 60,
                    "influence": 45,
                    "stability": 60
                },
                specific_stats={
                    "tracking_skill": 85,
                    "monster_knowledge": 90,
                    "combat_training": 80
                }
            )
        }
    
    def get_template(self, template_id: str) -> FactionTemplate:
        """Returns a specific faction blueprint"""
        return self.templates.get(template_id)
    
    def get_all_templates(self) -> Dict[str, FactionTemplate]:
        """Returns all available faction blueprints"""
        return self.templates
    
    def get_random_template(self) -> FactionTemplate:
        """Returns a random faction blueprint"""
        template_id = random.choice(list(self.templates.keys()))
        return self.templates[template_id]
    
    def generate_random_faction(self, template_id: str = None) -> Dict[str, Any]:
        """Generates a random faction based on a specific or random blueprint"""
        if template_id and template_id in self.templates:
            template = self.templates[template_id]
        else:
            template = self.get_random_template()
            
        return template.generate_faction()