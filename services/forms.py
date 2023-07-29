from dataclasses import fields
from django import forms
from .models import *
from django.contrib.admin.widgets import FilteredSelectMultiple


class LetterForm(forms.ModelForm):
    # custom_ayada =
    services = forms.ModelMultipleChoiceField(queryset=Service.objects.all(), widget=FilteredSelectMultiple("services", is_stacked=True))
    # ayada    = forms.ModelMultipleChoiceField(queryset=Ayadat.objects.all())
    class Meta:
        model  = Letter

        fields = ['serial','name','naId','by_doctor','law','ayada','diagnosis','description','price','services','entity','created_by']
        # fields = __all__

class sevicePriceForm(forms.ModelForm):
    class Meta:
        model = ServicePrice
        fields = ['name', 'price', 'notes']
