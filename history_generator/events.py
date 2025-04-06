from dataclasses import dataclass

@dataclass
class Event:
    year: int
    message: str

@dataclass
class MarriageEvent(Event):
    person1: str
    person2: str
    age: int

@dataclass
class BirthEvent(Event):
    child_name: str
    mother_name: str
    father_name: str

@dataclass
class DeathEvent(Event):
    person_name: str
    age: int

@dataclass
class SuccessionEvent(Event):
    old_monarch: str
    new_monarch: str
    is_king: bool

@dataclass
class NoSuccessorEvent(Event):
    monarch_name: str
    is_king: bool 