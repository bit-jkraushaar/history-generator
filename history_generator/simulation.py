from .person import Person
from .person_manager import PersonManager
from .marriage_market import MarriageMarket
from .dynasty import Dynasty
from .fantasy_events import FantasyEventGenerator, FantasyWorld
import random

class Simulation:
    def __init__(self, start_year=1000, duration=50):
        self.year = start_year
        self.end_year = start_year + duration
        self.dynasties = []
        self.person_manager = PersonManager()
        self.marriage_market = MarriageMarket(self.person_manager)
        self.fantasy_world = FantasyWorld()
        self.fantasy_generator = FantasyEventGenerator(self.fantasy_world)

    def create_dynasty(self, name: str):
        # random age for king & queen
        king_age = random.randint(20, 40)
        queen_age = random.randint(20, 40)
        birth_year = self.year - king_age

        # Create king and queen with appropriate faction and region
        king = Person(
            name=Person.generate_random_name("male"),
            gender="male",
            birth_year=birth_year,
            faction="Noble Houses",
            region="Central Valley"
        )
        queen = Person(
            name=Person.generate_random_name("female"),
            gender="female",
            birth_year=birth_year,
            faction="Noble Houses",
            region="Central Valley"
        )
        
        # Add persons to manager
        self.person_manager.add_person(king)
        self.person_manager.add_person(queen)
        
        # Marry them
        king.marry(queen)

        dynasty = Dynasty(name, king, queen)
        print(f"{king.name} is married to {queen.name}")
        self.dynasties.append(dynasty)

    def simulate_year(self):
        self.marriage_market.update(self.year)
        
        # Collect and process all events
        all_events = []
        
        # Get dynasty events
        for dynasty in self.dynasties:
            events = dynasty.simulate_year(self.year, self.marriage_market)
            all_events.extend(events)
        
        # Get fantasy world events
        fantasy_events = self.fantasy_generator.generate_events(self.year)
        all_events.extend(fantasy_events)
        
        # Clean up dead persons
        self.person_manager.cleanup_dead_persons(self.year)
        
        return all_events

    def increment_year(self):
        self.year += 1

    def debug_print(self):
        # Set current year for family tree display
        for dynasty in self.dynasties:
            for person in dynasty.family:
                if not person.is_dead(self.year):
                    person.death_year = None  # Reset death year for living persons
            dynasty.show_family_tree()

    def get_current_year(self):
        """Returns the current simulation year."""
        return self.year
