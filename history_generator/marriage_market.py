import random
from dataclasses import dataclass
from typing import Optional
from .person import Person
from .config.settings import MARRIAGE
from .logger_config import world_logger

@dataclass
class MarriageCandidate:
    """
    Represents a person available for marriage.
    
    Attributes:
        person: The person who is available for marriage
        remaining_years: Number of years the person will remain in the marriage market
    """
    person: Person
    remaining_years: int

class MarriageMarket:
    """
    Manages the marriage market where eligible persons can find partners.
    """
    
    def __init__(self, person_manager):
        """
        Initializes a new marriage market.
        
        Args:
            person_manager: The PersonManager instance to use
        """
        self.candidates = []
        self.person_manager = person_manager
        self.new_candidate_chance = 0.1
        self.factions = ["Noble Houses", "Commoners", "Merchants"]
        self.regions = ["Central Valley", "Northern Plains", "Southern Forests"]
        self.max_age_difference = 10

    def update(self, year: int) -> None:
        """
        Updates the marriage market for the current year.
        
        Args:
            year: The current year
        """
        # Decrease remaining years and remove unavailable candidates
        self.candidates = [c for c in self.candidates 
                         if c.remaining_years > 0 and 
                         not c.person.is_dead(year) and 
                         len(c.person.partners) == 0]
        
        for c in self.candidates:
            c.remaining_years -= 1
            
        # Add new random candidates
        if random.random() < self.new_candidate_chance:
            gender = random.choice(["male", "female"])
            person = Person(
                name=Person.generate_random_name(gender),
                gender=gender,
                birth_year=year - random.randint(16, 30),
                faction=random.choice(self.factions),
                region=random.choice(self.regions)
            )
            self.candidates.append(MarriageCandidate(person, remaining_years=5))
            world_logger.debug(f"Added new marriage candidate: {person.name}")

    def find_partner(self, person: Person) -> Optional[Person]:
        """
        Finds a suitable partner for a person.
        
        Args:
            person: The person seeking a partner
            
        Returns:
            A suitable partner or None if none found
        """
        suitable_candidates = [
            c for c in self.candidates
            if (c.person.gender != person.gender and  # Different gender
                len(c.person.partners) == 0 and  # Not married
                abs(c.person.age - person.age) <= self.max_age_difference)  # Age difference within limit
        ]
        
        if suitable_candidates:
            chosen = random.choice(suitable_candidates)
            return chosen.person
        return None

    def remove(self, person: Person) -> None:
        """
        Removes a person from the marriage market.
        
        Args:
            person: The person to remove
        """
        self.candidates = [c for c in self.candidates if c.person != person]
        world_logger.debug(f"Removed {person.name} from marriage market")
