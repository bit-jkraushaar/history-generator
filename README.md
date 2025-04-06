# History Generator

A fantasy world history generator that simulates events, dynasties, and world changes over time.

## Project Structure

```
history-generator/
├── scripts/
│   └── main.py          # Main script to run the simulation
├── history_generator/
│   ├── __init__.py
│   ├── person.py        # Person class and name lists
│   ├── dynasty.py       # Dynasty class
│   ├── marriage_market.py
│   ├── events.py        # Basic event classes
│   ├── fantasy_events.py # Fantasy event classes
│   ├── fantasy_world.py # Fantasy world state
│   ├── event_processor.py # Event processing logic
│   └── logger_config.py # Logging configuration
├── data/
│   └── event_definitions.json # Event definitions
├── docs/
│   └── event_system.md  # Documentation of the event system
├── tests/
│   ├── __init__.py
│   ├── test_events.py   # Tests for basic events
│   ├── test_fantasy_events.py # Tests for fantasy events
│   └── test_event_processor.py # Tests for event processing
└── README.md
```

## Running the Simulation

Basic parameters:
- `--start-year <year>`: Set the starting year (default: 1000)
- `--duration <years>`: Set the simulation duration in years (default: 50)

Event display options:
- `--show-deaths`: Show death events
- `--show-marriages`: Show marriage events
- `--show-births`: Show birth events
- `--show-successions`: Show succession events
- `--show-natural`: Show natural events
- `--show-magical`: Show magical events
- `--show-political`: Show political events
- `--show-fantasy`: Show all fantasy events
- `--show-family-tree`: Show the family tree
- `--show-all`: Show all events

### Examples

Run the simulation with default settings:
```bash
python scripts/main.py
```

Show only fantasy events:
```bash
python scripts/main.py --show-fantasy
```

Show the family tree:
```bash
python scripts/main.py --show-family-tree
```

Run a longer simulation:
```bash
python scripts/main.py --duration 100
```

## Testing

The project includes unit tests for various components. To run the tests:

### Running All Tests

```bash
python -m unittest discover tests
```

### Running Specific Test Files

```bash
# Test basic events
python -m unittest tests/test_events.py -v

# Test fantasy events
python -m unittest tests/test_fantasy_events.py -v

# Test event processor
python -m unittest tests/test_event_processor.py -v
```

### Test Coverage

The tests cover the following components:

1. **Basic Events** (`test_events.py`):
   - Event initialization
   - Marriage events
   - Birth events
   - Death events
   - Succession events

2. **Fantasy Events** (`test_fantasy_events.py`):
   - Natural events
   - Magical events
   - Political events
   - Event effects
   - Fantasy event generator

3. **Event Processor** (`test_event_processor.py`):
   - Condition evaluation
   - Effect application
   - Event triggering
   - Stat bounds checking
   - Common conditions

### Adding New Tests

When adding new features, please include corresponding tests. Follow these guidelines:

1. Create a new test file in the `tests` directory if needed
2. Use descriptive test method names
3. Include docstrings explaining what each test covers
4. Test both success and failure cases
5. Use mock objects for external dependencies

## Event System Documentation

For detailed information about the event system, see [docs/event_system.md](docs/event_system.md).
