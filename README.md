# Django Password Strength

An extension of the Django password widget including a password strength meter and crack time powered by [zxcvbn](https://github.com/lowe/zxcvbn).

![Empty Password](http://thegoods.aj7may.com/content/images/2013/Dec/Screen_Shot_2013_12_18_at_9_05_38_AM.png)

![Weak Password](http://thegoods.aj7may.com/content/images/2013/Dec/Screen_Shot_2013_12_18_at_9_06_05_AM.png)

![Strong Password](http://thegoods.aj7may.com/content/images/2013/Dec/Screen_Shot_2013_12_18_at_9_06_32_AM.png)

### Install:
`> pip install django-password-strength`

### Usage:

* Add `django_password_strength` to the installed apps of your Django Project
* Instead of using the django `PasswordInput` widget use the `PasswordStrengthInput`
* Be sure to include the form's required media in the template. _ie._ `{{ form.media }}`
* If you bundle your js you can use `django_password_strength/js/zxcvbn.js` or `django_password_strength/js/zxcvbn-async.js` and `django_password_strength/js/password_strength.js` instead
* For easiest integration also include [Twitter Bootstrap](http://getbootstrap.com/)

### Translations:

There are currently no translations already available, but all the text is translatable, you just have to translate it yourself.

For the javascript translations be sure to add the javascript translation catalog [provided by django](https://docs.djangoproject.com/en/1.7/topics/i18n/translation/#using-the-javascript-translation-catalog) or use something like [django-statici18n](https://github.com/zyegfryed/django-statici18n) for a static version of the catalog. If you don't want translations you don't have to add the catalog to your page.

### Example:

_forms.py_

    from django import forms
    from django_password_strength.widgets import PasswordStrengthInput, PasswordConfirmationInput
    
    class SignupForm(forms.Form):
        username = forms.CharField()
        passphrase = forms.CharField(
            widget=PasswordStrengthInput()
        )
        confirm_passphrase = forms.CharField(
            widget=PasswordConfirmationInput()
        )

### Example using multiple password fields:

_forms.py_

    from django import forms
    from django_password_strength.widgets import PasswordStrengthInput, PasswordConfirmationInput
    
    class SignupForm(forms.Form):
        username = forms.CharField()
        passphrase = forms.CharField(
            widget=PasswordStrengthInput()
        )
        confirm_passphrase = forms.CharField(
            widget=PasswordConfirmationInput(confirm_with='passphrase')
        )

        passphrase2 = forms.CharField(
            widget=PasswordStrengthInput()
        )
        confirm_passphrase2 = forms.CharField(
            widget=PasswordConfirmationInput(confirm_with='passphrase2')
        )
