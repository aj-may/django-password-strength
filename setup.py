from setuptools import setup, find_packages

setup(
    name = "django-password-strength",
    version = "1.0.0",
    packages = find_packages(),
    install_requires = ['django>=1.5'],
    author = "A.J. May",
    author_email = "aj7may@gmail.com",
    description = "This package contains an extention of the Django password widget including a password strength meter and crack time powered by zxcvbn.",
    license = "Creative Commons Attribution-ShareAlike 4.0 International License",
    keywords = "password meter zxcvbn strength security django",
    url = "http://thegoods.aj7may.com/django-password-strength",
    zip_safe = False,
    package_data = {
        'django_password_strength': ['static/js/*'],
    },
)