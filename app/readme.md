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

# running the app

## configure the following environment variables

* POSTGRESQL_PASSWORD
* POSTGRESQL_DATABASE
* POSTGRESQL_USER

(can get these values from the secret: site-db-secrets)

**todo: define the data load process from s3 so local env using a sqllite db would also work**

## port-forward the database pod from openshift

```
oc get pods
# pod you want is something like site-postgres-*
oc port-forward <db pod> 5432:5432
```

## Run the app:

```
cd app
uvicorn app.main:app
```
view the api swagger doc @ http://127.0.0.1:8000

Some of the end points are likely not necessary.  The main one that delivers
all the data required for a BCOnline Contaminated sites detailed report is:
`/pinpid/{pidno}/all_report`

A demo pin/pid that can be used against the `all_report` end point: 8006148
or query the `/pinpid` to get all the pinpids and then list one and submit to
the `all_report` end point.
