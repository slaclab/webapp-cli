import datetime
from zoneinfo import ZoneInfo
import re
import logging
from enum import Enum
from .calendars import all_calendars
from googleapiclient.discovery import build
import google_auth_httplib2

from typing import List
from pydantic import BaseModel

from base_events import GoogleCalendarEvents

logger = logging.getLogger('uvicorn.error')

class Line(str, Enum):
	hxr = "HXR"
	sxr = "SXR"

class Machine(str, Enum):
	sc = "SC"
	nc = "NC"

class Hutch(BaseModel):
	name: str
	color: str
	line: Line
	text_color: str

class Event(BaseModel):
	"""
	Describes a single item on the program calendar.
	"""
	url: str
	program_name: str | None = None
	description: str | None = None
	note: str | None = None
	calendar: str
	details: str | None = None
	start: datetime.datetime
	end: datetime.datetime
	tags: List[str] | None = None
	poc: str | None = None
	config: str | None = None
	hutch: Hutch | None = None
	machine: str

class TimetableRow(BaseModel):
	start: datetime.datetime
	end: datetime.datetime
	events: List[Event]

class LCLSEventClient(GoogleCalendarEvents):
	def __init__(self):
		super().__init__()
		# Incredibly nasty regex alert!
		# The first group (\[.+\])* matches one or more "tags"
		# like [Photon MD] or [Secondary]
		# The next group ([^(]+) matches text, this is usually the experiment
		# name and PI name  It does NOT match on "(", which is the start
		# of the next group.
		# The next group (?:\(([^)]+)\))? matches an (optional) experiment
		# point of contact.
		# The next group (?:\(([^)]+)\))? matches an (optional) machine
		# configuration.
		self.event_description_pattern = re.compile(r"^\s*(\[.+\])*\s*([^(]+)\s*(?:\(([^)]+)\))?\s*(?:\(([^)]+)\))?")
		# It took me an hour to make that regex, lol.
	
		self.hutches = {
			"TMO": Hutch(name="TMO", color="#668cd8", line=Line.sxr, text_color="white"),
			"ChemRIXS": Hutch(name="ChemRIXS", color="#b46313", line=Line.sxr, text_color="white"),
			"qRIXS": Hutch(name="qRIXS", color="#b46313", line=Line.sxr, text_color="white"),
			"TXI": Hutch(name="TXI", color="#7e7e7e", line=Line.sxr, text_color="white"),
			"XPP": Hutch(name="XPP", color="#00a53e", line=Line.hxr, text_color="white"),
			"XCS": Hutch(name="XCS", color="#5c0087", line=Line.hxr, text_color="white"),
			"MFX": Hutch(name="MFX", color="#d28500", line=Line.hxr, text_color="black"),
			"CXI": Hutch(name="CXI", color="#a00000", line=Line.hxr, text_color="white"),
			"MEC": Hutch(name="MEC", color="#edd000", line=Line.hxr, text_color="black"),
		}
		self.calendars = {calendar.id: calendar for calendar in all_calendars}
	
	def make_event_dict(self, raw_event) -> Event:
		raw_description = raw_event['summary']
		m = self.event_description_pattern.match(raw_description)
		# Turn a string like "[A][B]" into a list like ["A", "B"]
		tags = None
		poc = None
		config = None
		description = None
		program_name = None
		if m is None:
			description = raw_description
		else:
			if m.group(1):
				tags = m.group(1).replace("]","").strip("[").split("[")
			if m.group(2):
				program_name = m.group(2).strip()
				description = program_name
			maybe_poc = m.group(3)
			maybe_config = m.group(4)
			if maybe_poc is not None and re.search(r'\d', maybe_poc):
				# if maybe_poc has numbers in it, it is probably
				# config info, not actually a poc.
				config = maybe_poc
				poc = maybe_config
			else:
				poc = maybe_poc
				config = maybe_config
			
		hutch = None
		calendar = self.calendars[raw_event['organizer']['email']]
		if calendar.hutch is not None:
			hutch = self.hutches[calendar.hutch]
			description = f"Deliver to {calendar.hutch}"
		if "PAMM" in calendar.name:
			description = f"Beam off for {program_name}"
		
		start_date = datetime.datetime.fromisoformat(raw_event['start']['dateTime'])
		end_date = datetime.datetime.fromisoformat(raw_event['end']['dateTime'])
		return Event(
			url=raw_event['htmlLink'],
			program_name=program_name,
			description=description,
			note=raw_event.get('location'),
			calendar=calendar.name,
			details=raw_event.get('description'),
			start=start_date,
			end=end_date,
			tags=tags,
			poc=poc,
			config=config,
			hutch=hutch,
			machine=calendar.machine
		)
	
	def fetch_events(self, line=None, machine=None, non_program_events=False, start_time=None, end_time=None, limit=None) -> list[Event]:
		self.authenticate()
		authorized_http = google_auth_httplib2.AuthorizedHttp(self.creds, http=self.make_http_interface())
		service = build("calendar", "v3", http=authorized_http)
		if start_time is None:
			start_time = datetime.datetime.now()
		if end_time is None:
			end_time = start_time + datetime.timedelta(days=1)
		if start_time.tzinfo is None:
			start_time = start_time.astimezone(ZoneInfo("America/Los_Angeles"))
		if end_time.tzinfo is None:
			end_time = end_time.astimezone(ZoneInfo("America/Los_Angeles"))
		start_time = start_time.isoformat()
		end_time = end_time.isoformat()
		
		# This fingerprint uniquely identifies the requested data.
		# We will use this fingerprint for caching.
		fingerprint = (None if line is None else line.value, None if machine is None else machine.value, non_program_events, start_time, end_time)
		if fingerprint in self.event_cache:
			logger.debug("Using cached value.")
			all_events = self.event_cache[fingerprint]
		else:
			calendars_to_fetch = []
			for calendar in self.calendars.values():
				if (line is None or calendar.line == line.value or calendar.line is None) and (machine is None or calendar.machine == machine.value) and (calendar.is_program or non_program_events):
					calendars_to_fetch.append(calendar)
			calendar_ids = [calendar.id for calendar in calendars_to_fetch]
			requests = [self.events_request_for_calendar(service, calendar_id, start_time, end_time) for calendar_id in calendar_ids]
			all_events = self.fetch_batch_events(service, requests)
			all_events = [self.make_event_dict(event) for event in all_events if 'dateTime' in event.get('start', {})]
			all_events.sort(key=lambda e: e.start)
			self.event_cache[fingerprint] = all_events
		if limit is not None:
			return all_events[:limit]
		return all_events