from os import environ

import click
from flask import Flask

from pollux.auth import hash_pw
from pollux.blueprint.main import MAIN


def make_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("pollux.default_settings")
    if "POLLUX_SETTINGS" in environ:
        app.config.from_envvar("POLLUX_SETTINGS")
    app.register_blueprint(MAIN)

    @app.cli.command()
    @click.option(
        '--password', prompt=True, hide_input=True, confirmation_prompt=True
    )
    def hashpassword(password: str) -> None:
        """
        Creates a new password hash
        """
        hashed_pw = hash_pw(password)
        click.echo("Password Hash: %s" % hashed_pw)

    return app
