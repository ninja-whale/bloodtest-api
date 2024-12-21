from django.urls import path
from .views import BloodTestBatchUploadAPIView, BloodTestCreateAPIView, BloodTestListAPIView, BloodTestStatsAPIView

urlpatterns = [
    path('tests/', BloodTestCreateAPIView.as_view()),
    path('tests/list/', BloodTestListAPIView.as_view()),
    path('tests/stats/', BloodTestStatsAPIView.as_view()),
    path('tests/batch-upload/', BloodTestBatchUploadAPIView.as_view()),
]