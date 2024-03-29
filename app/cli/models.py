from app.odoo.odoo import OdooClient
from rich.console import Console
from rich.table import Table

def output_models(models):
    table = Table(title="Models", show_lines=True)
    table.add_column("Name", justify="left", style="cyan")
    table.add_column("Model ID", justify="left")

    for model in models:
        table.add_row(model.name, model.model)

    console = Console()
    console.print(table)

def output_users(users):
    table = Table(title="Users", show_lines=True)
    table.add_column("Name", justify="left", style="cyan")
    table.add_column("User ID", justify="left")
    table.add_column("Login (Email)", justify="left")

    for user in users:
        table.add_row(user.name, str(user.id), user.login)

    console = Console()
    console.print(table)
