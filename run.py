"""Run this file to run the application"""

import argparse

from application import app

app.secret_key = "$JLmL!eCQXyajbdu2LCJ&Vwqs2JGagg3B&FRfexCmKBV"


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
