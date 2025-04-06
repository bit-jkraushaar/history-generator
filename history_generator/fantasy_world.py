from .event_processor import EventProcessor
from .logger_config import world_logger
import os

class FantasyWorld:
    def __init__(self):
        self.year = 1000
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