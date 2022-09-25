from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'siamese-optimizer',
  packages = [
    'siamese',
    'siamese.models'
  ],
  version = '0.0.1',
  license = 'MIT',
  description = 'A Python package for manufacturing and assembly lines simulation and optimization.',
  long_description = long_description,
  long_description_content_type = 'text/markdown', 
  author = 'Gustavo Furtado',
  author_email = 'gustavofurtado2@gmail.com',
  url = 'https://github.com/GusFurtado/siamese-optimizer',
  download_url = 'https://github.com/GusFurtado/siamese-optimizer/archive/0.0.1.tar.gz',

  keywords = [
    'python',
    'simulation',
    'networkx',
    'manufacturing',
    'industry',
    'simpy',
    'assembly-line',
    'production-line',
    'line-engineering',
    'manufacturing-line'
  ],

  install_requires = [
    'networkx',
    'numpy',
    'plotly',
    'simpy'
  ],

  classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Manufacturing',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Natural Language :: Portuguese (Brazilian)',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6'
  ]
)