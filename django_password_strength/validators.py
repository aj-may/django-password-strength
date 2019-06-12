from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.utils.translation import ungettext_lazy
import password_strength as pwd


class PolicyBaseValidator(BaseValidator):
    def js_requirement(self):
        return {}

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
        return pwd.PasswordStats(value).length

    def compare(self, value, limit_value):
        return pwd.PasswordPolicy.from_names(length=limit_value).test(value)

    def js_requirement(self):
        return {'minlength': {
            'minLength': self.limit_value
        }}


class PolicyContainSpecialCharsValidator(PolicyBaseValidator):
    message = ungettext_lazy(
        'Your input should contain at least %(limit_value)d special character (it has %(show_value)d).',
        'Your input should contain at least %(limit_value)d special characters (it has %(show_value)d).',
        'limit_value')
    code = 'special_length'

    def __init__(self, *args, **kwargs):
        super(PolicyContainSpecialCharsValidator, self).__init__(*args, **kwargs)

    @staticmethod
    def clean(value):
        return pwd.PasswordStats(value).special_characters

    def compare(self, value, limit_value):
        return pwd.PasswordPolicy.from_names(special=limit_value).test(value)

    def js_requirement(self):
        return {'containSpecialChars': {
            'minLength': self.limit_value
        }}
