from registration.forms import RegistrationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _


class ExtendedRegistrationForm(RegistrationForm):
    def clean_email(self):
        """
        Validate that email is not in use.
        """
        # normalize email
        email = self.cleaned_data['email'].strip().lower()

        is_user_exists = User.objects.filter(email=email).exists()

        if is_user_exists:
            raise forms.ValidationError(
                _("A user with that email address is already exists."))
        else:
            return email
