
from django.forms import PasswordInput
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
import enum


class PasswordStrengthInputSettings(object):

    def __init__(self, show_strength_message=True, strength_message_format=None, strength_bar_ui=None,
                 show_warning_message=False, show_suggestions=False, min_score=2, min_length=8, max_length=128):
        self.show_strength_message = show_strength_message
        self.show_warning_message = show_warning_message
        self.strength_bar_ui = strength_bar_ui or ProgressBarUI()
        self.show_suggestions = show_suggestions
        self.strength_message_format = strength_message_format or \
            "This password would take <em class='password_strength_time'></em> to crack."
        self.min_score = min_score
        self.min_length = min_length
        self.max_length = max_length


class PasswordStrengthInput(PasswordInput):
    """
    Form widget to show the user how strong his/her password is.
    """

    def __init__(self, settings=None, *args, **kwargs):
        """
        Args:
            settings (PasswordStrengthInputSettings): The settings for showing the message.
        """
        super(PasswordStrengthInput, self).__init__(*args, **kwargs)
        self.settings = settings or PasswordStrengthInputSettings()

    def render(self, name, value, attrs=None):

        strength_message_markup = """
            <p class="password_strength_info password_info_message_text hidden">
                <span class="label label-info">
                    %s
                </span>
                <span class="text-muted" style="margin-left:5px;">
                    %s
                </span>
            </p>
        """ % (_('Info'), _(self.settings.strength_message_format))

        warning_message_markup = """
            <p class="password_warning_info password_info_label hidden">
                <span class="label label-danger">
                    %s
                </span>
                <span class="text-muted" style="margin-left:5px;">
                    %s
                </span>
            </p>
        """ % (_('Warning'), _('<span class="password_warning_message"></span>'))

        suggestions_markup = """
            <ul class="password_suggestions hidden">
                <li class="password_suggestion">
                    <div class="password_info_label">
                        <span class="label label-info">
                            Suggestion
                        </span>
                        <span class="suggestion_text text-muted" style="margin-left:5px;">
                        </span>
                    </div>
                </li>
            </ul>
        """

        markup = """<div id='zxcvbn_score_info' data-min-score='%s' data-min-length='%s' data-max-length='%s'>""" % (
            self.settings.min_score, self.settings.min_length, self.settings.max_length)
        if self.settings.strength_bar_ui is not None:
            markup += self.settings.strength_bar_ui.get_html()
        if self.settings.show_strength_message:
            markup += strength_message_markup
        if self.settings.show_warning_message:
            markup += warning_message_markup
        if self.settings.show_suggestions:
            markup += suggestions_markup
        markup += """</div>"""
        
        try:
            self.attrs['class'] = '%s password_strength'.strip() % self.attrs['class']
        except KeyError:
            self.attrs['class'] = 'password_strength'

        if not self.render_value:  # Respect the base classes render_value property, since we're overriding render.
            value = None

        return mark_safe(super(PasswordInput, self).render(name, value, attrs) + markup)

    class Media:
        js = (
            'django_password_strength/js/throttle_debounce.min.js',
            'django_password_strength/js/polyfill_lt_ie9.js',
            'django_password_strength/js/zxcvbn.js',
            'django_password_strength/js/password_strength.js',
        )


class PasswordConfirmationInput(PasswordInput):
    """
    Form widget to confirm the users password by letting him/her type it again.
    """

    def __init__(self, confirm_with=None, attrs=None, render_value=False):
        super(PasswordConfirmationInput, self).__init__(attrs, render_value)
        self.confirm_with = confirm_with

    def render(self, name, value, attrs=None):
        if self.confirm_with:
            self.attrs['data-confirm-with'] = 'id_%s' % self.confirm_with

        confirmation_markup = """
        <div style="margin-top: 3px;" class="hidden password_strength_info">
            <p class="text-muted">
                <span class="label label-danger">
                    %s
                </span>
                <span class="text-muted" style="margin-left:5px;">%s</span>
            </p>
        </div>
        """ % (_('Warning'), _('Your passwords don\'t match.'))

        try:
            self.attrs['class'] = '%s password_confirmation'.strip() % self.attrs['class']
        except KeyError:
            self.attrs['class'] = 'password_confirmation'

        if not self.render_value:  # Respect the base classes render_value property, since we're overriding render.
            value = None

        return mark_safe(super(PasswordInput, self).render(name, value, attrs) + confirmation_markup)


class ProgressBarUI(object):

    class Styles(enum.Enum):
        Bootstrap = 0,
        jQueryUI = 1,

    def __init__(self, style=Styles.Bootstrap, height=None, width=None, rounded_corners=True):
        self.style = style
        self.height = height
        self.width = width
        self.rounded_corners = rounded_corners

    def get_html(self):
        if self.style == self.Styles.Bootstrap:
            return """
                <div %s class="progress">
                    <div class="progress-bar progress-bar-warning password_strength_bar" role="progressbar"
                        aria-valuenow="0" aria-valuemin="0" aria-valuemax="5" style="width: 0%%;"></div>
                </div>
            """ % self.get_style_tag()
        elif self.style == self.Styles.jQueryUI:
            return """
                <div %s class="jquery_ui_progress_bar"></div>
            """ % self.get_style_tag()

    def get_style_tag(self):
        style_html = ""
        if self.height or self.width or self.rounded_corners:
            style_html += "style='"
            if self.height:
                style_html += "height:%s;" % self.height
            if self.width:
                style_html += "width:%s;" % self.width
            if not self.rounded_corners:
                style_html += "border-radius:0px;"
            style_html += "'"
        return style_html
