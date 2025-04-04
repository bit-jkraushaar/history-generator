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
- `--show-natural`: Display natural fantasy events
- `--show-magical`: Display magical fantasy events
- `--show-political`: Display political fantasy events
- `--show-fantasy`: Display all fantasy events (natural, magical, political)
- `--show-family-tree`: Display family tree at the end
- `--show-all`: Display all events and family tree

### Examples

Show only fantasy events:
```bash
python main.py --show-fantasy
```

Show fantasy events and family tree:
```bash
python main.py --show-fantasy --show-family-tree
```

Show specific fantasy event types:
```bash
python main.py --show-natural --show-magical
```

Show dynasty events with a longer duration:
```bash
python main.py --show-deaths --show-marriages --duration 100
```

Show all events and start in a different year:
```bash
python main.py --show-all --start-year 1200
```
