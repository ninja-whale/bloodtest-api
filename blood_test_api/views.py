from rest_framework.views import APIView
from django.db import models
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from .models import BloodTest
from rest_framework.parsers import JSONParser, FileUploadParser
from .serializers import BloodTestSerializer
import csv
from io import TextIOWrapper
import mimetypes


class BloodTestCreateAPIView(APIView):
    """
    API view to create a new blood test record.
    POST:
        - Request body: JSON containing blood test details.
        - Response: Newly created blood test record or error details.
    """
    def post(self, request):
        serializer = BloodTestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BloodTestListAPIView(APIView):
    """
    API view to retrieve all tests for a specific patient.
    GET:
        - Query parameter: patient_id
        - Response: List of tests for the patient or error message.
    """
    def get(self, request):
        patient_id = request.query_params.get('patient_id')
        if not patient_id:
            return Response({"error": "patient_id query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        tests = BloodTest.objects.filter(patient_id=patient_id)
        serializer = BloodTestSerializer(tests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# Endpoint to get basic statistics
class BloodTestStatsAPIView(APIView):
    """
    API view to retrieve aggregated statistics for blood tests.
    GET:
        - Response: Aggregated statistics or error message.
    """
    def get(self, request):
        try:
            stats_cache = cache.get('test_stats')
            if stats_cache:
                return Response(stats_cache, status=status.HTTP_200_OK)
        except ConnectionError:
            # Fall back to non-cached logic
            pass

        # Compute statistics (if Redis unavailable)
        stats = BloodTest.objects.values('test_name').annotate(
            min_value=models.Min('value'),
            max_value=models.Max('value'),
            avg_value=models.Avg('value'),
            total_tests=models.Count('id'),
            abnormal_count=models.Count('id', filter=models.Q(is_abnormal=True))
        )
        stats_data = {
            stat['test_name']: {
                "min_value": stat['min_value'],
                "max_value": stat['max_value'],
                "avg_value": stat['avg_value'],
                "total_tests": stat['total_tests'],
                "abnormal_count": stat['abnormal_count']
            } for stat in stats
        }
        return Response(stats_data, status=status.HTTP_200_OK)


# Endpoint for batch upload via CSV
class BloodTestBatchUploadAPIView(APIView):
    """
    API view to handle batch upload of blood test records via CSV.
    POST:
        - Request body: CSV file containing blood test records.
        - Response: Success message or error details.
    """
    parser_classes = [FileUploadParser]

    def post(self, request):
        if 'file' not in request.data:
            return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

        file = request.data['file']

        # Check if the file is CSV
        file_type, _ = mimetypes.guess_type(file.name)
        if file_type != 'text/csv':
            return Response({"error": "Invalid file type. Please upload a CSV file."}, status=status.HTTP_400_BAD_REQUEST)

        file = TextIOWrapper(file.file, encoding='utf-8')
        reader = csv.DictReader(file)

        records = []
        for row in reader:
            try:
                record = BloodTest(
                    patient_id=row['patient_id'],
                    test_name=row['test_name'],
                    value=row['value'],
                    unit=row['unit'],
                    test_date=row['test_date'],
                    is_abnormal=row['is_abnormal'].lower() == 'true'
                )
                records.append(record)
            except KeyError as e:
                return Response({"error": f"Missing column in CSV: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        BloodTest.objects.bulk_create(records)
        return Response({"message": "Batch upload successful."}, status=status.HTTP_201_CREATED)
