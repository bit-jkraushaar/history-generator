import random

maennliche_namen = [
    "Baelor", "Draven", "Falathar", "Hadrian", "Jareth", "Lysander", "Nyx", "Oberon",
    "Quintus", "Thorian", "Valerian", "Xander", "Aric", "Caspian", "Finnian", "Haelen",
    "Jorvik", "Kael", "Maelor", "Orion", "Raffael", "Tiberius", "Zaltar", "Aegon",
    "Balin", "Corvus", "Darius", "Eldrin", "Fenris", "Gideon", "Hektor", "Ignis",
    "Jarik", "Kaelan", "Lorien", "Marius", "Nereus", "Osric", "Phelan", "Ragnar",
    "Silas", "Talon", "Ulric", "Viggo", "Wulfric", "Xylon", "Yorath", "Zephyr"
]
weibliche_namen = [
    "Aeliana", "Caelia", "Elyndra", "Gwendolyn", "Isolde", "Kyra", "Myranda", "Phiala",
    "Rhiannon", "Seraphina", "Ursula", "Wynter", "Ylva", "Zephyra", "Brynn", "Dahlia",
    "Elowen", "Giselle", "Ilaria", "Lyra", "Niamh", "Primrose", "Saoirse", "Ulani",
    "Vespera", "Wren", "Xylia", "Yvaine", "Anya", "Brynja", "Calista", "Demetra",
    "Eira", "Fiona", "Gwyneira", "Hestia", "Iona", "Juno", "Kassandra", "Lilith",
    "Morgana", "Nixie", "Ophelia", "Pandora", "Ravenna", "Selene", "Titania", "Valencia",
    "Winifred", "Xanthe", "Yara", "Zelda"
]

alle_personen = []

class Person:
    def __init__(self, name, alter, gesundheit, geschlecht, geburtsjahr=0):
        self.name = name
        self.alter = alter
        self.gesundheit = gesundheit
        self.geschlecht = geschlecht
        self.partner = None
        self.partnerliste = []
        self.kinder = []
        self.tot = False
        self.war_koenig = False
        self.heiratsalter = random.randint(18, 30)
        self.geburtsjahr = geburtsjahr
        self.sterbejahr = None
        alle_personen.append(self)

    def altern(self, jahr, heiratsmarkt=None):
        self.alter += 1
        self.gesundheit -= random.randint(0, 5)

        if self.alter >= 18 and not self.partner and heiratsmarkt:
            chance = min(0.1 + (self.alter - 18) * 0.05, 0.9)
            if random.random() < chance:
                partner = heiratsmarkt.suche_partner(self)
                if partner:
                    print(f"{self.name} heiratet {partner.name} im Alter von {self.alter} Jahren")
                    self.heiraten(partner)
                    heiratsmarkt.entferne(partner)
                else:
                    print(f"{self.name} hätte gerne geheiratet, aber es gab keinen passenden Partner auf dem Heiratsmarkt.")

    def ist_tot(self, jahr):
        if self.tot:
            return True
        if self.gesundheit <= 0 or self.alter > 80 + random.randint(0, 40):
            self.tot = True
            self.sterbejahr = jahr
            return True
        return False

    def heiraten(self, partner):
        self.partner = partner
        partner.partner = self
        self.partnerliste.append(partner)
        partner.partnerliste.append(self)

    def gebaeren(self, jahr):
        if self.geschlecht == "weiblich" and self.partner and 16 < self.alter < 45:
            if random.random() < 0.3:
                geschlecht = "maennlich" if random.random() < 0.5 else "weiblich"
                name = random.choice(maennliche_namen) if geschlecht == "maennlich" else random.choice(weibliche_namen)
                kind = Person(name, 0, 100, geschlecht, geburtsjahr=jahr)
                self.kinder.append(kind)
                self.partner.kinder.append(kind)

def generiere_partner(geschlecht, jahr):
    name = random.choice(maennliche_namen) if geschlecht == "maennlich" else random.choice(weibliche_namen)
    age = random.randint(18, 40)
    return Person(name, age, 100, geschlecht, geburtsjahr=jahr - age)


class Heiratskandidat:
    def __init__(self, person, verbleibende_jahre):
        self.person = person
        self.verbleibende_jahre = verbleibende_jahre