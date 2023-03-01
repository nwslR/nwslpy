from distutils.core import setup

setup(name='nwslpy',
      version='1.0',
      description='Python wrapper around the nwslR library',
      packages=['nwslpy'],
      requires=[
          "rpy2",
          "pandas",
      ])
