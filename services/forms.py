from dataclasses import fields
from django import forms
from django import forms
from .models import Letter


class LetterForm(forms.ModelForm):
    class Meta:
        model  = Letter
        fields = ['name','naId','by_doctor','law','ayada','diagnosis','description','price','services','entity','created_by']
        # fields = __all__