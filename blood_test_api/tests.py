# Unit tests
from django.test import TestCase
from rest_framework.test import APIClient
from datetime import datetime
from .models import BloodTest

class BloodTestAPITest(TestCase):
    """
    Unit tests for BloodTest API endpoints.
    """
    def setUp(self):
        self.client = APIClient()
        self.test_record = BloodTest.objects.create(
            patient_id=123,
            test_name="Hemoglobin",
            value=13.5,
            unit="g/dL",
            test_date=datetime.now(),
            is_abnormal=False
        )

    def test_create_test(self):
        """
        Test creating a new blood test record.
        """
        response = self.client.post('/api/tests/', {
            "patient_id": 124,
            "test_name": "Platelets",
            "value": 150.0,
            "unit": "10^3/uL",
            "test_date": "2024-12-16T12:00:00Z",
            "is_abnormal": False
        }, format='json')
        self.assertEqual(response.status_code, 201)

    def test_get_tests_for_patient(self):
        """
        Test retrieving all tests for a specific patient.
        """
        response = self.client.get('/api/tests/?patient_id=123')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_stats_caching(self):
        """
        Test retrieving cached statistics for blood tests.
        """
        response = self.client.get('/api/tests/stats/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Hemoglobin', response.data)