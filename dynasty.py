from person import Person
from marriage_market import MarriageMarket
from events import SuccessionEvent, NoSuccessorEvent

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
        events = []
        for person in self.family[:]:
            # Age up and check for marriage
            marriage_event = person.age_up(year, marriage_market)
            if marriage_event:
                events.append(marriage_event)

            # Check for death
            death_event = person.is_dead(year)
            if death_event:
                events.append(death_event)
                self.family.remove(person)
                if person == self.king:
                    succession_event = self._replace_monarch(year, is_king=True)
                    if succession_event:
                        events.append(succession_event)
                elif person == self.queen:
                    succession_event = self._replace_monarch(year, is_king=False)
                    if succession_event:
                        events.append(succession_event)
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

    def _find_successor(self, parent, year, is_king: bool):
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

    def _replace_monarch(self, year, is_king: bool):
        parent = self.king if is_king else self.queen
        successor = self._find_successor(parent, year, is_king)
        
        if successor:
            old_monarch = self.king if is_king else self.queen
            if is_king:
                self.king = successor
            else:
                self.queen = successor
            successor.was_king = True
            
            relationship = "child" if successor in parent.children else "sibling"
            return SuccessionEvent(
                year=year,
                message=f"{successor.name} ({relationship}) succeeds {old_monarch.name} as {'King' if is_king else 'Queen'}",
                old_monarch=old_monarch.name,
                new_monarch=successor.name,
                is_king=is_king
            )
        else:
            return NoSuccessorEvent(
                year=year,
                message=f"The {'Queen' if not is_king else 'King'} has died, but there is no suitable successor.",
                monarch_name=parent.name,
                is_king=is_king
            )

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
