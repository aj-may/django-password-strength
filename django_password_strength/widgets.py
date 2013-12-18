from django.forms import PasswordInput
from django.utils.safestring import mark_safe

class PasswordStrengthInput(PasswordInput):
    def render(self, name, value, attrs=None):
        strength_markup = """
        <div style="margin-top: 10px;">
            <div class="progress" style="margin-bottom: 10px;">
                <div class="progress-bar progress-bar-warning" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="5" style="width: 0%" id="password_strength_bar"></div>
            </div>
            <p id="password_strength_info" class="text-muted"></p>
        </div>
        """

        self.attrs['class'] = '%s password_strength' % self.attrs['class']

        return mark_safe( super(PasswordInput, self).render(name, value) + strength_markup )

    class Media:
        js = (
            '//cdnjs.cloudflare.com/ajax/libs/zxcvbn/1.0/zxcvbn-async.js',
            'js/password_strength.js',
        )