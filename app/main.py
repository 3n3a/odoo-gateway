from fastapi import BackgroundTasks, Request

from app.odoo.odoo import OdooClient
from app.hooks.hooks import Hooks
from app.server.server import Server

odoo = OdooClient()
server = Server(odoo)
hooks = Hooks(server.logger, odoo)

app = server.app

@app.get("/")
def read_root():
    return {"info": "Odoo Gateway", "version": "1.0"}

@app.get("/hook/list", tags=["Hooks"])
def webhook_list():
    keys = hooks.list.keys()
    elements = [*keys]
    return {"options": elements}

@app.post("/hook/{hook_type}", tags=["Hooks"])
async def webhook_do(hook_type: str, request: Request, background_tasks: BackgroundTasks):
    body = await request.json()

    f = hooks.get(hook_type)
    background_tasks.add_task(f, body)

    return {"hook_type": hook_type}