from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView

from .models import Client, HealthProgram, Enrollment
from .forms import ClientForm, HealthProgramForm, EnrollmentForm, ClientSearchForm

# Authentication Views
class SignUpView(FormView):
    template_name = 'health_app/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Account created successfully! You can now log in.")
        return super().form_valid(form)

# Health Program Views
class HealthProgramListView(LoginRequiredMixin, ListView):
    model = HealthProgram
    template_name = 'health_app/program_list.html'
    context_object_name = 'programs'

class HealthProgramCreateView(LoginRequiredMixin, CreateView):
    model = HealthProgram
    form_class = HealthProgramForm
    template_name = 'health_app/program_form.html'
    success_url = reverse_lazy('program_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Health Program created successfully!')
        return super().form_valid(form)

# Client Views
class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'health_app/client_list.html'
    context_object_name = 'clients'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.GET.get('search', '')
        if search_term:
            queryset = queryset.filter(
                Q(first_name__icontains=search_term) | 
                Q(last_name__icontains=search_term)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = ClientSearchForm(self.request.GET or None)
        return context

class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'health_app/client_form.html'
    success_url = reverse_lazy('client_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Client registered successfully!')
        return super().form_valid(form)

class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'health_app/client_detail.html'
    context_object_name = 'client'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enrollments'] = Enrollment.objects.filter(client=self.object)
        context['enrollment_form'] = EnrollmentForm(client=self.object)
        return context

class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'health_app/client_update.html'
    
    def get_success_url(self):
        return reverse('client_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Client information updated successfully!')
        return super().form_valid(form)

# Enrollment Views
class EnrollClientView(LoginRequiredMixin, View):
    def post(self, request, pk):
        client = get_object_or_404(Client, pk=pk)
        form = EnrollmentForm(request.POST, client=client)
        
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.client = client
            enrollment.save()
            messages.success(request, f'Client enrolled in {enrollment.program.name} successfully!')
        else:
            messages.error(request, 'Error enrolling client in program.')
            
        return redirect('client_detail', pk=pk)
    
class UnenrollClientView(LoginRequiredMixin, View):
    def post(self, request, pk, program_pk):
        enrollment = get_object_or_404(
            Enrollment, 
            client__pk=pk, 
            program__pk=program_pk
        )
        program_name = enrollment.program.name
        enrollment.delete()
        messages.success(request, f'Client unenrolled from {program_name} successfully!')
        return redirect('client_detail', pk=pk)

# Dashboard View
class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        total_clients = Client.objects.count()
        total_programs = HealthProgram.objects.count()
        recent_clients = Client.objects.order_by('-registration_date')[:5]
        context = {
            'total_clients': total_clients,
            'total_programs': total_programs,
            'recent_clients': recent_clients,
        }
        return render(request, 'health_app/dashboard.html', context)