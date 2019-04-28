FROM python:3.7.3-alpine
MAINTAINER gkapfham@allegheny.edu

ENV APP_DIR /quizagator

# create and use the quizagator directory
WORKDIR ${APP_DIR}

# Copy the current folder to /quizagator in the image
# This should include Pipfile.lock
COPY . ${APP_DIR}

# install pipenv and dependencies into the image's system python
# (Don't use pipenv run to run things)
RUN set -ex && pip install pipenv && pipenv install --deploy --system

EXPOSE 80

# the start command will run the production server
CMD ["gunicorn", "--workers", "3", "--access-logfile", "-", "--bind", "0.0.0.0:80", "application.wsgi:app"]
