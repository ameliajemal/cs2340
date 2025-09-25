from django import forms
from .models import Profile, Education, WorkExperience, ProfileSkill, Project
from jobs.models import Skill

# ---------------- Profile Form ----------------
class ProfileForm(forms.ModelForm):
    # Make location required at the form level
    location = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City, State or Country'})
    )
    # Optional links
    linkedin = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'LinkedIn URL'}))
    github = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'GitHub URL'}))
    portfolio = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Portfolio URL'}))
    # Non-model field to manage ProfileSkill
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': 6})
    )
    class Meta:
        model = Profile
        fields = ['headline', 'bio', 'location', 'linkedin', 'github', 'portfolio', 'projects_text']
        widgets = {
            'headline': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Professional headline'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write a short bio...'}),
            'projects_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your projects, tech used, role, and impact...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Prepopulate skills from ProfileSkill for the instance
        instance = getattr(self, 'instance', None)
        if instance is not None and instance.pk:
            current_skills = Skill.objects.filter(profileskill__profile=instance)
            self.fields['skills'].initial = current_skills

    def save(self, commit=True):
        profile = super().save(commit=commit)
        # If the instance is not saved yet (no PK), we cannot manage related skills.
        if not getattr(profile, 'pk', None):
            return profile
        # Update ProfileSkill records based on submitted skills
        skills = self.cleaned_data.get('skills')
        if skills is not None:
            # Clear existing
            ProfileSkill.objects.filter(profile=profile).delete()
            # Create new links
            if skills:
                ProfileSkill.objects.bulk_create([
                    ProfileSkill(profile=profile, skill=s) for s in skills
                ])
        return profile

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

# ---------------- Project Form ----------------
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'url']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Project name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'What did you build? What tech? Your role?'}),
            'url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Optional link to the project'}),
        }

class CandidateSearchForm(forms.Form):
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            "class": "form-select",
            "size": 6,
        }),
        help_text="Select one or more skills",
    )
    location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "e.g., Atlanta, GA or Remote",
        }),
        help_text="Filter by candidate location",
    )

    project_keywords = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "e.g., Django, React, mobile app",
        }),
        help_text="Search within candidate project names and descriptions",
    )