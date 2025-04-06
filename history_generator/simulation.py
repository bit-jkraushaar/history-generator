from .person import Person, male_names, female_names
from .marriage_market import MarriageMarket
from .dynasty import Dynasty
from .fantasy_events import FantasyEventGenerator, FantasyWorld
import random

class Simulation:
    def __init__(self, start_year=1000, duration=50):
        self.year = start_year
        self.end_year = start_year + duration
        self.dynasties = []
        self.marriage_market = MarriageMarket()
        self.fantasy_world = FantasyWorld()
        self.fantasy_generator = FantasyEventGenerator(self.fantasy_world)

    def create_dynasty(self, name: str):
        # random age for king & queen
        king_age = random.randint(20, 40)
        queen_age = random.randint(20, 40)
        birth_year = self.year - king_age

        king = Person(random.choice(male_names), king_age, 100, "male", birth_year)
        queen = Person(random.choice(female_names), queen_age, 100, "female", birth_year)
        king.marry(queen)

        dynasty = Dynasty(name, king, queen)
        print(f"{king.name} is married to {king.partner.name if king.partner else 'nobody'}")
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
        
        return all_events

    def increment_year(self):
        self.year += 1

    def debug_print(self):
        for dynasty in self.dynasties:
            dynasty.show_family_tree()
