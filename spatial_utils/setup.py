import os
import sys

from setuptools import setup, find_packages
here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'readme')).read()

requires = [
    'Shapely',
    'rpy2'
    ]

setup(name='SpatialUtils',
      version='0.0',
      description='Spatial Utilties',
      long_description = README,
      classifiers=[
        "Programming Language :: Python"
        ],
      author='',
      author_email='',
      url='',
      keywords='spatial',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='tests',
      install_requires = requires
      )
