from dataclasses import fields
from django import forms
from .models import Category, DailyReport
from django.contrib.admin.widgets import FilteredSelectMultiple


class DailyReportForm(forms.ModelForm):
    class Meta:
        model  = DailyReport
        fields = ['category','num']