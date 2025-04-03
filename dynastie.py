from person import Person
from heiratsmarkt import Heiratsmarkt

class Dynastie:
    def __init__(self, name: str, koenig: Person, koenigin: Person):
        self.name = name
        self.gruender_koenig = koenig
        self.gruender_koenigin = koenigin
        self.koenig = koenig
        self.koenigin = koenigin
        self.koenig.war_koenig = True
        self.koenigin.war_koenig = True
        self.familie = [koenig, koenigin]

    def simuliere_jahr(self, jahr: int, heiratsmarkt: Heiratsmarkt):
        for person in self.familie[:]:
            person.altern(jahr, heiratsmarkt)
            if person.ist_tot(jahr):
                self.familie.remove(person)
                if person == self.koenig:
                    self._ersetze_monarch(jahr, is_koenig=True)
                elif person == self.koenigin:
                    self._ersetze_monarch(jahr, is_koenig=False)
            else:
                person.gebaeren(jahr)

        for person in self.familie:
            for kind in person.kinder:
                if kind not in self.familie and not kind.ist_tot(jahr):
                    self.familie.append(kind)

    def _ersetze_monarch(self, jahr, is_koenig: bool):
        elternteil = self.koenig if is_koenig else self.koenigin
        geeignete_kinder = [k for k in elternteil.kinder if not k.ist_tot(jahr) and k.alter >= 18]
        if geeignete_kinder:
            nachfolger = max(geeignete_kinder, key=lambda k: k.alter)
            if is_koenig:
                self.koenig = nachfolger
            else:
                self.koenigin = nachfolger
            nachfolger.war_koenig = True
        else:
            print(f"Die {'Königin' if not is_koenig else 'König'} ist gestorben, aber es gibt keinen geeigneten Nachfolger.")

    def zeige_stammbaum(self):
        print(f"\nStammbaum der Dynastie {self.name}:")
        self._zeige_stammbaum(self.gruender_koenig, 0)

    def _zeige_stammbaum(self, person, ebene):
        status = "†" if person.tot else "lebt"
        krone = "👑 " if person.war_koenig else ""
        zeichen = "├──" if ebene > 0 else ""
        jahresinfo = f"{person.geburtsjahr}–{person.sterbejahr}" if person.sterbejahr else f"geb. {person.geburtsjahr}"
        ausgabe = "  " * ebene + f"{zeichen}{krone}{person.name} ({status}, {jahresinfo})"
        if person.partnerliste:
            partner_infos = [f"{p.name} ({'†' if p.tot else 'lebt'}, geb. {p.geburtsjahr})" for p in person.partnerliste]
            ausgabe += " ⚭ " + ", ".join(partner_infos)
        print(ausgabe)
        gezeigte_kinder = set()
        for kind in person.kinder:
            if kind not in gezeigte_kinder:
                self._zeige_stammbaum(kind, ebene + 1)
                gezeigte_kinder.add(kind)
