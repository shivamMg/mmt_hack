from django import forms
from django.utils.translation import ugettext_lazy as _

from countries.models import Country
from .models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation',
                                widget=forms.PasswordInput)
    country = forms.CharField(label='Country', widget=forms.HiddenInput)

    class Meta:
        model = User
        fields = ('username', 'email')
        labels = {
            'username': _('Username'),
            'email': _('Email'),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_country(self):
        country_code = self.cleaned_data.get('country')
        try:
            country = Country.objects.get(code=country_code)
        except Country.DoesNotExist:
            raise forms.ValidationError('No such country')
        return country

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.country = self.clean_country()
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    country = forms.CharField(label='Country', widget=forms.HiddenInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',)
        labels = {
            'username': _('Username'),
            'email': _('Email'),
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
        }

    def clean_country(self):
        country_code = self.cleaned_data.get('country')
        try:
            country = Country.objects.get(code=country_code)
        except Country.DoesNotExist:
            raise forms.ValidationError('No such country')
        return country

    def save(self, commit=True):
        user = super(UserChangeForm, self).save(commit=False)
        user.country = self.clean_country()
        if commit:
            user.save()
        return user
