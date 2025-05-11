import csv
from datetime import datetime
import io

from django.db.models import Min
from django.utils.dateparse import parse_date, parse_datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from patient.models import Patient, PatientVisit
from patient.serializers import PatientSerializer


class PatientBulkUploadView(APIView):
    """ """

    def post(self, request, *args, **kwargs):
        files = request.FILES.getlist("files", [])
        if not files:
            return Response(
                {"message": "At least one CSV file is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        required_fields = {"mr_number", "first_name", "last_name", "date", "reason"}
        summary = {
            "files_processed": 0,
            "total_added": 0,
            "total_duplicates": 0,
            "file_stats": [],
        }
        for file in files:
            added = 0
            duplicates = 0
            errors = []

            try:
                decoded_content = file.read().decode("utf-8")
                csv_reader = csv.DictReader(io.StringIO(decoded_content))
            except Exception as exp:
                summary["file_stats"].append(
                    {"file": file.name, "error": f"Failed to read CSV {exp}"}
                )

            for i, row in enumerate(csv_reader, start=2):
                if not required_fields.issubset(row.keys()):
                    errors.append(f"Row {i}: missing required fields")
                    continue

                try:
                    mr_number = int(row["mr_number"])
                except (ValueError, TypeError):
                    errors.append(f"Row {i}: Invalid mr_number")
                    continue

                dob = None
                dob = parse_date(row["dob"])
                if not dob:
                    try:
                        dob = datetime.strptime(row["dob"], "%m/%d/%Y")
                    except Exception:
                        errors.append(f"Row {i}: Invalid format for dob")
                        continue

                visited_date = parse_datetime(row["date"])
                if not visited_date:
                    try:
                        visited_date = datetime.strptime(row["date"], "%m/%d/%Y %H:%M")
                        visited_date = visited_date.replace(second=0, microsecond=0)
                    except Exception:
                        errors.append(f"Row {i}: Invalid visited_date format")
                        continue

                patient, _ = Patient.objects.get_or_create(
                    mr_number=mr_number,
                    defaults={
                        "first_name": row["first_name"],
                        "last_name": row["last_name"],
                        "dob": dob,
                    },
                )

                if PatientVisit.objects.filter(
                    patient=patient, visited_date=visited_date, reason=row["reason"]
                ).exists():
                    duplicates += 1
                    continue

                PatientVisit.objects.create(
                    patient=patient, visited_date=visited_date, reason=row["reason"]
                )
                added += 1

            summary["files_processed"] += 1
            summary["total_added"] += added
            summary["total_duplicates"] += duplicates
            summary["file_stats"].append(
                {
                    "file": file.name,
                    "added": added,
                    "duplicates": duplicates,
                    "errors": errors,
                }
            )

        return Response(summary, status=status.HTTP_200_OK)


class PatientView(APIView):
    """ """

    def get(self, request, *args, **kwargs):
        patients_qs = Patient.objects.annotate(
            first_visit_date=Min("visits__visited_date")
        ).order_by("first_visit_date", "created")

        paginator = PageNumberPagination()
        patients = paginator.paginate_queryset(patients_qs, request)
        serializer = PatientSerializer(patients, many=True)

        return paginator.get_paginated_response(serializer.data)
