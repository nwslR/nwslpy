from rpy2.robjects.packages import importr

# one-time execution to build & install the Cubist R package
utils= importr('utils')
utils.install_packages('devtools')
devtools = importr('devtools')
devtools.install_github('topepo/Cubist')

# if success you can then import the package
Cubist = importr('Cubist') 