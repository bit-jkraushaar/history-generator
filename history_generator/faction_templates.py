from .logger_config import world_logger
import random
from typing import Dict, List, Any

# Blueprint for all faction types
class FactionTemplate:
    def __init__(self, 
                 faction_type: str, 
                 name_patterns: List[str], 
                 base_stats: Dict[str, int], 
                 specific_stats: Dict[str, int]):
        self.faction_type = faction_type
        self.name_patterns = name_patterns
        self.base_stats = base_stats  # power, influence, stability
        self.specific_stats = specific_stats  # type-specific statistics

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