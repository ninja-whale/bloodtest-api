from django.db import models

# Create your models here.
# Model definition
from django.db import models
from django.core.validators import MinValueValidator


# Define the BloodTest model
class BloodTest(models.Model):
    """
    Model representing a blood test record.
    Fields:
        - patient_id: ID of the patient.
        - test_name: Name of the test (e.g., Glucose, Hemoglobin).
        - value: Numeric result of the test.
        - unit: Unit of the test result.
        - test_date: Date when the test was conducted.
        - is_abnormal: Boolean indicating if the result is abnormal.
    """
    patient_id = models.IntegerField()
    test_name = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50)
    test_date = models.DateTimeField()
    is_abnormal = models.BooleanField()

    def __str__(self):
        return f"{self.test_name} for Patient {self.patient_id}"
