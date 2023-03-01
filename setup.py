from distutils.core import setup

setup(name='nwslpy',
      version='0.0.0.4',
      description='Python wrapper around the nwslR library',
      packages=['nwslpy'],
      requires=[
          "pandas",
      ])
