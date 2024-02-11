from typing import Union
from fastapi import FastAPI, BackgroundTasks, Request
from fastapi.middleware.gzip import GZipMiddleware
from fastapi_healthchecks.api.router import HealthcheckRouter, Probe
from app.health.http import HttpUACheck

from os import environ as env
from app.odoo.odoo import OdooClient

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ODOO_HOST = env.get('ODOO_HOST', 'localhost')
ODOO_PORT = env.get('ODOO_PORT', '8069')
ODOO_PROTO = env.get('ODOO_PROTO', 'jsonrpc')

ODOO_UA = env.get('ODOO_UA', 'OdooGateway/1.0')
ODOO_PREFIX = "https" if ODOO_PROTO.endswith("ssl") else "http"
ODOO_FULL_URL = f"{ODOO_PREFIX}://{ODOO_HOST}:{ODOO_PORT}/web/login"

app = FastAPI()
app.add_middleware(GZipMiddleware, minimum_size=1000)

app.include_router(
    HealthcheckRouter(
        Probe(
            name="readiness",
            checks=[
                HttpUACheck(
                    url=ODOO_FULL_URL,
                    user_agent=ODOO_UA
                )
            ],
        ),
        Probe(
            name="liveness",
            checks=[
                HttpUACheck(
                    url=ODOO_FULL_URL,
                    user_agent=ODOO_UA
                )
            ]
        )
    ),
    prefix="/health"
)

odoo = OdooClient(
    host=ODOO_HOST,
    port=ODOO_PORT,
    database=env.get('ODOO_DB'),
    username=env.get('ODOO_USER'),
    password=env.get('ODOO_PASS'),
    protocol=ODOO_PROTO,
    user_agent=ODOO_UA,
)

@app.get("/")
def read_root():
    return {"info": "Odoo Gateway", "version": "1.0"}

#### webhooks ####
def hook_default(body):
    logger.info("Default Webhook")
    logger.info(f"Body: {body}")

def hook_user(body):
    user_details = odoo.get_user()
    username = user_details[0].get("name", "No User Found")
    logger.info(f"User: {username}")

def hook_fb_todo(body):
    templ = """<table class="table table-bordered o_table" style="height: 165.25px; width: 1182px;" data-last-history-steps="1785015246683131"><tbody>{}</tbody></table><p><br></p>"""
    line_templ = """<tr style="height: 56.25px;"><td style="width: 136px;"><p><strong>{}</strong><br></p></td><td style="width: 1045px;"><p>{}<br></p></td></tr>"""
    inner = ""

    data = body.get('data').get('data')
    name = data.get('reason')

    for key, value in data.items():
        inner += line_templ.format(key, value)

    desc = templ.format(inner)
    todo_details = odoo.create_todo(name, desc)
    logger.info(f"Todo Create: {todo_details}")

hook_types = {
    "user": hook_user,
    "fb_todo": hook_fb_todo,
}

@app.post("/hook/{hook_type}")
async def webhook_do(hook_type: str, request: Request, background_tasks: BackgroundTasks):
    body = await request.json()

    f = hook_types.get(hook_type, hook_default)
    background_tasks.add_task(f, body)

    return {"hook_type": hook_type}