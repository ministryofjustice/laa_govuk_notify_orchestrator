#!/usr/bin/env python
import uvicorn
import logging
import argparse
from app.config import DEFAULT_HOST, DEFAULT_PORT

logger = logging.getLogger("uvicorn")

parser = argparse.ArgumentParser(description='Manages the GOV.UK Notify"\
                                "Orchestration API')

parser.add_argument("command", choices=["", "runserver", "test", "tests"], nargs='?')

parser.add_argument('--host', type=str,
                    help=f"(Optional) Sets which host to run the API on, "
                         f"defaults to {DEFAULT_HOST}")

parser.add_argument('--port', type=int,
                    help=f"(Optional) Sets which port to run the API on, "
                         f"defaults to {DEFAULT_PORT}.")

parser.add_argument('--log-level', type=int,
                    help="(Optional) Sets which log level to display, "
                         "defaults to 'debug'.")


def get_uvicorn_config(host=None, port=None, log_level=None):
    config = uvicorn.Config("app:notify_orchestrator_api")
    config.host = DEFAULT_HOST if host is None else host
    config.port = DEFAULT_PORT if port is None else port
    config.log_level = 'debug' if log_level is None else log_level
    return config


if __name__ == "__main__":
    args = parser.parse_args()
    config = get_uvicorn_config(args.host, args.port, args.log_level)
    server = uvicorn.Server(config)
    server.run()
