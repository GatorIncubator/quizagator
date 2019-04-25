FROM python:3.7.3-alpine
MAINTAINER gkapfham@allegheny.edu

ENV APP_DIR /quizagator
ENV FLASK_PORT 5000

EXPOSE ${FLASK_PORT}

# create and use the quizagator directory
WORKDIR ${APP_DIR}

# Copy the current folder to /quizagator in the image
# This should include Pipfile.lock
COPY . ${APP_DIR}

# install pipenv and dependencies into the image's system python
# (Don't use pipenv run to run things)
RUN set -ex && pip install pipenv && pipenv install --deploy --system

# the start command will run the production server
CMD python run.py --host 0.0.0.0 --port ${FLASK_PORT}
