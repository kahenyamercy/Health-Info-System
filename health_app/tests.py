from django.test import TestCase, Client as TestClient
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Client, HealthProgram, Enrollment

class ModelTests(TestCase):
    def setUp(self):
        # Create test health programs
        self.tb_program = HealthProgram.objects.create(
            name="Tuberculosis Program",
            description="TB treatment and prevention program"
        )
        self.hiv_program = HealthProgram.objects.create(
            name="HIV/AIDS Program",
            description="HIV treatment and prevention program"
        )
        
        # Create test client
        self.client_john = Client.objects.create(
            first_name="John",
            last_name="Doe",
            date_of_birth=timezone.now().date() - timedelta(days=365*30),  # 30 years old
            gender="M",
            contact_number="1234567890",
            email="john@example.com",
            address="123 Main St"
        )
        
        # Create enrollment
        self.enrollment = Enrollment.objects.create(
            client=self.client_john,
            program=self.tb_program,
            notes="Initial enrollment"
        )
    
    def test_health_program_str(self):
        self.assertEqual(str(self.tb_program), "Tuberculosis Program")
    
    def test_client_str(self):
        self.assertEqual(str(self.client_john), "John Doe")
    
    def test_client_get_full_name(self):
        self.assertEqual(self.client_john.get_full_name(), "John Doe")
    
    def test_client_get_age(self):
        # Approximately test age calculation
        self.assertAlmostEqual(self.client_john.get_age(), 30, delta=1)
    
    def test_enrollment_str(self):
        self.assertEqual(str(self.enrollment), "John Doe enrolled in Tuberculosis Program")
    
    def test_client_programs_relationship(self):
        self.assertEqual(self.client_john.programs.count(), 1)
        self.assertEqual(self.client_john.programs.first(), self.tb_program)
        
        # Enroll in another program
        Enrollment.objects.create(
            client=self.client_john,
            program=self.hiv_program
        )
        
        # Refresh from DB and check programs
        self.client_john.refresh_from_db()
        self.assertEqual(self.client_john.programs.count(), 2)


class ViewTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        
        # Create test client
        self.test_client = TestClient()
        
        # Create test data
        self.tb_program = HealthProgram.objects.create(
            name="Tuberculosis Program",
            description="TB treatment and prevention program"
        )
        
        self.john = Client.objects.create(
            first_name="John",
            last_name="Doe",
            date_of_birth=timezone.now().date() - timedelta(days=365*30),
            gender="M",
            contact_number="1234567890",
            email="john@example.com",
            address="123 Main St"
        )
    
    def test_dashboard_view(self):
        # Login required redirect expected
        response = self.test_client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        
        # Now login and try again
        self.test_client.login(username='testuser', password='testpassword')
        response = self.test_client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'health_app/dashboard.html')
    
    def test_client_list_view(self):
        self.test_client.login(username='testuser', password='testpassword')
        response = self.test_client.get(reverse('client_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'health_app/client_list.html')
        self.assertContains(response, "John Doe")
    
    def test_client_create_view(self):
        self.test_client.login(username='testuser', password='testpassword')
        
        # Get the form
        response = self.test_client.get(reverse('client_create'))
        self.assertEqual(response.status_code, 200)
        
        # Submit the form with data
        data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'date_of_birth': '1995-05-15',
            'gender': 'F',
            'contact_number': '9876543210',
            'email': 'jane@example.com',
            'address': '456 Oak St'
        }
        response = self.test_client.post(reverse('client_create'), data)
        
        # Check if redirect to client list
        self.assertRedirects(response, reverse('client_list'))
        
        # Check if client was created
        self.assertTrue(Client.objects.filter(first_name='Jane', last_name='Smith').exists())
    
    def test_client_detail_view(self):
        self.test_client.login(username='testuser', password='testpassword')
        response = self.test_client.get(reverse('client_detail', kwargs={'pk': self.john.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'health_app/client_detail.html')
        self.assertContains(response, "John Doe")
    
    def test_client_enroll_view(self):
        self.test_client.login(username='testuser', password='testpassword')
        
        # Enroll client in program
        data = {
            'program': self.tb_program.id,
            'notes': 'Test enrollment'
        }
        response = self.test_client.post(reverse('client_enroll', kwargs={'pk': self.john.pk}), data)
        
        # Check if redirect back to client detail
        self.assertRedirects(response, reverse('client_detail', kwargs={'pk': self.john.pk}))
        
        # Check if enrollment was created
        self.assertTrue(Enrollment.objects.filter(client=self.john, program=self.tb_program).exists())


class APITests(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        
        # Create test data
        self.tb_program = HealthProgram.objects.create(
            name="Tuberculosis Program",
            description="TB treatment and prevention program"
        )
        
        self.john = Client.objects.create(
            first_name="John",
            last_name="Doe",
            date_of_birth=timezone.now().date() - timedelta(days=365*30),
            gender="M",
            contact_number="1234567890",
            email="john@example.com",
            address="123 Main St"
        )
        
        self.enrollment = Enrollment.objects.create(
            client=self.john,
            program=self.tb_program,
            notes="Initial enrollment"
        )
    
    def test_get_clients_list_unauthenticated(self):
        url = reverse('client-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_get_clients_list_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('client-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_get_client_detail(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('client-detail', kwargs={'pk': self.john.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'John')
        self.assertEqual(response.data['last_name'], 'Doe')
        
        # Check that the enrollment data is included
        self.assertEqual(len(response.data['enrollments']), 1)
        self.assertEqual(response.data['enrollments'][0]['program']['name'], 'Tuberculosis Program')