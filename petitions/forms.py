#forms.py
from django import forms  # Django forms module for building form classe
from .models import Petition  # Import the Petition model to create a ModelForm


class PetitionForm(forms.ModelForm):
    """Form used to create a new Petition.

    This ModelForm exposes `title` and `description` fields from the model.
    """
    class Meta:
        model = Petition  # Backing model for the form
        fields = ['title', 'description']  # Fields exposed to users
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),  # Render description as a 4-line textarea
        }
