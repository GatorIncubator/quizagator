FROM python:3.7.3-alpine
MAINTAINER gkapfham@allegheny.edu

ENV APP_DIR /quizagator/

# create and use the quizagator directory
WORKDIR ${APP_DIR}

# copy over the pipfile to set up the environment
COPY Pipfile Pipfile.lock ${APP_DIR}

# install pipenv and dependencies into the image's system python
# (Don't use pipenv run to run things)
RUN set -ex && pip install pipenv && pipenv install --deploy --system

# Copy the current folder to /quizagator in the image
# This should include Pipfile.lock
COPY . ${APP_DIR}

EXPOSE 80

# the start command will run the production server
CMD ["gunicorn", "--workers", "3", "--access-logfile", "-", "--bind", "0.0.0.0:80", "application.wsgi:app"]
