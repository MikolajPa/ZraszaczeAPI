from django.test import TestCase
from rest_framework.test import APIClient
from .models import Device
from .views import DeviceCrud

class TestDeviceCrud(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.device1 = Device.objects.create(GUID='device1', location='location1')
        self.device2 = Device.objects.create(GUID='device2', location='location2')

    def test_get_all_devices(self):
        response = self.client.get('/devices/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['GUID'], self.device1.GUID)
        self.assertEqual(response.data[0]['location'], self.device1.location)
        self.assertEqual(response.data[1]['GUID'], self.device2.GUID)
        self.assertEqual(response.data[1]['location'], self.device2.location)