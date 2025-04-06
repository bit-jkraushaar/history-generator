from typing import List, Optional
from .person import Person
from .marriage_market import MarriageMarket
from .events import SuccessionEvent, NoSuccessorEvent, DeathEvent, MarriageEvent, BirthEvent, Event
from .logger_config import world_logger
from .config.settings import MARRIAGE, CHILDBIRTH
import random

class Dynasty:
    """
    Represents a noble dynasty in the simulation.
    
    Attributes:
        name: Name of the dynasty
        founding_king: The first king of the dynasty
        founding_queen: The first queen of the dynasty
        monarch: The current monarch
        family: List of all family members
    """
    
    def __init__(self, name: str, king: Person, queen: Person):
        """
        Initializes a new dynasty.
        
        Args:
            name: Name of the dynasty
            king: The founding king
            queen: The founding queen
        """
        self.name = name
        self.founding_king = king
        self.founding_queen = queen
        self.monarch = king  # Only one monarch
        self.monarch.was_king = True
        self.family = [king, queen]
        world_logger.info(f"Created new dynasty: {name}")

    def simulate_year(self, year: int, marriage_market: MarriageMarket) -> List[Event]:
        """
        Simulates a year for the dynasty.
        
        Args:
            year: The current year
            marriage_market: The marriage market for finding partners
            
        Returns:
            List of events that occurred during the year
        """
        events = []
        
        # Process each family member
        for person in self.family[:]:  # Copy list to allow modification during iteration
            # Check for death
            if person.is_dead(year):
                age = year - person.birth_year
                events.append(DeathEvent(
                    year=year,
                    message=f"{person.name} has died at the age of {age}",
                    person_name=person.name,
                    age=age
                ))
                self.family.remove(person)
                
                # Handle succession if monarch dies
                if person == self.monarch:
                    succession_event = self._replace_monarch(year)
                    if succession_event:
                        events.append(succession_event)
                continue
            
            # Handle marriage
            if (len(person.partners) == 0 and 
                year - person.birth_year >= MARRIAGE["min_age"] and 
                random.random() < MARRIAGE["marriage_chance_base"] + 
                    (year - person.birth_year - MARRIAGE["min_age"]) * MARRIAGE["marriage_chance_increase"]):
                partner = marriage_market.find_partner(person)
                if partner:
                    person.marry(partner)
                    marriage_market.remove(partner)
                    events.append(MarriageEvent(
                        year=year,
                        message=f"{person.name} marries {partner.name}",
                        person1=person.name,
                        person2=partner.name,
                        age=year - person.birth_year
                    ))
            
            # Handle childbirth
            if person.can_have_child(year):
                # Find living partner
                living_partners = [p for p in person.partners if not p.is_dead(year)]
                if living_partners:
                    if random.random() < CHILDBIRTH["chance"]:
                        # Choose random gender
                        child_gender = random.choice(["male", "female"])
                        child_name = Person.generate_random_name(child_gender)
                        child = Person(child_name, child_gender, year, person.faction, person.region)
                        
                        # Add child to both parents
                        person.children.append(child)
                        living_partners[0].children.append(child)
                        self.family.append(child)
                        
                        events.append(BirthEvent(
                            year=year,
                            message=f"{person.name} and {living_partners[0].name} have a new child: {child_name}",
                            child_name=child_name,
                            mother_name=person.name if person.gender == "female" else living_partners[0].name,
                            father_name=person.name if person.gender == "male" else living_partners[0].name
                        ))

        return events

    def _replace_monarch(self, year: int) -> Optional[Event]:
        """
        Replaces the monarch after death.
        
        Args:
            year: The current year
            
        Returns:
            A succession event or None if no successor is found
        """
        # Find oldest living male child
        successor = None
        for person in self.family:
            if (person.gender == "male" and 
                not person.is_dead(year) and 
                not getattr(person, 'was_king', False) and
                (successor is None or person.birth_year < successor.birth_year)):
                successor = person

        if successor:
            old_monarch = self.monarch.name
            self.monarch = successor
            successor.was_king = True
            # Add crown to the new monarch
            self.monarch.was_king = True
            return SuccessionEvent(
                year=year,
                message=f"{successor.name} becomes the new monarch of {self.name}",
                old_monarch=old_monarch,
                new_monarch=successor.name,
                is_king=True
            )
        else:
            return NoSuccessorEvent(
                year=year,
                message=f"Dynasty {self.name} has no eligible successor",
                monarch_name=self.monarch.name,
                is_king=True
            )

    def show_family_tree(self):
        print(f"\nFamily tree of the {self.name} dynasty:")
        self._show_family_tree(self.founding_king, 0)

    def _show_family_tree(self, person, level, shown_persons=None):
        if shown_persons is None:
            shown_persons = set()
            
        if person in shown_persons:
            return
            
        shown_persons.add(person)
        
        status = "†" if person.is_dead() else ""
        crown = "👑 " if getattr(person, 'was_king', False) else ""
        gender = "♂ " if person.gender == "male" else "♀ "
        symbol = "├──" if level > 0 else ""
        year_info = f"{person.birth_year}–{person.death_year}" if person.death_year else f"{person.birth_year}–"
        output = "  " * level + f"{symbol}{crown}{gender}{person.name} ({status}{year_info})"
        if person.partners:
            partner_infos = []
            for p in person.partners:
                p_gender = "♂ " if p.gender == "male" else "♀ "
                p_status = "†" if p.is_dead() else ""
                p_year_info = f"{p.birth_year}–{p.death_year}" if p.death_year else f"{p.birth_year}–"
                partner_infos.append(f"{p_gender}{p.name} ({p_status}{p_year_info})")
            output += " ⚭ " + ", ".join(partner_infos)
        print(output)
        
        # Show children
        for child in person.children:
            self._show_family_tree(child, level + 1, shown_persons)
