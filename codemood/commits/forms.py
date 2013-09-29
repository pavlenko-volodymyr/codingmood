from django import forms

from .models import Repository


class RepositoryForm(forms.ModelForm):
    start_date = forms.DateTimeField()
    end_date = forms.DateTimeField()

    class Meta:
        model = Repository
        fields = ('url',)
