import password_strength as pwd
from django.core.validators import BaseValidator
from django.utils.translation import gettext, ungettext_lazy


class PolicyBaseValidator(BaseValidator):
    def js_requirement(self):
        return {}


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
        return value < limit_value

    def js_requirement(self):
        return {'minlength': {
            'minLength': self.limit_value,
            'text': gettext('be at least minLength characters long'),
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
        return value < limit_value

    def js_requirement(self):
        return {'containSpecialChars': {
            'minLength': self.limit_value,
            'text': gettext('Your input should contain at least minLength special character'),
            'regex': "([^!%&@#$^*?_~])",
            'regex_flags': 'g'
        }}


class PolicyContainLowercaseValidator(PolicyBaseValidator):
    message = ungettext_lazy(
        'Your input should contain at least %(limit_value)d lower case character (it has %(show_value)d).',
        'Your input should contain at least %(limit_value)d lower case characters (it has %(show_value)d).',
        'limit_value')
    code = 'lowercase_length'

    def __init__(self, *args, **kwargs):
        super(PolicyContainLowercaseValidator, self).__init__(*args, **kwargs)

    @staticmethod
    def clean(value):
        return pwd.PasswordStats(value).letters_lowercase

    def compare(self, value, limit_value):
        return value < limit_value

    def js_requirement(self):
        return {'containLowercase': {
            'minLength': self.limit_value,
            'text': gettext("Your input should contain at least minLength lower case character")
        }}


class PolicyContainUppercaseValidator(PolicyBaseValidator):
    message = ungettext_lazy(
        'Your input should contain at least %(limit_value)d upper case character (it has %(show_value)d).',
        'Your input should contain at least %(limit_value)d upper case characters (it has %(show_value)d).'
        'limit_value')
    code = 'uppercase_length'

    def __init__(self, *args, **kwargs):
        super(PolicyContainUppercaseValidator, self).__init__(*args, **kwargs)

    @staticmethod
    def clean(value):
        return pwd.PasswordStats(value).letters_uppercase

    def compare(self, value, limit_value):
        return value < limit_value

    def js_requirement(self):
        return {'containUppercase': {
            'minLength': self.limit_value,
            'text': gettext("Your input should contain at least minLength upper case character")
        }}


class PolicyContainNumbersValidator(PolicyBaseValidator):
    message = ungettext_lazy(
        'Your input should contain at least %(limit_value)d number (it has %(show_value)d).',
        'Your input should contain at least %(limit_value)d numbers (it has %(show_value)d).',
        'limit_value')
    code = 'number_length'

    def __init__(self, *args, **kwargs):
        super(PolicyContainNumbersValidator, self).__init__(*args, **kwargs)

    @staticmethod
    def clean(value):
        return pwd.PasswordStats(value).numbers

    def compare(self, value, limit_value):
        return value < limit_value

    def js_requirement(self):
        return {'containNumbers': {
            'minLength': self.limit_value,
            'text': gettext("Your input should contain at least minLength number")
        }}
