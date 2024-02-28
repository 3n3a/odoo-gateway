import click
from app.cli.models import output_models, output_users

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

@click.command("users")
def users():
    """Outputs Table of all Users in Odoo"""
    users = odoo.list_users()
    output_users(users)


cli.add_command(models)
cli.add_command(users)

if __name__=='__main__':
    cli()