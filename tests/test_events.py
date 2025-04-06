import unittest
from history_generator.events import Event, MarriageEvent, BirthEvent, DeathEvent, SuccessionEvent, NoSuccessorEvent

class TestEvents(unittest.TestCase):
    def test_base_event(self):
        """Test the base Event class"""
        event = Event(year=1000, message="Test event")
        self.assertEqual(event.year, 1000)
        self.assertEqual(event.message, "Test event")

    def test_marriage_event(self):
        """Test the MarriageEvent class"""
        event = MarriageEvent(
            year=1000,
            message="Test marriage",
            person1="John",
            person2="Jane",
            age=25
        )
        self.assertEqual(event.year, 1000)
        self.assertEqual(event.message, "Test marriage")
        self.assertEqual(event.person1, "John")
        self.assertEqual(event.person2, "Jane")
        self.assertEqual(event.age, 25)

    def test_birth_event(self):
        """Test the BirthEvent class"""
        event = BirthEvent(
            year=1000,
            message="Test birth",
            child_name="Baby",
            mother_name="Jane",
            father_name="John"
        )
        self.assertEqual(event.year, 1000)
        self.assertEqual(event.message, "Test birth")
        self.assertEqual(event.child_name, "Baby")
        self.assertEqual(event.mother_name, "Jane")
        self.assertEqual(event.father_name, "John")

    def test_death_event(self):
        """Test the DeathEvent class"""
        event = DeathEvent(
            year=1000,
            message="Test death",
            person_name="John",
            age=75
        )
        self.assertEqual(event.year, 1000)
        self.assertEqual(event.message, "Test death")
        self.assertEqual(event.person_name, "John")
        self.assertEqual(event.age, 75)

    def test_succession_event(self):
        """Test the SuccessionEvent class"""
        event = SuccessionEvent(
            year=1000,
            message="Test succession",
            old_monarch="John",
            new_monarch="Jane",
            is_king=True
        )
        self.assertEqual(event.year, 1000)
        self.assertEqual(event.message, "Test succession")
        self.assertEqual(event.old_monarch, "John")
        self.assertEqual(event.new_monarch, "Jane")
        self.assertTrue(event.is_king)

    def test_no_successor_event(self):
        """Test the NoSuccessorEvent class"""
        event = NoSuccessorEvent(
            year=1000,
            message="Test no successor",
            monarch_name="John",
            is_king=True
        )
        self.assertEqual(event.year, 1000)
        self.assertEqual(event.message, "Test no successor")
        self.assertEqual(event.monarch_name, "John")
        self.assertTrue(event.is_king)

if __name__ == '__main__':
    unittest.main() 