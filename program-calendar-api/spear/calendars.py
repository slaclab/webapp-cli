from dataclasses import dataclass

@dataclass
class Calendar:
    name: str
    id: str
    is_program: bool

all_calendars = [
            Calendar(name="SPEAR-AP",  id="a55ffdddc34da99930883c06710f410efa91789733aacbc2723661c7d5441ed4@group.calendar.google.com", is_program=True),
            Calendar(name="SPEAR-USER", id="276e580a982a8bd4ba3d1d5c1a1d59dbcb65e417e5cba0fbfb8e775135314330@group.calendar.google.com", is_program=True),
            Calendar(name="SPEAR-MAINT", id="253070b736d89c88a5cd351cb2b35007b92a73cf546154bcde72ef1ff10b6faa@group.calendar.google.com", is_program=True)
            ]