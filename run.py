"""Run this file to run the development server"""

import argparse
import os

from application import appfactory

app = appfactory.create_app()

app.secret_key = "dev"
app.config["DATABASE"] = "data/quizagator.db"

parser = argparse.ArgumentParser()
parser.add_argument(
    "-d, --debug",
    dest="debug",
    default=False,
    action="store_true",
    help="set debug mode",
)
parser.add_argument(
    "--port",
    dest="port",
    type=int,
    default=5000,
    help="port to listen on (default: 5000)",
)
parser.add_argument(
    "--host",
    dest="host",
    type=str,
    default="0.0.0.0",
    help="host to serve from (default: 0.0.0.0)",
)

parser.add_argument(
    "--clear",
    dest="clear",
    default=False,
    action="store_true",
    help="clear the database",
)

args = parser.parse_args()

if args.clear:
    if os.path.isfile(app.config["DATABASE"]):
        os.remove(app.config["DATABASE"])
    with app.app_context():
        from application import db_connect

        db_connect.db_init()
    print("Reinitialized database!")
else:
    app.debug = args.debug
    app.run(args.host, args.port)
