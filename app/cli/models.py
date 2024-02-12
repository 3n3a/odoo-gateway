
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
