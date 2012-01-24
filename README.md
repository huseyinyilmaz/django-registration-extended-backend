django-registration extended backend
====================================

This is a django-registration backend that have some diffirences from default registration backend.

* Users can send multiple activation from same email. When user is activated from one of them, we create a user from that activation and invalidate the rest.
* E-mail normalization during activation process. We lovercase email addresses, and make sure that we do not get any invalid characters in username.
