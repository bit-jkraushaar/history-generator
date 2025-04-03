from person import Person, generiere_partner,maennliche_namen,weibliche_namen
from heiratsmarkt import Heiratsmarkt
from dynastie import Dynastie
import random

class Simulation:
    def __init__(self, startjahr=1000, dauer=50):
        self.jahr = startjahr
        self.endjahr = startjahr + dauer
        self.dynastien = []
        self.heiratsmarkt = Heiratsmarkt()

    def dynastie_erzeugen(self, name: str):
        # zufälliges Alter für König & Königin
        alter_koenig = random.randint(20, 40)
        alter_koenigin = random.randint(20, 40)
        geburtsjahr = self.jahr - alter_koenig

        koenig = Person(random.choice(maennliche_namen), alter_koenig, 100, "maennlich", geburtsjahr)
        koenigin = Person(random.choice(weibliche_namen), alter_koenigin, 100, "weiblich", geburtsjahr)
        koenig.heiraten(koenigin)

        dynastie = Dynastie(name, koenig, koenigin)
        print(f"{koenig.name} ist verheiratet mit {koenig.partner.name if koenig.partner else 'niemandem'}")
        self.dynastien.append(dynastie)

    def simuliere(self):
        while self.jahr < self.endjahr:
            print(f"\n🗓 Jahr {self.jahr}")
            self.heiratsmarkt.aktualisieren(self.jahr)
            for dynastie in self.dynastien:
                dynastie.simuliere_jahr(self.jahr, self.heiratsmarkt)
            self.jahr += 1

        for dynastie in self.dynastien:
            dynastie.zeige_stammbaum()
