import os.path
import json
import logging
import urllib.parse
from functools import partial

from ttlcache import TTLCache

import requests
import httplib2
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

logger = logging.getLogger('uvicorn.error')

class GoogleCalendarEvents:
	"""
	A base class for interfacing with a google calendar.
	
	Not very useful on its own.  Each accelerator facility has its own subclass.
	"""
	def __init__(self):
		self.SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
		self.creds = None
		self.config = {}
		self.event_cache = TTLCache(maxsize=256, ttl=300)
		try:
			with open("config.json", "r") as f:
				self.config = json.load(f)
		except Exception as _:
			pass
		self.session = requests.Session()
		self.proxy_info = None
		if 'proxyURL' in self.config:
			# Use a proxy to tunnel to a public-facing machine.
			proxies = {"http": self.config['proxyURL'],
					   "https": self.config['proxyURL']}
			self.session.proxies = proxies
			parsed_proxy_url = urllib.parse.urlparse(self.config['proxyURL'])
			self.proxy_info = httplib2.ProxyInfo(proxy_type=httplib2.socks.PROXY_TYPE_SOCKS5,
							   proxy_host=parsed_proxy_url.hostname,
							   proxy_port=parsed_proxy_url.port
			)

	def make_http_interface(self):
		return httplib2.Http(proxy_info=self.proxy_info)

	def events_request_for_calendar(self, service, calendar_id, time_min, time_max):
		return service.events().list(
				calendarId=calendar_id,
				timeMin=time_min,
				timeMax=time_max,
				singleEvents=True,
				orderBy="startTime",)

	def fetch_batch_events(self, service, requests):
		batch_results = []
		batch = service.new_batch_http_request(callback=partial(self.batch_event_callback, batch_results))
		for request in requests:
			batch.add(request)
		batch.execute(http=self.make_http_interface())
		return batch_results
	
	def batch_event_callback(self, batch_results, _, response, exception):
		if exception is not None:
			logger.info("Failed to get some requests in the batch!")
			logger.info(str(exception))
			return
		batch_results.extend(response.get('items', []))

	def authenticate(self):
		if os.path.exists("token.json"):
			self.creds = Credentials.from_authorized_user_file("token.json", self.SCOPES)
		if not self.creds or not self.creds.valid:
			if self.creds and self.creds.expired and self.creds.refresh_token:
				r = Request(session=self.session)
				try:
					self.creds.refresh(r)
				except Exception as _:
					logger.info(dir(r))	
			else:
				flow = InstalledAppFlow.from_client_secrets_file("credentials.json", self.SCOPES)
				self.creds = flow.run_local_server(port=0)
			with open("token.json", "w") as token:
				token.write(self.creds.to_json())

	def make_event_timetable(self, events, limit=None):
		boundary_times = set([event.start for event in events])
		boundary_times.update([event.end for event in events])
		boundary_times = sorted(boundary_times)
		timetable = []
		for i in range(0,len(boundary_times)-1):
			t1 = boundary_times[i]
			t2 = boundary_times[i+1]
			events_in_timespan = []
			for event in events:
				if event.end > t1 and event.start < t2:
					events_in_timespan.append(event)
			timetable.append({"start": t1, "end": t2, "events": events_in_timespan})
		if limit is not None:
			return timetable[:limit]
		return timetable