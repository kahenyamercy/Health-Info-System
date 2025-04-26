from rest_framework import viewsets, filters, permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django_filters.rest_framework import DjangoFilterBackend

from ..models import Client, HealthProgram, Enrollment
from .serializers import ClientSerializer, HealthProgramSerializer, EnrollmentSerializer

class ClientViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows clients to be viewed.
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['gender']
    search_fields = ['first_name', 'last_name', 'email']

class HealthProgramViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows health programs to be viewed.
    """
    queryset = HealthProgram.objects.all()
    serializer_class = HealthProgramSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

class EnrollmentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows enrollments to be viewed.
    """
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['client', 'program', 'is_active']