#from distutils.core import setup
from setuptools import setup
setup(
  name = 'clara',
  packages = ['clara','clara/utils'],
  package_data={'clara/utils':['*']},
  version = '1.0.1',
  description = 'Conversational chit-chat utility agent',
  author = 'Noah Huber-Feely',
  author_email = 'nhuberfeely@gmail.com',
  url = 'https://github.com/huberf/clara-pip', # use the URL to the github repo
  download_url = 'https://github.com/huberf/clara-pip/archive/1.0.0.tar.gz', # I'll explain this in a second
  keywords = ['clara', 'chat'], # arbitrary keywords
  classifiers = [],
)
