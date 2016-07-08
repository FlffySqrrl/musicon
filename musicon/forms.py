from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.forms.models import BaseInlineFormSet

from models import *

# ------------------------------------------------------------------------------
# ENTITY FORMS
# ------------------------------------------------------------------------------

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['event_name']

class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = ['lat', 'lng']

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

# ------------------------------------------------------------------------------
# USER FORMS
# ------------------------------------------------------------------------------

class RequiredInlineFormSet(BaseInlineFormSet):
    '''
    Generates a required in-line form.
    '''
    def _construct_form(self, i, **kwargs):
        '''
        Overrides the method to set empty_permitted to False.
        '''
        form = super(RequiredInlineFormSet, self)._construct_form(i, **kwargs)
        form.empty_permitted = False
        return form
