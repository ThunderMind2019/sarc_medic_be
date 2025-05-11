"""
URL configuration for patient app
"""

from django.urls import path

from patient.views import PatientBulkUploadView, PatientView


urlpatterns = [
    path(
        "patient/bulk_upload/",
        PatientBulkUploadView.as_view(),
        name="patient_bulk_upload",
    ),
    path("patients/", PatientView.as_view(), name="patients"),
]
