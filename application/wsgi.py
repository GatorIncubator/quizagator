"""WSGI entry point for use with gunicorn in production"""
import os

from application import appfactory

app = appfactory.create_app()
app.secret_key = os.environ["FLASK_SECRET_KEY"]
app.config["DATABASE"] = "/data/quizagator.db"
