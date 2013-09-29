from django import forms

from .models import Repository


class RepositoryForm(forms.ModelForm):
    start_date = forms.DateTimeField(required=False)
    end_date = forms.DateTimeField(required=False)

    class Meta:
        model = Repository
        fields = ('url',)
