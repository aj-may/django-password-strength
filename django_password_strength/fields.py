from django import forms

from django_password_strength.validators import (
    PolicyMinLengthValidator,
    PolicyBaseValidator,
    PolicyContainSpecialCharsValidator,
    PolicyContainLowercaseValidator,
    PolicyContainUppercaseValidator,
    PolicyContainNumbersValidator)
from django_password_strength.widgets import PasswordStrengthInput, PasswordConfirmationInput


class PasswordField(forms.CharField):
    """Password field"""

    widget = PasswordStrengthInput

    def __init__(self,
                 max_length=None,
                 min_length=None,
                 special_length=None,
                 lowercase_length=None,
                 uppercase_length=None,
                 numbers_length=None,
                 strip=True,
                 *args, **kwargs):
        super(PasswordField, self).__init__(max_length=max_length,
                                            min_length=None,
                                            strip=strip,
                                            *args, **kwargs)
        self.min_length = min_length
        self.special_length = special_length
        self.lowercase_length = lowercase_length
        self.uppercase_length = uppercase_length
        self.numbers_length = numbers_length

        if min_length is not None:
            self.validators.append(PolicyMinLengthValidator(int(min_length)))

        if special_length is not None:
            self.validators.append(PolicyContainSpecialCharsValidator(int(special_length)))

        if lowercase_length is not None:
            self.validators.append(PolicyContainLowercaseValidator(int(lowercase_length)))

        if uppercase_length is not None:
            self.validators.append(PolicyContainUppercaseValidator(int(uppercase_length)))

        if numbers_length is not None:
            self.validators.append(PolicyContainNumbersValidator(int(numbers_length)))

        # validators
        validators_attrs = self.widget_validators_attrs(self.widget)
        if validators_attrs and hasattr(self.widget, "attrs"):
            self.widget.attrs.update(validators_attrs)

    def widget_validators_attrs(self, widget):
        attrs = {'validators': []}
        for validator in self.validators:
            if isinstance(validator, PolicyBaseValidator):
                attrs['validators'].append(validator.js_requirement())
        return attrs


class PasswordConfirmationField(forms.CharField):
    """Password confirmation field"""

    widget = PasswordConfirmationInput

    def __init__(self, confirm_with=None, *args, **kwargs):
        self.confirm_with = confirm_with
        super(PasswordConfirmationField, self).__init__(*args, **kwargs)

    def widget_attrs(self, widget):
        attrs = super(PasswordConfirmationField, self).widget_attrs(widget)
        if self.confirm_with is not None:
            attrs['data-confirm-with'] = 'id_%s' % self.confirm_with
        return attrs
