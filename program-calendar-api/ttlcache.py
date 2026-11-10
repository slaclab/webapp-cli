import time
from collections import OrderedDict

class TTLCache:
	def __init__(self, maxsize: int, ttl: int):
		self.ttl = ttl
		self.maxsize = maxsize
		self.items = OrderedDict()
	
	def __getitem__(self, key):
		if key not in self:
			raise KeyError(key)
		self.items.move_to_end(key)
		_, item = self.items[key]
		return item
	
	def __setitem__(self, key, value):
		self.items[key] = time.monotonic(), value
		if len(self.items) > self.maxsize:
			self.items.popitem(last=False)
	
	def __contains__(self, key):
		if key not in self.items:
			return False
		ts, _ = self.items[key]
		if time.monotonic() - ts > self.ttl:
			return False
		return True