from simulation import Simulation
import random
import argparse
from events import DeathEvent, MarriageEvent, BirthEvent, SuccessionEvent, NoSuccessorEvent

def parse_arguments():
    parser = argparse.ArgumentParser(description='Run a dynasty simulation')
    parser.add_argument('--start-year', type=int, default=1000, help='Starting year of the simulation')
    parser.add_argument('--duration', type=int, default=50, help='Duration of the simulation in years')
    parser.add_argument('--show-deaths', action='store_true', help='Show death events')
    parser.add_argument('--show-marriages', action='store_true', help='Show marriage events')
    parser.add_argument('--show-births', action='store_true', help='Show birth events')
    parser.add_argument('--show-successions', action='store_true', help='Show succession events')
    parser.add_argument('--show-family-tree', action='store_true', help='Show family tree at the end')
    parser.add_argument('--show-all', action='store_true', help='Show all events and family tree')
    return parser.parse_args()

def should_show_event(event, args):
    if args.show_all:
        return True
    if isinstance(event, DeathEvent) and args.show_deaths:
        return True
    if isinstance(event, MarriageEvent) and args.show_marriages:
        return True
    if isinstance(event, BirthEvent) and args.show_births:
        return True
    if isinstance(event, (SuccessionEvent, NoSuccessorEvent)) and args.show_successions:
        return True
    return False

if __name__ == "__main__":
    args = parse_arguments()
    random.seed(42)
    sim = Simulation(start_year=args.start_year, duration=args.duration)
    sim.create_dynasty("House Nerdival")
    
    # Run simulation with filtered events
    while sim.year < sim.end_year:
        events = sim.simulate_year()
        visible_events = [event for event in events if should_show_event(event, args)]
        if visible_events:
            print(f"\n🗓 Year {sim.year}")
            for event in visible_events:
                print(f"  {event.message}")
        sim.year += 1

    # Show family tree if requested
    if args.show_family_tree or args.show_all:
        sim.debug_print()
