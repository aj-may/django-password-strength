from setuptools import setup, find_packages

setup(
    name='django-password-strength',
    version='1.1.1',
    url='http://thegoods.aj7may.com/django-password-strength',
    author='A.J. May',
    author_email='aj7may@gmail.com',
    description='This package contains an extention of the Django password widget including a password strength meter and crack time powered by zxcvbn.',
    keywords='password meter zxcvbn strength security django',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
