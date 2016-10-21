from django import forms
from django.utils.translation import ugettext_lazy as _

from countries.models import Country
from .models import Profile


def _clean_country(country_code):
    """Returns Country object for a `country_code`.
    If no country found a ValidationError is raised.
    """
    try:
        country = Country.objects.get(code=country_code)
    except Country.DoesNotExist:
        raise forms.ValidationError('No such country')
    return country


class SearchForm(forms.Form):
    """Journey Profile Search Form
    """
    src_country = forms.CharField(label='Source Country',
                                  widget=forms.HiddenInput)
    dest_country = forms.CharField(label='Destination Country',
                                   widget=forms.HiddenInput)
    departure_date = forms.DateField(
        label='Departure Date',
        widget=forms.TextInput(
            attrs={'placeholder': 'Probable departure date'}))

    def clean_src_country(self):
        country_code = self.cleaned_data.get('src_country')
        return _clean_country(country_code)

    def clean_dest_country(self):
        country_code = self.cleaned_data.get('dest_country')
        return _clean_country(country_code)


class CreationForm(forms.ModelForm):
    """Journey Profile Creation Form
    """
    src_country = forms.CharField(label='Source Country',
                                  widget=forms.HiddenInput)
    dest_country = forms.CharField(label='Destination Country',
                                   widget=forms.HiddenInput)

    class Meta:
        model = Profile
        fields = ('range_start',
                  'range_end', )
        labels = {
            'range_start': _('Range Start'),
            'range_end': _('Range End'),
        }

    def clean_src_country(self):
        country_code = self.cleaned_data.get('src_country')
        return _clean_country(country_code)

    def clean_dest_country(self):
        country_code = self.cleaned_data.get('dest_country')
        return _clean_country(country_code)

    def save(self, commit=True):
        profile = super(CreationForm, self).save(commit=False)
        profile.src_country = self.clean_src_country()
        profile.dest_country = self.clean_dest_country()
        if commit:
            profile.save()
        return profile
