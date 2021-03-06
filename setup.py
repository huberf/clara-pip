#from distutils.core import setup
from setuptools import setup
setup(
  name = 'clara',
  packages = ['clara','clara/utils'],
  install_requires=[
      'flask',
      'python-Levenshtein',
      'vaderSentiment',
  ],
  package_data={'clara/utils':['*']},
  scripts=['bin/clara'],
  version = '1.4.0',
  description = 'Conversational chit-chat utility agent',
  author = 'Noah Huber-Feely',
  author_email = 'nhuberfeely@gmail.com',
  url = 'https://github.com/huberf/clara-pip', # use the URL to the github repo
  download_url = 'https://github.com/huberf/clara-pip/archive/1.4.0.tar.gz',
  keywords = ['clara', 'chat'], # arbitrary keywords
  classifiers = [],
)
