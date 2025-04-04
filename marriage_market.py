import random
from person import generate_partner, MarriageCandidate  # ggf. Heiratskandidat separat definieren

class MarriageMarket:
    def __init__(self):
        self.candidates = []

    def update(self, year):
        for candidate in self.candidates:
            candidate.remaining_years -= 1

        # Remove unavailable candidates
        self.candidates = [
            c for c in self.candidates
            if c.remaining_years > 0 and not c.person.dead and not c.person.partner
        ]

        # Add new random candidates
        for _ in range(random.randint(2, 5)):
            gender = random.choice(["male", "female"])
            new_candidate = generate_partner(gender, year)
            duration = random.randint(1, 5)
            self.candidates.append(MarriageCandidate(new_candidate, duration))

    def find_partner(self, person):
        for candidate in self.candidates:
            p = candidate.person
            if (
                p.gender != person.gender and
                not p.partner and
                not p.dead and
                abs(p.age - person.age) <= 10
            ):
                return p
        return None

    def remove(self, person):
        self.candidates = [c for c in self.candidates if c.person != person]
