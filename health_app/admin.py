from django.contrib import admin
from .models import Client, HealthProgram, Enrollment

@admin.register(HealthProgram)
class HealthProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_date')
    search_fields = ('name',)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'gender', 'contact_number', 'registration_date')
    list_filter = ('gender', 'registration_date')
    search_fields = ('first_name', 'last_name', 'contact_number', 'email')
    date_hierarchy = 'registration_date'

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'program', 'enrollment_date', 'is_active')
    list_filter = ('program', 'enrollment_date', 'is_active')
    search_fields = ('client__first_name', 'client__last_name', 'program__name')
    date_hierarchy = 'enrollment_date'