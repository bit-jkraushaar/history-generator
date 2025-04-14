from .event_processor import EventProcessor
from .logger_config import world_logger
from .faction_templates import FactionTemplates
import os
import random

class FantasyWorld:
    def __init__(self):
        self.year = 1000
        # Initialize the faction templates
        self.faction_templates = FactionTemplates()
        
        self.regions = {
            "Northern Mountains": {
                "magical_energy": 30,
                "trade": 40,
                "fertility": 20,
                "creature_diversity": 50,
                "dragon_activity": 10
            },
            "Central Valley": {
                "magical_energy": 50,
                "trade": 70,
                "fertility": 80,
                "creature_diversity": 40
            },
            "Eastern Forests": {
                "magical_energy": 60,
                "trade": 30,
                "fertility": 55,
                "creature_diversity": 40
            },
            "Southern Plains": {
                "magical_energy": 20,
                "trade": 60,
                "fertility": 70,
                "creature_diversity": 30
            },
            "Western Deserts": {
                "magical_energy": 40,
                "trade": 40,
                "fertility": 10,
                "creature_diversity": 20
            },
            "Coastal Regions": {
                "magical_energy": 30,
                "trade": 80,
                "fertility": 50,
                "creature_diversity": 50
            }
        }
        self.factions = {
            "Mages' Guild": {
                "power": 60,
                "influence": 65,
                "stability": 70
            },
            "Noble Houses": {
                "power": 65,
                "influence": 70,
                "stability": 75
            },
            "Merchant League": {
                "power": 55,
                "influence": 60,
                "stability": 80,
                "trade_income": 70
            },
            "Rangers' Order": {
                "power": 55,
                "influence": 50,
                "stability": 85
            },
            "Temple of Light": {
                "power": 55,
                "influence": 75,
                "stability": 85
            },
            "Dark Brotherhood": {
                "power": 50,
                "influence": 40,
                "stability": 40
            }
        }
        
        try:
            event_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "event_definitions.json")
            self.event_processor = EventProcessor(event_file_path)
            world_logger.info("FantasyWorld successfully initialized")
        except Exception as e:
            world_logger.error(f"Error initializing EventProcessor: {e}")
            # Create an empty EventProcessor as fallback
            self.event_processor = EventProcessor("")
            self.event_processor.events = {"events": {}}
            world_logger.warning("EventProcessor initialized with empty definitions")

    def get_world_state(self):
        return {
            "current_year": self.year,
            "regions": self.regions,
            "factions": self.factions
        }

    def generate_events(self):
        world_logger.info(f"Generating events for year {self.year}")
        
        world_state = self.get_world_state()
        triggered_events = self.event_processor.process_events(world_state, self.year)
        
        if triggered_events:
            world_logger.info(f"Found fantasy events: {len(triggered_events)}")
            for event in triggered_events:
                world_logger.info(f"  {event['name']}")
            
        return triggered_events
        
    def generate_faction(self, template_id: str = None, name: str = None):
        """Generates a single faction based on a template"""
        if template_id:
            template = self.faction_templates.get_template(template_id)
            if not template:
                world_logger.warning(f"Faction template '{template_id}' not found. Using a random template.")
                template = self.faction_templates.get_random_template()
        else:
            template = self.faction_templates.get_random_template()
        
        faction_data = template.generate_faction(name)
        return faction_data
    
    def generate_factions(self, count: int = 6, required_types: list = None):
        """Generates a list of factions with optional required types"""
        world_logger.info(f"Generating {count} factions for the world")
        
        factions = {}
        
        # If specific faction types are required, generate these first
        if required_types:
            for template_id in required_types:
                if len(factions) >= count:
                    break
                
                faction_data = self.generate_faction(template_id)
                faction_name = self._generate_unique_faction_name(faction_data["type"], list(factions.keys()))
                factions[faction_name] = faction_data
                world_logger.info(f"Created required faction: {faction_name} ({faction_data['type']})")
        
        # Fill the rest with random factions
        remaining = count - len(factions)
        for _ in range(remaining):
            # Choose a random template
            template = self.faction_templates.get_random_template()
            faction_data = template.generate_faction()
            
            # Generate a unique name
            faction_name = self._generate_unique_faction_name(faction_data["type"], list(factions.keys()))
            factions[faction_name] = faction_data
            world_logger.info(f"Created random faction: {faction_name} ({faction_data['type']})")
        
        return factions
    
    def _generate_unique_faction_name(self, faction_type: str, existing_names: list):
        """Helper method to generate a unique faction name"""
        base_patterns = [
            f"The {faction_type} of {self._random_place_name()}",
            f"{self._random_adjective()} {faction_type}",
            f"{faction_type} of {self._random_concept()}",
            f"{faction_type} of the {self._random_concept()}",
        ]
        
        # Try up to 10 times to generate a unique name
        for _ in range(10):
            pattern = random.choice(base_patterns)
            name = pattern
            if name not in existing_names:
                return name
        
        # If all attempts fail, add a number
        return f"{random.choice(base_patterns)} {random.randint(1, 999)}"
    
    def _random_place_name(self):
        """Generates a random place name"""
        places = [
            "Silver Lake", "Mist Valley", "Iron Rock", "Dark Grove", "Clearing", 
            "Red Mountain", "Gold Coast", "Green Forest", "Black Water", "White Stone",
            "Dragon Mountain", "Storm Wind", "Sun Rock", "Moonlight", "Star Valley"
        ]
        return random.choice(places)
    
    def _random_adjective(self):
        """Generates a random adjective"""
        adjectives = [
            "Mighty", "Venerable", "Secret", "Ancient", "New",
            "Mystical", "Radiant", "Golden", "Silver", "Honorable",
            "Dark", "Shining", "Hidden", "Holy", "Royal"
        ]
        return random.choice(adjectives)
    
    def _random_concept(self):
        """Generates a random concept"""
        concepts = [
            "Dragons", "Sun", "Moon", "Stars", "Magic",
            "Wisdom", "Power", "Strength", "Honor", "Valor",
            "Knowledge", "Light", "Shadow", "Fire", "Water",
            "War", "Peace", "Trade", "Wealth", "Destiny"
        ]
        return random.choice(concepts)
    
    def initialize_factions(self, count: int = 6, required_types: list = None):
        """Initializes the factions for the world"""
        world_logger.info("Initializing factions for the Fantasy World")
        self.factions = self.generate_factions(count, required_types)
        
        # Initialize faction-specific events
        self._initialize_faction_events()
        
        world_logger.info(f"{len(self.factions)} factions have been initialized")
        
    def _initialize_faction_events(self):
        """Initialize faction-specific events for each faction"""
        world_logger.info("Initializing faction-specific events")
        
        # Make sure the event categories exist
        if "events" not in self.event_processor.events:
            self.event_processor.events["events"] = {}
            
        # Add categories if they don't exist
        if "faction_specific" not in self.event_processor.events["events"]:
            self.event_processor.events["events"]["faction_specific"] = {}
            
        faction_events_category = self.event_processor.events["events"]["faction_specific"]
        
        # Process each faction
        for faction_name, faction_data in self.factions.items():
            faction_type = faction_data.get("type")
            if not faction_type:
                continue
                
            # Find the template for this faction type
            for template_id, template in self.faction_templates.templates.items():
                if template.faction_type == faction_type:
                    # Get faction-specific events from the template
                    faction_events = template.get_events_for_faction(faction_name)
                    
                    # Add these events to the event processor
                    if faction_events:
                        world_logger.info(f"Adding {len(faction_events)} events for faction '{faction_name}'")
                        for event_id, event_data in faction_events.items():
                            faction_events_category[event_id] = event_data
                    
                    break