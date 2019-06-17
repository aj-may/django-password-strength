from django.forms import PasswordInput
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
import django


class PasswordInputCompat(PasswordInput):

    def build_attrs(self, attrs, extra_attrs=None, **kwargs):
        if django.VERSION >= (1, 11):
            return super(PasswordInputCompat, self).build_attrs(
                attrs, extra_attrs=extra_attrs)
        else:
            return super(PasswordInputCompat, self).build_attrs(attrs, **kwargs)


class PasswordMutedInput(PasswordInputCompat):
    """Hide related infos"""

    class Media(object):
        js = (
            'django_password_strength/js/pass-requirements.js',
        )
        css = {
            'screen': ('django_password_strength/css/password-strength.css',)
        }

    def render(self, name, value, attrs=None, **kwargs):
        validators = self.attrs.pop('validators', [])
        validators_defaults = self.attrs.pop('validators_defaults', True)

        autocomplete = 'autocomplete'
        if autocomplete not in attrs:
            attrs[autocomplete] = 'new-password'

        html = super(PasswordInput, self).render(name, value, attrs, **kwargs)
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        # strength rules
        html += render_to_string("django_password_strength/widgets/strength-rules.txt",
                                 context={'attrs': final_attrs,
                                          'validators': validators,
                                          'validators_defaults': validators_defaults})
        return mark_safe(html)


class PasswordStrengthInput(PasswordInputCompat):
    """
    Form widget to show the user how strong his/her password is.
    """

    def render(self, name, value, attrs=None, **kwargs):
        validators = self.attrs.pop('validators', [])
        show_progressbar_info = self.attrs.pop('show_progressbar_info', True)
        validators_defaults = self.attrs.pop('validators_defaults', True)
        try:
            self.attrs['class'] = '%s password_strength'.strip() % self.attrs['class']
        except KeyError:
            self.attrs['class'] = 'password_strength'

        autocomplete = 'autocomplete'
        if autocomplete not in attrs:
            attrs[autocomplete] = 'new-password'

        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)

        # strength markup
        html = render_to_string("django_password_strength/widgets/progressbar.html",
                                context=final_attrs)
        html += super(PasswordInput, self).render(name, value, attrs, **kwargs)
        if show_progressbar_info:
            html += render_to_string("django_password_strength/widgets/progressbar-info.html",
                                     context=final_attrs)
        html += render_to_string("django_password_strength/widgets/strength-rules.txt",
                                 context={'attrs': final_attrs,
                                          'validators': validators,
                                          'validators_defaults': validators_defaults})
        return mark_safe(html)

    class Media(object):
        js = (
            'django_password_strength/js/zxcvbn.js',
            'django_password_strength/js/password_strength.js',
            'django_password_strength/js/pass-requirements.js',
        )
        css = {
            'screen': ('django_password_strength/css/password-strength.css',)
        }


class PasswordConfirmationInput(PasswordInputCompat):
    """
    Form widget to confirm the users password by letting him/her type it again.
    """

    def __init__(self, confirm_with=None, attrs=None, render_value=False):
        super(PasswordConfirmationInput, self).__init__(attrs, render_value)
        self.confirm_with = confirm_with

    def render(self, name, value, attrs=None, **kwargs):
        if self.confirm_with:
            self.attrs['data-confirm-with'] = 'id_%s' % self.confirm_with

        try:
            self.attrs['class'] = '%s password_confirmation'.strip() % self.attrs['class']
        except KeyError:
            self.attrs['class'] = 'password_confirmation'

        autocomplete = 'autocomplete'
        if autocomplete not in attrs:
            attrs[autocomplete] = 'new-password'

        confirmation_markup = render_to_string("django_password_strength/widgets/strength-info.html",
                                               context=attrs)
        return mark_safe(super(PasswordInput, self).render(name, value, attrs, **kwargs) + confirmation_markup)
