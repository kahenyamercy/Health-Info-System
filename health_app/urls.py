from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    # Authentication URLs
    path('login/', LoginView.as_view(template_name='health_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    
    # Dashboard
    path('', views.DashboardView.as_view(), name='dashboard'),
    
    # Health Program URLs
    path('programs/', views.HealthProgramListView.as_view(), name='program_list'),
    path('programs/create/', views.HealthProgramCreateView.as_view(), name='program_create'),
    
    # Client URLs
    path('clients/', views.ClientListView.as_view(), name='client_list'),
    path('clients/create/', views.ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/', views.ClientDetailView.as_view(), name='client_detail'),
    path('clients/<int:pk>/update/', views.ClientUpdateView.as_view(), name='client_update'),
    
    # Enrollment URLs
    path('clients/<int:pk>/enroll/', views.EnrollClientView.as_view(), name='client_enroll'),
    path('clients/<int:pk>/unenroll/<int:program_pk>/', views.UnenrollClientView.as_view(), name='client_unenroll'),
]