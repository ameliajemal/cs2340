from django import template
from accounts.models import UserProfile

register = template.Library()

@register.filter
def is_recruiter(user):
    """Check if user is a recruiter"""
    try:
        return user.userprofile.role == 'recruiter'
    except UserProfile.DoesNotExist:
        return False
