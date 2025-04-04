import random

male_names = [
    "Baelor", "Draven", "Falathar", "Hadrian", "Jareth", "Lysander", "Nyx", "Oberon",
    "Quintus", "Thorian", "Valerian", "Xander", "Aric", "Caspian", "Finnian", "Haelen",
    "Jorvik", "Kael", "Maelor", "Orion", "Raffael", "Tiberius", "Zaltar", "Aegon",
    "Balin", "Corvus", "Darius", "Eldrin", "Fenris", "Gideon", "Hektor", "Ignis",
    "Jarik", "Kaelan", "Lorien", "Marius", "Nereus", "Osric", "Phelan", "Ragnar",
    "Silas", "Talon", "Ulric", "Viggo", "Wulfric", "Xylon", "Yorath", "Zephyr"
]
female_names = [
    "Aeliana", "Caelia", "Elyndra", "Gwendolyn", "Isolde", "Kyra", "Myranda", "Phiala",
    "Rhiannon", "Seraphina", "Ursula", "Wynter", "Ylva", "Zephyra", "Brynn", "Dahlia",
    "Elowen", "Giselle", "Ilaria", "Lyra", "Niamh", "Primrose", "Saoirse", "Ulani",
    "Vespera", "Wren", "Xylia", "Yvaine", "Anya", "Brynja", "Calista", "Demetra",
    "Eira", "Fiona", "Gwyneira", "Hestia", "Iona", "Juno", "Kassandra", "Lilith",
    "Morgana", "Nixie", "Ophelia", "Pandora", "Ravenna", "Selene", "Titania", "Valencia",
    "Winifred", "Xanthe", "Yara", "Zelda"
]

all_persons = []

class Person:
    def __init__(self, name, age, health, gender, birth_year=0):
        self.name = name
        self.age = age
        self.health = health
        self.gender = gender
        self.partner = None
        self.partner_list = []
        self.children = []
        self.dead = False
        self.was_king = False
        self.marriage_age = random.randint(18, 30)
        self.birth_year = birth_year
        self.death_year = None
        all_persons.append(self)

    def age_up(self, year, marriage_market=None):
        self.age += 1
        self.health -= random.randint(0, 5)

        if self.age >= 18 and not self.partner and marriage_market:
            chance = min(0.1 + (self.age - 18) * 0.05, 0.9)
            if random.random() < chance:
                partner = marriage_market.find_partner(self)
                if partner:
                    print(f"{self.name} marries {partner.name} at the age of {self.age} years")
                    self.marry(partner)
                    marriage_market.remove(partner)
                else:
                    print(f"{self.name} would have liked to marry, but there was no suitable partner on the marriage market.")

    def is_dead(self, year):
        if self.dead:
            return True
        if self.health <= 0 or self.age > 80 + random.randint(0, 40):
            self.dead = True
            self.death_year = year
            return True
        return False

    def marry(self, partner):
        self.partner = partner
        partner.partner = self
        self.partner_list.append(partner)
        partner.partner_list.append(self)

    def give_birth(self, year):
        if self.gender == "female" and self.partner and 16 < self.age < 45:
            if random.random() < 0.3:
                gender = "male" if random.random() < 0.5 else "female"
                name = random.choice(male_names) if gender == "male" else random.choice(female_names)
                child = Person(name, 0, 100, gender, birth_year=year)
                self.children.append(child)
                self.partner.children.append(child)

def generate_partner(gender, year):
    name = random.choice(male_names) if gender == "male" else random.choice(female_names)
    age = random.randint(18, 40)
    return Person(name, age, 100, gender, birth_year=year - age)


class MarriageCandidate:
    def __init__(self, person, remaining_years):
        self.person = person
        self.remaining_years = remaining_years