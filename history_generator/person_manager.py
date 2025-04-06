from typing import List, Optional
from .person import Person
from .logger_config import world_logger

class PersonManager:
    """
    Manages the lifecycle and states of all persons in the simulation.
    
    This class is responsible for:
    - Creating new persons
    - Tracking all active persons
    - Removing deceased persons
    - Providing persons to other systems
    """
    
    def __init__(self):
        """Initializes a new PersonManager."""
        self._persons: List[Person] = []
        world_logger.info("PersonManager initialized")
        
    def add_person(self, person: Person) -> None:
        """
        Adds a new person to the management.
        
        Args:
            person: The person to add
        """
        if person not in self._persons:
            self._persons.append(person)
            world_logger.debug(f"Added person {person.name} to management")
            
    def remove_person(self, person: Person) -> None:
        """
        Removes a person from the management.
        
        Args:
            person: The person to remove
        """
        if person in self._persons:
            self._persons.remove(person)
            world_logger.debug(f"Removed person {person.name} from management")
            
    def get_person_by_id(self, person_id: int) -> Optional[Person]:
        """
        Searches for a person by their ID.
        
        Args:
            person_id: The ID of the person to find
            
        Returns:
            The found person or None if no person with the ID exists
        """
        for person in self._persons:
            if person.id == person_id:
                return person
        return None
        
    def get_all_persons(self) -> List[Person]:
        """
        Returns a list of all managed persons.
        
        Returns:
            List of all active persons
        """
        return self._persons.copy()  # Return a copy to prevent external modifications
        
    def get_living_persons(self) -> List[Person]:
        """
        Returns a list of all living persons.
        
        Returns:
            List of all living persons
        """
        return [person for person in self._persons if not person.is_dead()]
        
    def cleanup_dead_persons(self, current_year: int) -> None:
        """
        Removes deceased persons from the management.
        
        Args:
            current_year: The current year of the simulation
        """
        dead_persons = [person for person in self._persons if person.is_dead(current_year)]
        for person in dead_persons:
            self.remove_person(person)
            world_logger.info(f"Removed deceased person {person.name} from management")
            
    def get_persons_by_faction(self, faction_name: str) -> List[Person]:
        """
        Returns all persons of a specific faction.
        
        Args:
            faction_name: Name of the faction
            
        Returns:
            List of all persons in the faction
        """
        return [person for person in self._persons if person.faction == faction_name]
        
    def get_persons_by_region(self, region_name: str) -> List[Person]:
        """
        Returns all persons in a specific region.
        
        Args:
            region_name: Name of the region
            
        Returns:
            List of all persons in the region
        """
        return [person for person in self._persons if person.region == region_name] 