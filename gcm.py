import urllib2
from . import NotificationError


GCM_POST_URL = "https://android.googleapis.com/gcm/send"

class GCMError(NotificationError):
	pass

def _gcm_send(data, content_type):
	from django.conf import settings
	from django.core.exceptions import ImproperlyConfigured

	key = settings.PUSH_NOTIFICATIONS_SETTINGS.get("GCM_API_KEY")
	if not key:
		raise ImproperlyConfigured('You need to set PUSH_NOTIFICATIONS_SETTINGS["GCM_API_KEY"] to send messages through GCM.')

	headers = {
		"Content-Type": content_type,
		"Authorization": "key=%s" % (key),
		"Content-Length": str(len(data)),
	}

	request = urllib2.Request(GCM_POST_URL, data, headers)
	response = urllib2.urlopen(request)
	result = response.read()

	if result.startswith("Error="):
		raise GCMError(result)

	return result

def gcm_send_message(registration_id, data, collapse_key=None):
	"""
	Sends a GCM notification to a single registration_id.
	This will send the notification as form data.
	If sending multiple notifications, it is more efficient to use
	gcm_send_bulk_message()
	"""
	from urllib import urlencode

	values = {
		"registration_id": registration_id,
		"collapse_key": collapse_key,
	}

	for k, v in data.items():
		values["data.%s" % (k)] = v.encode("utf-8")

	data = urlencode(values)

	return _gcm_send(data, "application/x-www-form-urlencoded;charset=UTF-8")

def gcm_send_bulk_message(registration_ids, data, collapse_key=None, delay_while_idle=False):
	"""
	Sends a GCM notification to one or more registration_ids. The registration_ids
	needs to be a list.
	This will send the notification as json data.
	"""
	import json

	values = {
		"registration_ids": registration_ids,
		"collapse_key": collapse_key,
		"data": data,
	}

	if delay_while_idle:
		values["delay_while_idle"] = delay_while_idle