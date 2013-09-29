from django import forms
from django.core.validators import URLValidator

from .models import Repository


class RepositoryForm(forms.ModelForm):
    start_date = forms.DateTimeField(required=False)
    end_date = forms.DateTimeField(required=False)

    class Meta:
        model = Repository
        fields = ('url',)

    def clean_url(self):
        data = self.cleaned_data['url']
        if not data.endswith('.git'):
            raise forms.ValidationError("Please give us url fo clone, for e.x. https://github.com/user/reopsitory.git")
        return data