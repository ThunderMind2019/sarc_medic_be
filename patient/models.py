from django.db import models

from model_utils.models import TimeStampedModel


class Patient(TimeStampedModel):
    """ """

    mr_number = models.PositiveBigIntegerField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    dob = models.DateField(null=True, blank=True, verbose_name="Date of Birth")


class PatientVisit(TimeStampedModel):
    """ """

    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="visits"
    )
    visited_date = models.DateTimeField()
    reason = models.TextField()
