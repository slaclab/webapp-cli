import datetime
from zoneinfo import ZoneInfo
import logging
from .calendars import all_calendars
from googleapiclient.discovery import build
import google_auth_httplib2

from typing import List
from pydantic import BaseModel

from base_events import GoogleCalendarEvents

logger = logging.getLogger('uvicorn.error')

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

class TimetableRow(BaseModel):
	start: datetime.datetime
	end: datetime.datetime
	events: List[Event]

class SPEAREventClient(GoogleCalendarEvents):
	def __init__(self):
		super().__init__()
		self.calendars = {calendar.id: calendar for calendar in all_calendars}
	
	def make_event_dict(self, raw_event) -> Event:
		raw_description = raw_event['summary']
		program_name = raw_description
		calendar = self.calendars[raw_event['organizer']['email']]
		if "PAMM" in calendar.name:
			description = "Beam off for SPEAR PAMM"
		else:
			description = ""
		
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
			end=end_date
		)
	
	def fetch_events(self, start_time=None, end_time=None, limit=None) -> list[Event]:
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
		fingerprint = (start_time, end_time)
		if fingerprint in self.event_cache:
			logger.debug("Using cached value.")
			all_events = self.event_cache[fingerprint]
		else:
			calendars_to_fetch = self.calendars.values()
			calendar_ids = [calendar.id for calendar in calendars_to_fetch]
			requests = [self.events_request_for_calendar(service, calendar_id, start_time, end_time) for calendar_id in calendar_ids]
			all_events = self.fetch_batch_events(service, requests)
			all_events = [self.make_event_dict(event) for event in all_events if 'dateTime' in event.get('start', {})]
			all_events.sort(key=lambda e: e.start)
			self.event_cache[fingerprint] = all_events
		if limit is not None:
			return all_events[:limit]
		return all_events