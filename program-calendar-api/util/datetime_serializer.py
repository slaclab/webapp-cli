import datetime
def datetime_serializer(obj):
	if isinstance(obj, (datetime.datetime)):
		return obj.isoformat()
	raise TypeError("Type %s not serializable" % type(obj))