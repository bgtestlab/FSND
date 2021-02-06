import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode
DEBUG = True

# Connect to the database
DATABASE_NAME = 'fyyur'
#SQLALCHEMY_DATABASE_URI = 'postgres://udacity@localhost:5432/fyyur'
SQLALCHEMY_DATABASE_URI = 'postgres://{}/{}'.format('localhost:5432', DATABASE_NAME)

# Suppress warnings
SQLALCHEMY_TRACK_MODIFICATIONS = False