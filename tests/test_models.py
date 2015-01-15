import mock
from django.test import TestCase
from django.utils import timezone
from push_notifications.models import GCMDevice, APNSDevice
from tests.mock_responses import GCM_PLAIN_RESPONSE


class ModelTestCase(TestCase):
	def test_can_save_gcm_device(self):
		device = GCMDevice.objects.create(
			registration_id="a valid registration id"
		)
		assert device.id is not None
		assert device.date_created is not None
		assert device.date_created.date() == timezone.now().date()

	def test_can_save_apns_device(self):
		device = APNSDevice.objects.create(
			registration_id="a valid registration id"
		)
		assert device.id is not None
		assert device.date_created is not None
		assert device.date_created.date() == timezone.now().date()

	def test_can_save_duplicate_apns_device(self):
		before_count = APNSDevice.objects.all().count()

		APNSDevice.objects.create(
			registration_id="a valid registration id",
			device_id="2CA3E8AD-894F-4C04-A548-20C35CB99F45"
		)
		APNSDevice.objects.create(
			registration_id="a new valid registration id",
			device_id="2CA3E8AD-894F-4C04-A548-20C35CB99F45"
		)

		after_count = APNSDevice.objects.all().count()
		assert after_count is before_count + 1


	def test_gcm_send_message(self):
		device = GCMDevice.objects.create(
			registration_id="abc",
		)
		with mock.patch("push_notifications.gcm._gcm_send", return_value=GCM_PLAIN_RESPONSE) as p:
			device.send_message("Hello world")
			p.assert_called_once_with(
				b"data.message=Hello+world&registration_id=abc",
				"application/x-www-form-urlencoded;charset=UTF-8")

	def test_gcm_send_message_extra(self):
		device = GCMDevice.objects.create(
			registration_id="abc",
		)
		with mock.patch("push_notifications.gcm._gcm_send", return_value=GCM_PLAIN_RESPONSE) as p:
			device.send_message("Hello world", extra={"foo": "bar"})
			p.assert_called_once_with(
				b"data.foo=bar&data.message=Hello+world&registration_id=abc",
				"application/x-www-form-urlencoded;charset=UTF-8")

	def test_apns_send_message(self):
		device = APNSDevice.objects.create(
			registration_id="abc",
		)
		socket = mock.MagicMock()
		with mock.patch("push_notifications.apns._apns_pack_frame") as p:
			device.send_message("Hello world", socket=socket, expiration=1)
			p.assert_called_once_with("abc", b'{"aps":{"alert":"Hello world"}}', 0, 1, 10)

	def test_apns_send_message_extra(self):
		device = APNSDevice.objects.create(
			registration_id="abc",
		)
		socket = mock.MagicMock()
		with mock.patch("push_notifications.apns._apns_pack_frame") as p:
			device.send_message("Hello world", extra={"foo": "bar"}, socket=socket, identifier=1, expiration=2, priority=5)
			p.assert_called_once_with("abc", b'{"aps":{"alert":"Hello world"},"foo":"bar"}', 1, 2, 5)
