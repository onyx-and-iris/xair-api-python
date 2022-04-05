from setuptools import setup

setup(
  name='mair_remote',
  version='0.1',
  description='MAIR Remote Python API',
  packages=['mair'],
  install_requires=[
    'python-osc'
  ],
  extras_require={
    'development': [
      'nose',
      'randomize',
      'parameterized'
    ]
  }
)
