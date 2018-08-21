from setuptools import setup

setup(name='loacore',
      version='0.1',
      url='https://github.com/PaulBreugnot/Loacore',
      author="Paul Breugnot",
      author_email='paul.breugnot@etu.emse.fr',
      description="Language and Opinion Analyzer For Comments and Reviews",
      # packages=find_packages(exclude=['test', 'results', 'resources']),
      packages=[''],
      package_data={'': ['data', 'docs']},
      long_description=open('README.md').read(),
      setup_requires=['PyFreelingApi', 'nltk', 'matplotlib', 'PrettyTable'])
