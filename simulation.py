from person import Person, male_names, female_names
from marriage_market import MarriageMarket
from dynasty import Dynasty
import random

class Simulation:
    def __init__(self, start_year=1000, duration=50):
        self.year = start_year
        self.end_year = start_year + duration
        self.dynasties = []
        self.marriage_market = MarriageMarket()

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

    def simulate(self):
        while self.year < self.end_year:
            self.marriage_market.update(self.year)
            
            # Collect and process all events
            all_events = []
            for dynasty in self.dynasties:
                events = dynasty.simulate_year(self.year, self.marriage_market)
                all_events.extend(events)
            
            # Sort events by type and print them
            if all_events:
                print(f"\n🗓 Year {self.year}")
                for event in sorted(all_events, key=lambda e: (e.year, type(e).__name__)):
                    print(f"  {event.message}")
            
            self.year += 1

    def debug_print(self):
        for dynasty in self.dynasties:
            dynasty.show_family_tree()
