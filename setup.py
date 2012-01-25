from setuptools import setup
from setuptools import find_packages

VERSION = '0.1.a1'
DESCRIPTION = 'Backend for django registration that sends email in HTML and does email normalization'

setup(
    name='django-registration-extended-backend',
    version=VERSION,
    description=DESCRIPTION,
    url='https://bitbucket.org/yilmazhuseyin/django-sslredirector',
    author='Huseyin Yilmaz',
    author_email='me@yilmazhuseyin.com',
    packages=find_packages(),
    include_package_data=True,
    license='GPLv3',
    keywords='django registration django-registration',
    install_requires=[
        'Django>=1.3',
    ]
)
