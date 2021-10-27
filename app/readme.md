# Python Setup

project is using pipenv.

To get started: `pipenv install`

Then to start a virtualenv, `pipenv shell`

Most of the code in this folder is sample application using fast api.
Currently looking into wrapping database using datatrucker instead of
fastapi.  Keeping sample code here for now in case come back to the
fastapi approach.

# Data loading

## load.py

This script can be used to load the sample data into a sample database.
Load script uses sqlalchemy so same script should be able to be used to
load to whatever database is supported by the sqlalchemy orm.

## TODO

* modify the script to pull dump files down from object storage and then load
* configure as a cronjob in helm chart
* add MD5's or SHA1's on data files so only load if data has changed.

