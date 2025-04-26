from rest_framework import serializers
from ..models import Client, HealthProgram, Enrollment

class HealthProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthProgram
        fields = ['id', 'name', 'description', 'created_date']

class EnrollmentSerializer(serializers.ModelSerializer):
    program = HealthProgramSerializer(read_only=True)
    
    class Meta:
        model = Enrollment
        fields = ['id', 'program', 'enrollment_date', 'is_active', 'notes']

class ClientSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    enrollments = serializers.SerializerMethodField()
    
    class Meta:
        model = Client
        fields = [
            'id', 'first_name', 'last_name', 'date_of_birth', 
            'gender', 'contact_number', 'email', 'address', 
            'registration_date', 'age', 'enrollments'
        ]
    
    def get_age(self, obj):
        return obj.get_age()
    
    def get_enrollments(self, obj):
        enrollments = Enrollment.objects.filter(client=obj)
        return EnrollmentSerializer(enrollments, many=True).data