"""macdev — macOS local dev server management CLI."""
import click

from .nginx import nginx
from .php import php
from .ssl import ssl
from .vhost import vhost


@click.group()
@click.version_option(package_name="macdev")
def cli():
    """macdev — manage nginx vhosts, PHP versions and SSL certs on macOS (Homebrew)."""


cli.add_command(vhost)
cli.add_command(php)
cli.add_command(ssl)
cli.add_command(nginx)
