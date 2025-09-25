from django import forms
from .models import Profile, Education, WorkExperience
from jobs.models import Skill

# ---------------- Profile Form ----------------
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['headline', 'bio', 'skills', 'linkedin', 'github', 'portfolio']
        widgets = {
            'headline': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Professional headline'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write a short bio...'}),
            'skills': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 6}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'LinkedIn URL'}),
            'github': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'GitHub URL'}),
            'portfolio': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Portfolio URL'}),
        }

# ---------------- Education Form ----------------
class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['institution', 'degree', 'field_of_study', 'start_date', 'end_date']
        widgets = {
            'institution': forms.TextInput(attrs={'class': 'form-control'}),
            'degree': forms.TextInput(attrs={'class': 'form-control'}),
            'field_of_study': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

# ---------------- Work Experience Form ----------------
class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        fields = ['company', 'title', 'start_date', 'end_date', 'description']
        widgets = {
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
