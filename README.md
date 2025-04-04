# history-generator
A generator for the history of a random fantasy world, including a simulation for dynasties.

## Command Line Parameters

The simulation can be customized using the following command line parameters:

### Basic Parameters
- `--start-year <year>`: Set the starting year of the simulation (default: 1000)
- `--duration <years>`: Set the duration of the simulation in years (default: 50)

### Event Display Options
- `--show-deaths`: Display death events
- `--show-marriages`: Display marriage events
- `--show-births`: Display birth events
- `--show-successions`: Display succession events (monarch changes)
- `--show-family-tree`: Display the family tree at the end of the simulation
- `--show-all`: Display all events and the family tree

### Examples

Show only deaths and the family tree:
```bash
python main.py --show-deaths --show-family-tree
```

Show marriages and births with a longer duration:
```bash
python main.py --show-marriages --show-births --duration 100
```

Show all events and start in a different year:
```bash
python main.py --show-all --start-year 1200
```
