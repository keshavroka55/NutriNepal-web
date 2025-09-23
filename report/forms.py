from django import forms
from .models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['subject', 'description', 'priority', 'attachment']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Short summary'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Steps to reproduce, expected vs actual, screenshots, console logs...'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'attachment': forms.FileInput(attrs={'class': 'form-control'}),
        }

class AdminUpdateForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['status', 'priority', 'admin_comment', 'resolved_by']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'admin_comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'resolved_by': forms.Select(attrs={'class': 'form-select'}),
        }
