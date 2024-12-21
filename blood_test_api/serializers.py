from rest_framework.serializers import ModelSerializer, ValidationError
from .models import BloodTest

class BloodTestSerializer(ModelSerializer):
    """
    Serializer for BloodTest model with validation logic.
    """
    class Meta:
        model = BloodTest
        fields = '__all__'

    def validate(self, data):
        if data['value'] < 0:
            raise ValidationError("Test value cannot be negative.")
        return data
