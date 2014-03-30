from distutils.core import setup

setup(
   name='Nintensity',
   version='0.0.1',
   author='Nathan S., Gary P., Sako E.',
   author_email='spe@i-sako.com',
   packages=['nintensity', 'nintensity.test'],
   scripts=['bin/script1','bin/script2'],
   url='http://pypi.python.org/pypi/nintensity/',
   license='LICENSE.txt',
   description='A Django-based project that tracks fitness metrics for individuals and teams',
   long_description=open('README.txt').read(),
   install_requires=[
       "Django >= 1.6.2",
       "pytest",
   ],
)