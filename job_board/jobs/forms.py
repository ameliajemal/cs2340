from django import forms
from .models import Job, Skill

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title', 'company', 'location', 'description', 'job_type'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Senior Software Engineer'
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Tech Corp Inc.'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., San Francisco, CA'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Describe the role, responsibilities, and requirements...'
            }),
            'job_type': forms.Select(attrs={
                'class': 'form-select'
            })
        }
class JobFilterForm(forms.Form):
    q = forms.CharField(
        required=False,
        label="Keyword",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Title, company, description or skill…"})
    )

    location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g., New York, NY"})
    )

    skills = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Skill.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "form-select", "size": 6})
    )

    salary_min = forms.IntegerField(
        required=False, min_value=0,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Min $"}),
        label="Min salary (USD)"
    )
    salary_max = forms.IntegerField(
        required=False, min_value=0,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Max $"}),
        label="Max salary (USD)"
    )

    remote = forms.ChoiceField(
        required=False,
        choices=[("", "Any"), ("remote", "Remote"), ("onsite", "On-site")],
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Remote / On-site"
    )

    sponsorship = forms.ChoiceField(
        required=False,
        choices=[("", "Any"), ("yes", "Visa sponsorship available"), ("no", "No sponsorship")],
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Visa sponsorship"
    )