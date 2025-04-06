from .person import Person
from .marriage_market import MarriageMarket
from .events import SuccessionEvent, NoSuccessorEvent, DeathEvent, MarriageEvent

class Dynasty:
    def __init__(self, name: str, king: Person, queen: Person):
        self.name = name
        self.founding_king = king
        self.founding_queen = queen
        self.monarch = king  # Only one monarch
        self.monarch.was_king = True
        self.family = [king, queen]

    def simulate_year(self, year: int, marriage_market: MarriageMarket):
        events = []
        for person in self.family[:]:
            # Age up and check for death and marriage
            age_event = person.age_up(year, marriage_market)
            if isinstance(age_event, DeathEvent):
                events.append(age_event)
                self.family.remove(person)
                if person == self.monarch:
                    succession_event = self._replace_monarch(year)
                    if succession_event:
                        events.append(succession_event)
            elif isinstance(age_event, MarriageEvent):
                events.append(age_event)
            else:
                # Check for birth
                birth_event = person.give_birth(year)
                if birth_event:
                    events.append(birth_event)

        # Add new children to family
        for person in self.family:
            for child in person.children:
                if child not in self.family and not child.is_dead(year):
                    self.family.append(child)

        return events

    def _find_successor(self, parent, year):
        # First try to find a suitable child
        suitable_children = [k for k in parent.children if not k.is_dead(year) and k.age >= 18]
        if suitable_children:
            return max(suitable_children, key=lambda k: k.age)

        # If no suitable child, try to find a sibling
        # Get all siblings by looking at the children of the parents
        siblings = []
        if parent.parents:
            mother, father = parent.parents
            # Get all children of the parents that are not the monarch
            siblings.extend([c for c in mother.children 
                           if c != parent and not c.is_dead(year) and c.age >= 18])
            siblings.extend([c for c in father.children 
                           if c != parent and not c.is_dead(year) and c.age >= 18])
        
        if siblings:
            return max(siblings, key=lambda s: s.age)
        
        return None

    def _replace_monarch(self, year):
        successor = self._find_successor(self.monarch, year)
        
        if successor:
            old_monarch = self.monarch
            self.monarch = successor
            successor.was_king = True
                       
            relationship = "child" if successor in old_monarch.children else "sibling"
            return SuccessionEvent(
                year=year,
                message=f"{successor.name} ({relationship}) succeeds {old_monarch.name} as Monarch",
                old_monarch=old_monarch.name,
                new_monarch=successor.name,
                is_king=successor.gender == "male"
            )
        else:
            return NoSuccessorEvent(
                year=year,
                message=f"The Monarch has died, but there is no suitable successor.",
                monarch_name=self.monarch.name,
                is_king=self.monarch.gender == "male"
            )

    def show_family_tree(self):
        print(f"\nFamily tree of the {self.name} dynasty:")
        self._show_family_tree(self.founding_king, 0)

    def _show_family_tree(self, person, level):
        status = "†" if person.dead else "alive"
        crown = "👑 " if person.was_king else ""
        gender = "♂ " if person.gender == "male" else "♀ "
        symbol = "├──" if level > 0 else ""
        year_info = f"{person.birth_year}–{person.death_year}" if person.death_year else f"born {person.birth_year}"
        output = "  " * level + f"{symbol}{crown}{gender}{person.name} ({status}, {year_info})"
        if person.partner_list:
            partner_infos = []
            for p in person.partner_list:
                p_gender = "♂ " if p.gender == "male" else "♀ "
                p_status = "†" if p.dead else "alive"
                p_year_info = f"{p.birth_year}–{p.death_year}" if p.death_year else f"born {p.birth_year}"
                partner_infos.append(f"{p_gender}{p.name} ({p_status}, {p_year_info})")
            output += " ⚭ " + ", ".join(partner_infos)
        print(output)
        shown_children = set()
        for child in person.children:
            if child not in shown_children:
                self._show_family_tree(child, level + 1)
                shown_children.add(child)
