from person import Person
from marriage_market import MarriageMarket

class Dynasty:
    def __init__(self, name: str, king: Person, queen: Person):
        self.name = name
        self.founding_king = king
        self.founding_queen = queen
        self.king = king
        self.queen = queen
        self.king.was_king = True
        self.queen.was_king = True
        self.family = [king, queen]

    def simulate_year(self, year: int, marriage_market: MarriageMarket):
        for person in self.family[:]:
            person.age_up(year, marriage_market)
            if person.is_dead(year):
                self.family.remove(person)
                if person == self.king:
                    self._replace_monarch(year, is_king=True)
                elif person == self.queen:
                    self._replace_monarch(year, is_king=False)
            else:
                person.give_birth(year)

        for person in self.family:
            for child in person.children:
                if child not in self.family and not child.is_dead(year):
                    self.family.append(child)

    def _replace_monarch(self, year, is_king: bool):
        parent = self.king if is_king else self.queen
        suitable_children = [k for k in parent.children if not k.is_dead(year) and k.age >= 18]
        if suitable_children:
            successor = max(suitable_children, key=lambda k: k.age)
            if is_king:
                self.king = successor
            else:
                self.queen = successor
            successor.was_king = True
        else:
            print(f"The {'Queen' if not is_king else 'King'} has died, but there is no suitable successor.")

    def show_family_tree(self):
        print(f"\nFamily tree of the {self.name} dynasty:")
        self._show_family_tree(self.founding_king, 0)

    def _show_family_tree(self, person, level):
        status = "†" if person.dead else "alive"
        crown = "👑 " if person.was_king else ""
        symbol = "├──" if level > 0 else ""
        year_info = f"{person.birth_year}–{person.death_year}" if person.death_year else f"born {person.birth_year}"
        output = "  " * level + f"{symbol}{crown}{person.name} ({status}, {year_info})"
        if person.partner_list:
            partner_infos = [f"{p.name} ({'†' if p.dead else 'alive'}, born {p.birth_year})" for p in person.partner_list]
            output += " ⚭ " + ", ".join(partner_infos)
        print(output)
        shown_children = set()
        for child in person.children:
            if child not in shown_children:
                self._show_family_tree(child, level + 1)
                shown_children.add(child)
