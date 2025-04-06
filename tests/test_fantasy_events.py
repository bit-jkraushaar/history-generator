import unittest
from unittest.mock import MagicMock
from history_generator.fantasy_events import NaturalEvent, MagicalEvent, PoliticalEvent, FantasyEventGenerator
from history_generator.fantasy_world import FantasyWorld

class TestFantasyEvents(unittest.TestCase):
    def test_natural_event(self):
        """Test the NaturalEvent class"""
        event_data = {
            'name': 'Earthquake',
            'description': 'A powerful earthquake shakes the land',
            'category': 'natural',
            'effects': [
                {
                    'type': 'modify_stat',
                    'region': 'Southern Plains',
                    'stat': 'fertility',
                    'value': -20
                },
                {
                    'type': 'modify_stat',
                    'region': 'Southern Plains',
                    'stat': 'magical_energy',
                    'value': 15
                }
            ]
        }
        event = NaturalEvent(year=1000, event_data=event_data)
        
        self.assertEqual(event.year, 1000)
        self.assertEqual(event.name, 'Earthquake')
        self.assertEqual(event.event_data['description'], 'A powerful earthquake shakes the land')
        self.assertEqual(len(event.effects), 2)
        self.assertEqual(event.effects[0]['region'], 'Southern Plains')
        self.assertEqual(event.effects[0]['stat'], 'fertility')
        self.assertEqual(event.effects[0]['value'], -20)
        self.assertEqual(event.effects[1]['region'], 'Southern Plains')
        self.assertEqual(event.effects[1]['stat'], 'magical_energy')
        self.assertEqual(event.effects[1]['value'], 15)

    def test_magical_event(self):
        """Test the MagicalEvent class"""
        event_data = {
            'name': 'Mana Surge',
            'description': 'A surge of magical energy affects the region',
            'category': 'magical',
            'effects': [
                {
                    'type': 'modify_stat',
                    'faction': 'Mages\' Guild',
                    'stat': 'power',
                    'value': 15
                },
                {
                    'type': 'modify_stat',
                    'faction': 'Mages\' Guild',
                    'stat': 'stability',
                    'value': -10
                }
            ]
        }
        event = MagicalEvent(year=1000, event_data=event_data)
        
        self.assertEqual(event.year, 1000)
        self.assertEqual(event.name, 'Mana Surge')
        self.assertEqual(event.event_data['description'], 'A surge of magical energy affects the region')
        self.assertEqual(len(event.effects), 2)
        self.assertEqual(event.effects[0]['faction'], 'Mages\' Guild')
        self.assertEqual(event.effects[0]['stat'], 'power')
        self.assertEqual(event.effects[0]['value'], 15)
        self.assertEqual(event.effects[1]['faction'], 'Mages\' Guild')
        self.assertEqual(event.effects[1]['stat'], 'stability')
        self.assertEqual(event.effects[1]['value'], -10)

    def test_political_event(self):
        """Test the PoliticalEvent class"""
        event_data = {
            'name': 'Temple Crusade',
            'description': 'The Temple of Light launches a crusade',
            'category': 'political',
            'effects': [
                {
                    'type': 'modify_stat',
                    'faction': 'Temple of Light',
                    'stat': 'power',
                    'value': 20
                },
                {
                    'type': 'modify_stat',
                    'faction': 'Dark Brotherhood',
                    'stat': 'stability',
                    'value': -15
                }
            ]
        }
        event = PoliticalEvent(year=1000, event_data=event_data)
        
        self.assertEqual(event.year, 1000)
        self.assertEqual(event.name, 'Temple Crusade')
        self.assertEqual(event.event_data['description'], 'The Temple of Light launches a crusade')
        self.assertEqual(len(event.effects), 2)
        self.assertEqual(event.effects[0]['faction'], 'Temple of Light')
        self.assertEqual(event.effects[0]['stat'], 'power')
        self.assertEqual(event.effects[0]['value'], 20)
        self.assertEqual(event.effects[1]['faction'], 'Dark Brotherhood')
        self.assertEqual(event.effects[1]['stat'], 'stability')
        self.assertEqual(event.effects[1]['value'], -15)

    def test_event_str_representation(self):
        """Test the string representation of events"""
        event_data = {
            'name': 'Test Event',
            'description': 'A test event',
            'category': 'natural',
            'effects': []
        }
        
        natural_event = NaturalEvent(year=1000, event_data=event_data)
        event_data['category'] = 'magical'
        magical_event = MagicalEvent(year=1000, event_data=event_data)
        event_data['category'] = 'political'
        political_event = PoliticalEvent(year=1000, event_data=event_data)
        
        self.assertEqual(str(natural_event), "Test Event (natural)")
        self.assertEqual(str(magical_event), "Test Event (magical)")
        self.assertEqual(str(political_event), "Test Event (political)")

    def test_fantasy_event_generator(self):
        """Test the FantasyEventGenerator class"""
        # Create a mock FantasyWorld
        mock_world = MagicMock(spec=FantasyWorld)
        
        # Set up the mock to return specific events
        mock_world.generate_events.return_value = [
            {
                'name': 'Earthquake',
                'description': 'A powerful earthquake',
                'category': 'natural',
                'effects': [
                    {
                        'type': 'modify_stat',
                        'region': 'Southern Plains',
                        'stat': 'fertility',
                        'value': -20
                    }
                ]
            },
            {
                'name': 'Mana Surge',
                'category': 'magical',
                'effects': [
                    {
                        'type': 'modify_stat',
                        'faction': 'Mages\' Guild',
                        'stat': 'power',
                        'value': 15
                    }
                ]
            },
            {
                'name': 'Political Alliance',
                'category': 'political',
                'effects': [
                    {
                        'type': 'modify_stat',
                        'faction': 'Noble Houses',
                        'stat': 'influence',
                        'value': 10
                    }
                ]
            }
        ]
        
        # Initialize regions and factions for effect application
        mock_world.regions = {
            'Southern Plains': {
                'fertility': 70
            }
        }
        mock_world.factions = {
            'Mages\' Guild': {
                'power': 60
            },
            'Noble Houses': {
                'influence': 70
            }
        }
        
        # Create generator with mock world
        generator = FantasyEventGenerator(mock_world)
        
        # Generate events for year 1000
        events = generator.generate_events(1000)
        
        # Verify that the world's year was set
        self.assertEqual(mock_world.year, 1000)
        
        # Verify that generate_events was called
        mock_world.generate_events.assert_called_once()
        
        # Check that we got the right number of events
        self.assertEqual(len(events), 3)
        
        # Check that events are of the correct types
        self.assertIsInstance(events[0], NaturalEvent)
        self.assertIsInstance(events[1], MagicalEvent)
        self.assertIsInstance(events[2], PoliticalEvent)
        
        # Verify that effects were applied
        self.assertEqual(mock_world.regions['Southern Plains']['fertility'], 50)  # 70 - 20
        self.assertEqual(mock_world.factions['Mages\' Guild']['power'], 75)  # 60 + 15
        self.assertEqual(mock_world.factions['Noble Houses']['influence'], 80)  # 70 + 10

    def test_fantasy_event_generator_invalid_category(self):
        """Test the FantasyEventGenerator with invalid event category"""
        mock_world = MagicMock(spec=FantasyWorld)
        mock_world.generate_events.return_value = [
            {
                'name': 'Invalid Event',
                'category': 'invalid',
                'effects': []
            }
        ]
        
        generator = FantasyEventGenerator(mock_world)
        events = generator.generate_events(1000)
        
        # Check that invalid category events are ignored
        self.assertEqual(len(events), 0)

    def test_fantasy_event_generator_missing_category(self):
        """Test the FantasyEventGenerator with missing event category"""
        mock_world = MagicMock(spec=FantasyWorld)
        mock_world.generate_events.return_value = [
            {
                'name': 'Missing Category Event',
                'effects': []
            }
        ]
        
        generator = FantasyEventGenerator(mock_world)
        events = generator.generate_events(1000)
        
        # Check that events without category are ignored
        self.assertEqual(len(events), 0)

if __name__ == '__main__':
    unittest.main() 