from typing import Optional, List
from datetime import datetime
import random
from .logger_config import world_logger
from .config.names import MALE_NAMES, FEMALE_NAMES
from .config.settings import PERSON, CHILDBIRTH

class Person:
    """
    Represents a person in the simulation.
    
    Attributes:
        id: Unique ID of the person
        name: Name of the person
        gender: Gender of the person
        birth_year: Year of birth
        death_year: Year of death (None if alive)
        faction: Faction the person belongs to
        region: Region where the person lives
        health: Health status (0-100)
        partners: List of partners (current and previous)
        children: List of children
    """
    
    @classmethod
    def generate_random_name(cls, gender: str) -> str:
        """
        Generates a random name based on gender.
        
        Args:
            gender: Gender of the person ('male' or 'female')
            
        Returns:
            A randomly selected name
        """
        if gender.lower() == 'male':
            return random.choice(MALE_NAMES)
        elif gender.lower() == 'female':
            return random.choice(FEMALE_NAMES)
        else:
            raise ValueError(f"Invalid gender: {gender}")
    
    def __init__(self, name: str, gender: str, birth_year: int, faction: str, region: str):
        """
        Initializes a new person.
        
        Args:
            name: Name of the person
            gender: Gender of the person
            birth_year: Year of birth
            faction: Faction the person belongs to
            region: Region where the person lives
        """
        self.id = id(self)  # Unique ID based on object ID
        self.name = name
        self.gender = gender
        self.birth_year = birth_year
        self.death_year = None
        self.faction = faction
        self.region = region
        self.health = PERSON["initial_health"]
        self.partners = []
        self.children = []
        world_logger.debug(f"Created new person: {name}")
        
    @property
    def age(self) -> int:
        """Calculates the current age of the person."""
        if self.death_year:
            return self.death_year - self.birth_year
        return 0  # Age will be calculated based on current_year in is_dead method
        
    def is_dead(self, current_year: Optional[int] = None) -> bool:
        """
        Checks if the person is deceased.
        
        Args:
            current_year: Optional year for calculation
            
        Returns:
            True if the person is deceased, False otherwise
        """
        if self.death_year is not None:
            return True
            
        if current_year is None:
            return False  # If no year is provided, assume person is alive
            
        age = current_year - self.birth_year
        
        # Only set death_year if the person actually dies
        if self.health <= 0 or age > PERSON["max_base_age"] + random.randint(0, PERSON["max_age_bonus"]):
            self.death_year = current_year
            return True
            
        return False
        
    def marry(self, partner: 'Person') -> None:
        """
        Marries another person.
        
        Args:
            partner: The person to marry
        """
        if partner not in self.partners:
            self.partners.append(partner)
            if self not in partner.partners:
                partner.partners.append(self)
            world_logger.info(f"{self.name} married {partner.name}")
            
    def can_have_child(self, current_year: int) -> bool:
        """
        Checks if the person can have a child.
        
        Args:
            current_year: The current year
            
        Returns:
            True if the person can have a child, False otherwise
        """
        age = current_year - self.birth_year
        has_living_partner = any(not p.is_dead(current_year) for p in self.partners)
        return (self.gender == "female" and 
                has_living_partner and 
                CHILDBIRTH["min_age"] < age < CHILDBIRTH["max_age"] and 
                not self.is_dead(current_year))
                
    def __str__(self) -> str:
        """Returns a string representation of the person."""
        return f"{self.name} ({self.gender}, {self.age} years old)"