import click
from app.cli.models import output_models

from app.odoo.odoo import OdooClient

## setup
odoo = OdooClient()

## commands
@click.group()
def cli():
    pass

@click.command("models")
def models():
    """Outputs Table of all Models in Odoo"""
    models = odoo.list_models()
    output_models(models)

cli.add_command(models)

if __name__=='__main__':
    cli()