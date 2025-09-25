from django import forms
from jobs.models import Skill


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
