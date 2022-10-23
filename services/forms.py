from dataclasses import fields
from django import forms
from .models import Letter, Service
from django.contrib.admin.widgets import FilteredSelectMultiple


class LetterForm(forms.ModelForm):
    # services = forms.ModelMultipleChoiceField(queryset=Service.objects.all(), to_field_name="name",widget=forms.CheckboxSelectMultiple())

    # # def __init__(self, *args, **kwargs):
    # #     super(LetterForm, self).__init__(*args, **kwargs)
    # #     instance = getattr(self, 'instance', None)
    # #     if instance and instance.pk:
    # #         if instance.name is not None:
    # #           self.fields['name'].widget.attrs['readonly'] = True
    services = forms.ModelMultipleChoiceField(queryset=Service.objects.all(), widget=FilteredSelectMultiple("services", is_stacked=True))
    class Meta:
        model  = Letter        
        
        fields = ['name','naId','by_doctor','law','ayada','diagnosis','description','price','services','entity','created_by']
        # fields = __all__