import odoorpc
import urllib.request

from app.health.http import HttpUACheck

from os import environ as env

class OdooClient:
    conn = None

    def __init__(self) -> None:
        self.host       = env.get('ODOO_HOST', 'localhost')
        self.port       = env.get('ODOO_PORT', '8069')
        self.protocol   = env.get('ODOO_PROTO', 'jsonrpc')
        self.database   = env.get('ODOO_DB')
        self.username   = env.get('ODOO_USER')
        self.password   = env.get('ODOO_PASS')
        self.user_agent = env.get('ODOO_UA', 'OdooGateway/1.0')
        self.prefix     = "https" if self.protocol.endswith("ssl") else "http"
        self.full_url   = f"{self.prefix}://{self.host}:{self.port}"

        ####### set custom user agent #######
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent', self.user_agent)]
        ####### end custom user agent #######

        self.conn = odoorpc.ODOO(
            self.host,
            port=self.port,
            protocol=self.protocol,
            opener=opener,
        )
        self.conn.login(
            self.database,
            self.username,
            self.password,
        )

        ####### Model Classes ########
        self.Todo = self.conn.env['project.task']
        self.Model = self.conn.env['ir.model']

    def _debug_env(self):
        print(self.conn.env)

    def get_healthcheck(self):
        url = f"{self.full_url}/web/login"
        return HttpUACheck(
            url=url,
            user_agent=self.user_agent
        )

    def get_user(self):
        user_id = self.conn.env.user.id
        r = self.conn.execute('res.users', 'read', [user_id])
        return r
    
    def list_models(self):
        model_ids = self.Model.search([])
        models = self.Model.browse(model_ids)
        return models

    def create_todo(self, name, description):
        todos = self.Todo.create({
            'name': name,
            'user_ids': [self.conn.env.user.id],
            'description': description
        })
        return todos