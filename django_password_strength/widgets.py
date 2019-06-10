from django.forms import PasswordInput
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _


class PasswordStrengthInput(PasswordInput):
    """
    Form widget to show the user how strong his/her password is.
    """

    def render(self, name, value, attrs=None):
        try:
            self.attrs['class'] = '%s password_strength'.strip() % self.attrs['class']
        except KeyError:
            self.attrs['class'] = 'password_strength'

        strength_markup = render_to_string("password_strength/progressbar.html",
                                           context=attrs)

        return mark_safe( super(PasswordInput, self).render(name, value, attrs) + strength_markup)

    class Media:
        js = (
            'django_password_strength/js/zxcvbn-async.js',
            'django_password_strength/js/password_strength.js',
        )


class PasswordConfirmationInput(PasswordInput):
    """
    Form widget to confirm the users password by letting him/her type it again.
    """

    def __init__(self, confirm_with=None, attrs=None, render_value=False):
        super(PasswordConfirmationInput, self).__init__(attrs, render_value)
        self.confirm_with=confirm_with

    def render(self, name, value, attrs=None):
        if self.confirm_with:
            self.attrs['data-confirm-with'] = 'id_%s' % self.confirm_with

        confirmation_markup = """
        <div style="margin-top: 10px;" class="hidden password_strength_info">
            <p class="text-muted">
                <span class="label label-danger">
                    %s
                </span>
                <span style="margin-left:5px;">%s</span>
            </p>
        </div>
        """ % (_('Warning'), _('Your passwords don\'t match.'))

        try:
            self.attrs['class'] = '%s password_confirmation'.strip() % self.attrs['class']
        except KeyError:
            self.attrs['class'] = 'password_confirmation'

        return mark_safe( super(PasswordInput, self).render(name, value, attrs) + confirmation_markup )
