from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.core.files.images import get_image_dimensions
from .models import *
import re

class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'username','email',)

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['phone'].required = True
        self.fields['password1'].required = False
        self.fields['password2'].required = False

    def clean_email(self):
        email  = self.cleaned_data['email']
        username = self.cleaned_data['username']
        if email and User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError(u'This email address is already registered.')
        return email
