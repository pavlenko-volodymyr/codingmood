from django.contrib import admin
from django import forms

from django_ace import AceWidget

from .models import Badge

class BadgeAdminForm(forms.ModelForm):
    class Meta:
        model = Badge
        widgets = {
            # Add json editor.
            'qs': AceWidget(mode='json', attrs={'style': 'width:100%;'})
        }

class BadgeAdmin(admin.ModelAdmin):
    form = BadgeAdminForm

admin.site.register(Badge, BadgeAdmin)