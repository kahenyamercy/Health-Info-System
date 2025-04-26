from django import forms
from .models import Client, HealthProgram, Enrollment

class HealthProgramForm(forms.ModelForm):
    class Meta:
        model = HealthProgram
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'date_of_birth', 'gender', 
                  'contact_number', 'email', 'address']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['program', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        self.client = kwargs.pop('client', None)
        super(EnrollmentForm, self).__init__(*args, **kwargs)
        # Filter out programs the client is already enrolled in
        if self.client:
            enrolled_programs = self.client.programs.all()
            self.fields['program'].queryset = HealthProgram.objects.exclude(
                id__in=[p.id for p in enrolled_programs]
            )

class ClientSearchForm(forms.Form):
    search = forms.CharField(required=False, label='Search by name')