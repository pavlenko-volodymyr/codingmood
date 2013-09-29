from django import forms
from django.core.validators import URLValidator

from .models import Repository


class RepositoryForm(forms.ModelForm):
    start_date = forms.DateField(required=False, widget=forms.widgets.TextInput(attrs={'class': 'form-control input-sm',
                                                                                'placeholder': 'DD/MM/YYYY'}))
    end_date = forms.DateField(required=False, widget=forms.widgets.TextInput(attrs={'class': 'form-control input-sm',
                                                                              'placeholder': 'DD/MM/YYYY'}))

    class Meta:
        model = Repository
        fields = ('url',)
        widgets = {
            'url': forms.widgets.TextInput(attrs={'class': 'form-control input-sm',
                                                  'placeholder': ' https://github.com/user/reopsitory.git'}),
        }


    def clean_url(self):
        data = self.cleaned_data['url']
        if not data.endswith('.git'):
            raise forms.ValidationError("Please give us url fo clone, for e.x. https://github.com/user/reopsitory.git")
        return data