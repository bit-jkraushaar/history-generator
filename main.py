import argparse
from simulation import Simulation
from events import DeathEvent, MarriageEvent, BirthEvent, SuccessionEvent, NoSuccessorEvent
from fantasy_events import NaturalEvent, MagicalEvent, PoliticalEvent
import random

def parse_arguments():
    parser = argparse.ArgumentParser(description='Run a dynasty simulation')
    parser.add_argument('--start-year', type=int, default=1000, help='Starting year of the simulation')
    parser.add_argument('--duration', type=int, default=50, help='Duration of the simulation in years')
    
    # Event display options
    parser.add_argument('--show-deaths', action='store_true', help='Display death events')
    parser.add_argument('--show-marriages', action='store_true', help='Display marriage events')
    parser.add_argument('--show-births', action='store_true', help='Display birth events')
    parser.add_argument('--show-successions', action='store_true', help='Display succession events')
    parser.add_argument('--show-natural', action='store_true', help='Display natural events')
    parser.add_argument('--show-magical', action='store_true', help='Display magical events')
    parser.add_argument('--show-political', action='store_true', help='Display political events')
    parser.add_argument('--show-family-tree', action='store_true', help='Display family tree at the end')
    parser.add_argument('--show-all', action='store_true', help='Display all events and family tree')
    parser.add_argument('--show-fantasy', action='store_true', help='Display only fantasy events (natural, magical, political)')
    
    return parser.parse_args()

def should_show_event(event, args):
    if args.show_all:
        return True
    
    if args.show_fantasy:
        return isinstance(event, (NaturalEvent, MagicalEvent, PoliticalEvent))
    
    if isinstance(event, DeathEvent) and args.show_deaths:
        return True
    if isinstance(event, MarriageEvent) and args.show_marriages:
        return True
    if isinstance(event, BirthEvent) and args.show_births:
        return True
    if isinstance(event, (SuccessionEvent, NoSuccessorEvent)) and args.show_successions:
        return True
    if isinstance(event, NaturalEvent) and args.show_natural:
        return True
    if isinstance(event, MagicalEvent) and args.show_magical:
        return True
    if isinstance(event, PoliticalEvent) and args.show_political:
        return True
    
    return False

def main():
    args = parse_arguments()
    
    # Create simulation
    sim = Simulation(start_year=args.start_year, duration=args.duration)
    
    # Create initial dynasty
    sim.create_dynasty("House Nerdival")
    
    # Run simulation with filtered events
    while sim.year < sim.end_year:
        events = sim.simulate_year()
        visible_events = [event for event in events if should_show_event(event, args)]
        
        if visible_events:
            print(f"\n🗓 Year {sim.year}")
            for event in visible_events:
                if isinstance(event, (NaturalEvent, MagicalEvent, PoliticalEvent)):
                    print(f"  - {event}")
                    if event.effects:
                        print("    Effects:")
                        for effect in event.effects:
                            if effect['type'] == 'modify_stat':
                                if 'faction' in effect:
                                    print(f"      {effect['faction']}: {effect['stat']} {effect['value']:+d}")
                                elif 'region' in effect:
                                    print(f"      {effect['region']}: {effect['stat']} {effect['value']:+d}")
                else:
                    print(f"  {event.message}")
        
        sim.increment_year()
    
    # Show family tree if requested
    if args.show_family_tree or args.show_all:
        print("\n🌳 Family Tree:")
        sim.debug_print()

if __name__ == "__main__":
    #random.seed(42)
    main()
