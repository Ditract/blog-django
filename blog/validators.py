from django.contrib.auth.password_validation import MinimumLengthValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class CustomMinimumLengthValidator(MinimumLengthValidator):
    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _('Esta contraseña es demasiado corta. Debe contener al menos %(min_length)d caracteres.'),
                code='password_too_short',
                params={'min_length': self.min_length},
            )