from simulation import Simulation
import random

if __name__ == "__main__":
    random.seed(42)
    sim = Simulation(startjahr=1000, dauer=50)
    sim.dynastie_erzeugen("Haus Nerdival")
    sim.simuliere()
