from dataclasses import dataclass

@dataclass
class Calendar:
    name: str
    id: str
    is_program: bool

all_calendars = [
            Calendar(name="FACET-PAMM",  id="r0210ceqt2k11gs8g3e1q09sok@group.calendar.google.com", is_program=True),
            Calendar(name="FACET-MD", id="facet.ii.schedule@gmail.com", is_program=True),
            Calendar(name="FACET-USER", id="08t3idt93iijso2nlfrbn0bi24@group.calendar.google.com", is_program=True)
            ]