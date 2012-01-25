django-registration extended backend
====================================

This is a django-registration backend that have some diffirences from default registration backend.

* E-mail normalization during activation process. We lovercase email addresses, and make sure that we do not get any invalid characters in username.
* Sends emails in HTML format