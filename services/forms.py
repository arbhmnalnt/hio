from dataclasses import fields
from django import forms
from .models import Letter, Service
from django.contrib.admin.widgets import FilteredSelectMultiple


class LetterForm(forms.ModelForm):
    # custom_ayada =
    services = forms.ModelMultipleChoiceField(queryset=Service.objects.all(), widget=FilteredSelectMultiple("services", is_stacked=True))
    class Meta:
        model  = Letter

        fields = ['serial','name','naId','by_doctor','law','ayada','diagnosis','description','price','services','entity','created_by']
        # fields = __all__