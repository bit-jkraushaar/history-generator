import random
from person import generiere_partner, Heiratskandidat  # ggf. Heiratskandidat separat definieren

class Heiratsmarkt:
    def __init__(self):
        self.kandidaten = []

    def aktualisieren(self, jahr):
        for kandidat in self.kandidaten:
            kandidat.verbleibende_jahre -= 1

        # Entferne nicht mehr verfügbare Kandidaten
        self.kandidaten = [
            k for k in self.kandidaten
            if k.verbleibende_jahre > 0 and not k.person.tot and not k.person.partner
        ]

        # Füge neue zufällige Kandidaten hinzu
        for _ in range(random.randint(2, 5)):
            geschlecht = random.choice(["maennlich", "weiblich"])
            neuer = generiere_partner(geschlecht, jahr)
            dauer = random.randint(1, 5)
            self.kandidaten.append(Heiratskandidat(neuer, dauer))

    def suche_partner(self, person):
        for kandidat in self.kandidaten:
            p = kandidat.person
            if (
                p.geschlecht != person.geschlecht and
                not p.partner and
                not p.tot and
                abs(p.alter - person.alter) <= 10
            ):
                return p
        return None

    def entferne(self, person):
        self.kandidaten = [k for k in self.kandidaten if k.person != person]
