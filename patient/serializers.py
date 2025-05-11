from rest_framework import serializers
from patient.models import Patient, PatientVisit


class PatientVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientVisit
        fields = ["visited_date", "reason"]


class PatientSerializer(serializers.ModelSerializer):
    visits = PatientVisitSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = ["mr_number", "first_name", "last_name", "dob", "visits"]
