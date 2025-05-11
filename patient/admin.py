from django.contrib import admin
from patient.models import Patient, PatientVisit


class PatientVisitInline(admin.TabularInline):
    model = PatientVisit
    extra = 0
    readonly_fields = ["visited_date", "reason"]
    can_delete = False


class PatientAdmin(admin.ModelAdmin):
    list_display = ("mr_number", "first_name", "last_name", "dob")
    search_fields = ("mr_number", "first_name", "last_name")
    list_filter = ("dob",)
    inlines = [PatientVisitInline]


class PatientVisitAdmin(admin.ModelAdmin):
    list_display = ("patient", "visited_date", "reason")
    search_fields = ("patient__first_name", "patient__last_name", "reason")
    list_select_related = ("patient",)
    list_filter = ("visited_date",)


admin.site.register(Patient, PatientAdmin)
admin.site.register(PatientVisit, PatientVisitAdmin)
