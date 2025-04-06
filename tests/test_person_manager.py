import unittest
from datetime import datetime
from history_generator.person_manager import PersonManager
from history_generator.person import Person
from history_generator.config.settings import PERSON, CHILDBIRTH

class TestPersonManager(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.manager = PersonManager()
        self.current_year = datetime.now().year
        
        # Create test persons
        self.person1 = Person("Test1", "male", self.current_year - 20, "Noble Houses", "Central Valley")
        self.person2 = Person("Test2", "female", self.current_year - 25, "Mages' Guild", "Northern Mountains")
        self.person3 = Person("Test3", "male", self.current_year - 100, "Noble Houses", "Central Valley")  # Will be dead
        
    def test_add_person(self):
        """Test adding a person to the manager."""
        self.manager.add_person(self.person1)
        self.assertIn(self.person1, self.manager.get_all_persons())
        
    def test_remove_person(self):
        """Test removing a person from the manager."""
        self.manager.add_person(self.person1)
        self.manager.remove_person(self.person1)
        self.assertNotIn(self.person1, self.manager.get_all_persons())
        
    def test_get_person_by_id(self):
        """Test retrieving a person by ID."""
        self.manager.add_person(self.person1)
        found_person = self.manager.get_person_by_id(self.person1.id)
        self.assertEqual(found_person, self.person1)
        
    def test_get_all_persons(self):
        """Test retrieving all persons."""
        self.manager.add_person(self.person1)
        self.manager.add_person(self.person2)
        all_persons = self.manager.get_all_persons()
        self.assertEqual(len(all_persons), 2)
        self.assertIn(self.person1, all_persons)
        self.assertIn(self.person2, all_persons)
        
    def test_get_living_persons(self):
        """Test retrieving only living persons."""
        self.manager.add_person(self.person1)
        self.manager.add_person(self.person3)  # This person is dead
        # Force person3 to be dead by setting their health to 0
        self.person3.health = 0
        living_persons = self.manager.get_living_persons()
        self.assertEqual(len(living_persons), 1)
        self.assertIn(self.person1, living_persons)
        self.assertNotIn(self.person3, living_persons)
        
    def test_cleanup_dead_persons(self):
        """Test cleanup of dead persons."""
        self.manager.add_person(self.person1)
        self.manager.add_person(self.person3)  # This person is dead
        # Force person3 to be dead by setting their health to 0
        self.person3.health = 0
        self.manager.cleanup_dead_persons(self.current_year)
        all_persons = self.manager.get_all_persons()
        self.assertEqual(len(all_persons), 1)
        self.assertIn(self.person1, all_persons)
        self.assertNotIn(self.person3, all_persons)
        
    def test_get_persons_by_faction(self):
        """Test retrieving persons by faction."""
        self.manager.add_person(self.person1)
        self.manager.add_person(self.person2)
        noble_persons = self.manager.get_persons_by_faction("Noble Houses")
        self.assertEqual(len(noble_persons), 1)
        self.assertIn(self.person1, noble_persons)
        
    def test_get_persons_by_region(self):
        """Test retrieving persons by region."""
        self.manager.add_person(self.person1)
        self.manager.add_person(self.person2)
        central_valley_persons = self.manager.get_persons_by_region("Central Valley")
        self.assertEqual(len(central_valley_persons), 1)
        self.assertIn(self.person1, central_valley_persons)
        
    def test_duplicate_person_handling(self):
        """Test handling of duplicate person additions."""
        self.manager.add_person(self.person1)
        self.manager.add_person(self.person1)  # Try to add the same person again
        all_persons = self.manager.get_all_persons()
        self.assertEqual(len(all_persons), 1)  # Should still only have one instance
        
    def test_remove_nonexistent_person(self):
        """Test removing a person that doesn't exist in the manager."""
        self.manager.remove_person(self.person1)  # Try to remove a person that was never added
        all_persons = self.manager.get_all_persons()
        self.assertEqual(len(all_persons), 0)  # Should still be empty 