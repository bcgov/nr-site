FROM python:3.9-alpine AS BUILD_IMAGE
WORKDIR /srv
COPY ["Pipfile", "Pipfile.lock", "./"]
RUN apk add build-base postgresql-dev gcc python3-dev musl-dev;\
    python -m pip install --upgrade pip;\
    pip install pipenv
RUN pipenv lock --keep-outdated --requirements > requirements.txt;\
    mkdir /install;\
    pip install --prefix=/install -r requirements.txt

FROM python:3.9-alpine
RUN apk add postgresql-libs
COPY --from=BUILD_IMAGE /install /usr/local
WORKDIR /srv
COPY ./app/app app/

ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]





# FROM python:3.9-alpine
# ENV LANG C.UTF-8

# COPY app/app/* /app/
# COPY Pipfile Pipfile
# COPY Pipfile.lock Pipfile.lock

# RUN pip install pipenv; pipenv install --system --deploy --ignore-pipfile
# ENV PYTHONPATH='/usr/local/lib/python3.6:/usr/local/lib/python3.6/site-packages:/usr/local/bin'
# ENTRYPOINT ["uvicorn", "app.main:app"]
