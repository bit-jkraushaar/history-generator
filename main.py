from simulation import Simulation
import random

if __name__ == "__main__":
    random.seed(42)
    sim = Simulation(start_year=1000, duration=50)
    sim.create_dynasty("House Nerdival")
    sim.simulate()
    sim.debug_print()
