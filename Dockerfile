FROM python:3.9-alpine AS BUILD_IMAGE

#RUN ls -la / &&  ls -la /srv && mkdir /srv
WORKDIR /srv
COPY ["Pipfile", "./"]

# the package.json file is automatically created, Getting people
# who are creating an SMK app may not have the skills to properly
# edit the file so that http-server is defined as a devdependency
# so using the uninstall as a fallback.

# apk add postgresql-dev gcc python3-dev musl-dev
# WORKING TO HERE
RUN apk add build-base postgresql-dev gcc python3-dev musl-dev; pip install pipenv; pipenv install





# FROM python:3.9-alpine
# ENV LANG C.UTF-8

# COPY app/app/* /app/
# COPY Pipfile Pipfile
# COPY Pipfile.lock Pipfile.lock

# RUN pip install pipenv; pipenv install --system --deploy --ignore-pipfile
# ENV PYTHONPATH='/usr/local/lib/python3.6:/usr/local/lib/python3.6/site-packages:/usr/local/bin'
# ENTRYPOINT ["uvicorn", "app.main:app"]
