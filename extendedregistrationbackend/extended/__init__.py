from django.conf import settings
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site

from registration import signals
from extendedregistrationbackend.forms import ExtendedRegistrationForm
from registration.models import RegistrationProfile
from registration.backends.default import DefaultBackend

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from warnings import warn


def normalize_email(email):
    return email.strip().lower()


class ExtendedBackend(DefaultBackend):
    def register(self, request, **kwargs):
        """
        Given a username, email address and password, register a new
        user account, which will initially be inactive.

        Along with the new ``User`` object, a new
        ``registration.models.RegistrationProfile`` will be created,
        tied to that ``User``, containing the activation key which
        will be used for this account.

        An email will be sent to the supplied email address; this
        email should contain an activation link. The email will be
        rendered using two templates. See the documentation for
        ``RegistrationProfile.send_activation_email()`` for
        information about these templates and the contexts provided to
        them.

        After the ``User`` and ``RegistrationProfile`` are created and
        the activation email is sent, the signal
        ``registration.signals.user_registered`` will be sent, with
        the new ``User`` as the keyword argument ``user`` and the
        class of this backend as the sender.

        """
        username, email, password = kwargs['username'], kwargs['email'], kwargs['password1']
        # normalize email
        normalization_func = getattr(settings,'EMAIL_NORMALIZATION_FUNCTION',normalize_email)
        email = normalization_func(email)

        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
        # Create user but do not send activation email
        new_user = RegistrationProfile.objects.\
            create_inactive_user(username, email,
                                 password, site,
                                 False)
        profile = new_user.registrationprofile_set.all()[0]

        self.send_activation_email(site, profile)
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user

    def get_form_class(self, request):
        """
        Return the default form class used for user registration.

        """
        return ExtendedRegistrationForm

    def send_activation_email(self, site, profile):
        user = profile.user
        ctx_dict = {'activation_key': profile.activation_key,
                    'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                    'site': site,
                    'email': user.email}

        # Email subject *must not* contain newlines
        subject = ''.join(\
            render_to_string('registration/activation_email_subject.txt',
                             ctx_dict).splitlines())

        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = user.email

        text_content = render_to_string('registration/activation_email.txt',
                                        ctx_dict)
        try:
            html_content = render_to_string('registration/activation_email.html',
                                            ctx_dict)
        except:
            # If any error occurs during html preperation do not add html content
            # This is here to make sure when we switch from default backend to extended
            # we do not get any missing here
            html_content = None
            # XXX we should not catch all exception for this
            warn('registration/activation_email.html template cannot be rendered. Make sure you have it to send HTML messages. Will send email as TXT')

        msg = EmailMultiAlternatives(subject,
                                     text_content,
                                     from_email,
                                     [to_email])
        if html_content:
            msg.attach_alternative(html_content, "text/html")

        msg.send()

