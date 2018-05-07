#from distutils.core import setup
from setuptools import setup
setup(
  name = 'clara',
  packages = ['clara','clara/utils'],
  package_data={'clara/utils':['*']},
  scripts=['bin/clara'],
  version = '1.1.1',
  description = 'Conversational chit-chat utility agent',
  author = 'Noah Huber-Feely',
  author_email = 'nhuberfeely@gmail.com',
  url = 'https://github.com/huberf/clara-pip', # use the URL to the github repo
  download_url = 'https://github.com/huberf/clara-pip/archive/1.1.1.tar.gz',
  keywords = ['clara', 'chat'], # arbitrary keywords
  classifiers = [],
)
