import unittest
import json
from unittest.mock import mock_open, patch
from history_generator.event_processor import EventProcessor, ConditionType, EffectType

class TestEventProcessor(unittest.TestCase):
    def setUp(self):
        # Mock event definitions
        self.event_data = {
            "events": {
                "natural": {
                    "earthquake": {
                        "name": "Earthquake",
                        "description": "A powerful earthquake",
                        "conditions": [
                            {
                                "type": "region",
                                "region": "Southern Plains",
                                "stat": "magical_energy",
                                "operator": ">=",
                                "value": 50
                            }
                        ],
                        "effects": [
                            {
                                "type": "modify_stat",
                                "region": "Southern Plains",
                                "stat": "fertility",
                                "value": -20
                            }
                        ]
                    }
                },
                "magical": {
                    "mana_surge": {
                        "name": "Mana Surge",
                        "description": "A magical surge",
                        "conditions": [
                            {
                                "type": "common",
                                "value": "magical_instability"
                            }
                        ],
                        "effects": [
                            {
                                "type": "modify_stat",
                                "faction": "Mages' Guild",
                                "stat": "power",
                                "value": 15
                            }
                        ],
                        "followup_events": [
                            {
                                "id": "mana_aftermath",
                                "probability": 1.0
                            }
                        ]
                    },
                    "mana_aftermath": {
                        "name": "Mana Aftermath",
                        "description": "The aftermath of the surge",
                        "is_followup": True,
                        "effects": [
                            {
                                "type": "modify_stat",
                                "faction": "Mages' Guild",
                                "stat": "stability",
                                "value": -10
                            }
                        ]
                    }
                }
            }
        }
        
        # Create EventProcessor with mocked file
        with patch('builtins.open', mock_open(read_data=json.dumps(self.event_data))):
            self.processor = EventProcessor("mock_path.json")
            # Replace the loaded events with our test data
            self.processor.events = self.event_data

    def test_condition_evaluation_region(self):
        """Test evaluation of region-based conditions"""
        world_state = {
            "current_year": 1000,
            "regions": {
                "Southern Plains": {
                    "magical_energy": 60,
                    "fertility": 70
                }
            }
        }
        
        condition = {
            "type": "region",
            "region": "Southern Plains",
            "stat": "magical_energy",
            "operator": ">=",
            "value": 50
        }
        
        self.assertTrue(self.processor._evaluate_condition(condition, world_state))
        
        # Test with lower value
        world_state["regions"]["Southern Plains"]["magical_energy"] = 40
        self.assertFalse(self.processor._evaluate_condition(condition, world_state))

    def test_condition_evaluation_common(self):
        """Test evaluation of common conditions"""
        world_state = {
            "regions": {
                "Central Valley": {
                    "magical_energy": 90
                }
            }
        }
        
        condition = {
            "type": "common",
            "value": "magical_instability"
        }
        
        self.assertTrue(self.processor._evaluate_condition(condition, world_state))
        
        # Test with lower value
        world_state["regions"]["Central Valley"]["magical_energy"] = 70
        self.assertFalse(self.processor._evaluate_condition(condition, world_state))

    def test_effect_application(self):
        """Test application of effects"""
        world_state = {
            "regions": {
                "Southern Plains": {
                    "fertility": 70
                }
            },
            "factions": {
                "Mages' Guild": {
                    "power": 60,
                    "stability": 70
                }
            }
        }
        
        # Test region effect
        effect = {
            "type": "modify_stat",
            "region": "Southern Plains",
            "stat": "fertility",
            "value": -20
        }
        
        self.processor._apply_effect(effect, world_state)
        self.assertEqual(world_state["regions"]["Southern Plains"]["fertility"], 50)
        
        # Test faction effect
        effect = {
            "type": "modify_stat",
            "faction": "Mages' Guild",
            "stat": "power",
            "value": 15
        }
        
        self.processor._apply_effect(effect, world_state)
        self.assertEqual(world_state["factions"]["Mages' Guild"]["power"], 75)

    def test_process_events(self):
        """Test the complete event processing"""
        world_state = {
            "current_year": 1000,
            "regions": {
                "Southern Plains": {
                    "magical_energy": 60,
                    "fertility": 70
                },
                "Central Valley": {
                    "magical_energy": 90
                }
            },
            "factions": {
                "Mages' Guild": {
                    "power": 60,
                    "stability": 70
                }
            }
        }
        
        # Process events with random seed for reproducibility
        with patch('random.choice', side_effect=lambda x: x[0]):
            triggered_events = self.processor.process_events(world_state, 1000)
        
        # We expect both the earthquake and mana surge events to trigger
        self.assertEqual(len(triggered_events), 3)  # Including followup event
        
        # Check that effects were applied
        self.assertEqual(world_state["regions"]["Southern Plains"]["fertility"], 50)
        self.assertEqual(world_state["factions"]["Mages' Guild"]["power"], 75)
        self.assertEqual(world_state["factions"]["Mages' Guild"]["stability"], 60)

    def test_stat_bounds(self):
        """Test that stats are kept within bounds (0-100)"""
        world_state = {
            "regions": {
                "Southern Plains": {
                    "fertility": 10
                }
            },
            "factions": {
                "Mages' Guild": {
                    "power": 90
                }
            }
        }
        
        # Test lower bound
        effect = {
            "type": "modify_stat",
            "region": "Southern Plains",
            "stat": "fertility",
            "value": -20
        }
        self.processor._apply_effect(effect, world_state)
        self.assertEqual(world_state["regions"]["Southern Plains"]["fertility"], 0)
        
        # Test upper bound
        effect = {
            "type": "modify_stat",
            "faction": "Mages' Guild",
            "stat": "power",
            "value": 20
        }
        self.processor._apply_effect(effect, world_state)
        self.assertEqual(world_state["factions"]["Mages' Guild"]["power"], 100)

if __name__ == '__main__':
    unittest.main() 