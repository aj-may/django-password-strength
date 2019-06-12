from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.utils.translation import ungettext_lazy
from password_strength import PasswordPolicy


class PolicyBaseValidator(BaseValidator):
    def __call__(self, value):
        value_cleaned = self.clean(value)
        params = {'limit_value': self.limit_value, 'show_value': value_cleaned, 'value': value}
        if self.compare(value, self.limit_value):
            raise ValidationError(self.message, code=self.code, params=params)


class PolicyMinLengthValidator(PolicyBaseValidator):
    message = ungettext_lazy(
        'Ensure this value has at least %(limit_value)d character (it has %(show_value)d).',
        'Ensure this value has at least %(limit_value)d characters (it has %(show_value)d).',
        'limit_value')
    code = 'min_value'

    def __init__(self, *args, **kwargs):
        super(PolicyMinLengthValidator, self).__init__(*args, **kwargs)

    @staticmethod
    def clean(value):
        return len(value)

    def compare(self, value, limit_value):
        return PasswordPolicy.from_names(length=limit_value).test(value)
