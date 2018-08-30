from setuptools import setup, find_packages

setup(name='loacore',
      version='0.1.2',
      url='https://github.com/PaulBreugnot/Loacore',
      author="Paul Breugnot",
      author_email='paul.breugnot@etu.emse.fr',
      description="Language and Opinion Analyzer For Comments and Reviews",
      # packages=find_packages(exclude=['test', 'results', 'resources']),
      packages=find_packages(exclude=['test']),
      # package_dir={'': 'loacore'},
      package_data={'loacore': ['data/database/.gitignore',
                                'data/database/reviews.db',
                                'test/test_file.txt',
                                'docs/*',
                                'results/*',
                                'output/*']},
      long_description=open('README.md').read(),
      install_requires=['nltk', 'matplotlib', 'PrettyTable']
      )
