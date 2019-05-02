"""Run this file to run the development server"""

import argparse

from application import appfactory
# creates app for flask
app = appfactory.create_app()
# sets secret key to "dev"
app.secret_key = "dev"
app.config["DATABASE"] = "data/quizagator.db"
# parser to debug arguments and validate user input
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

args = parser.parse_args()

app.debug = args.debug
app.run(args.host, args.port)
