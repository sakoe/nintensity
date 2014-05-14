from setuptools import setup, find_packages

import os

setup(
   name='nintensity',
   version='0.0.1',
   author='Nathan S., Gary P., Sako E.',
   author_email='spe@i-sako.com',
   packages=find_packages(),
   url='http://pypi.python.org/pypi/nintensity/',
   license='LICENSE.txt',
   description='A Django-based project that tracks fitness metrics for individuals and teams',
   long_description=open('README.md').read(),
   install_requires=[
       "Django == 1.6.2",
       "pytest",
       "Jinja2==2.7.2",
       "MarkupSafe==0.19",
       "Pygments==1.6",
       "South==0.8.4",
       "Sphinx==1.2.2",
       "argparse==1.2.1",
       "django-registration==1.0",
       "docutils==0.11",
       "psycopg2==2.5.2",
       "python-dateutil==2.2",
       "pytz==2014.2",
       "six==1.6.1",
       "vobject==0.8.1c",
       "wsgiref==0.1.2",
   ],
)
