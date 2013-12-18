# Django Password Strength

## A Smarter Password Strength Meter

An extention of the Django password widget including a password strength meter and crack time powered by [zxcvbn](https://github.com/lowe/zxcvbn).

{<1>}![Empty Password](http://thegoods.aj7may.com/content/images/2013/Dec/Screen_Shot_2013_12_18_at_9_05_38_AM.png)

{<2>}![Weak Password](http://thegoods.aj7may.com/content/images/2013/Dec/Screen_Shot_2013_12_18_at_9_06_05_AM.png)

{<3>}![Strong Password](http://thegoods.aj7may.com/content/images/2013/Dec/Screen_Shot_2013_12_18_at_9_06_32_AM.png)

### Install:
`> pip install django-password-strength`

### Usage:

* Add `django-password-strength` to the installed apps of your Django Project
* Instead of using the django `PasswordInput` widget use the `PasswordStrengthInput`
* Be sure to include the form's required media in the template. _ie._ `{{ form.media }}`
* For easiest integration also include [Twitter Bootstrap](http://getbootstrap.com/)

### Example:

_forms.py_

	from django import forms
	from django_password_strength.widgets import PasswordStrengthInput
    
    class SignupForm(forms.Form):
    	username = forms.CharField()
    	passphrase = forms.CharField(
        	widget=PasswordStrengthInput()
        )