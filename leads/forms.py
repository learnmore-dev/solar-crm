from django import forms
from .models import Lead
from django.contrib.auth.models import User
# ===============================
# ENQUIRY FORM (No Status Field)
# ===============================
class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Lead
        exclude = ['status']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'medium': forms.Select(attrs={'class': 'form-select'}),
            'source': forms.Select(attrs={'class': 'form-select'}),
            'campaign': forms.Select(attrs={'class': 'form-select'}),
            'installation_type': forms.Select(attrs={'class': 'form-select'}),
            'roof_type': forms.Select(attrs={'class': 'form-select'}),
            'financing_preference': forms.Select(attrs={'class': 'form-select'}),
            'average_monthly_bill': forms.NumberInput(attrs={'class': 'form-control'}),
            'sanctioned_load': forms.NumberInput(attrs={'class': 'form-control'}),
            'follow_up_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'follow_up_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
# ===============================
# FULL LEAD FORM (WITH Status)
# ===============================
class LeadForm(forms.ModelForm):
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Lead
        fields = '__all__'   # ✅ VERY IMPORTANT

        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'follow_up_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'follow_up_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


# ===============================
# CONVERGENT FORM
# ===============================
class ConvergentLeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['status', 'follow_up_date', 'follow_up_time', 'remarks']

        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'follow_up_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'follow_up_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
from .models import Leave

class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['leave_date', 'leave_type', 'reason']

        widgets = {
            'leave_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'leave_type': forms.Select(attrs={'class': 'form-select'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['leave_date', 'leave_type', 'reason']

        widgets = {
            'leave_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'leave_type': forms.Select(attrs={'class': 'form-select'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }