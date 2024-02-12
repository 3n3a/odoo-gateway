import logging
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi_healthchecks.api.router import HealthcheckRouter, Probe

class Server:
    def __init__(self, odoo) -> None:
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.app = FastAPI()
        self.odoo = odoo

        self._setup_app()

    def _setup_app(self):
        ## middleware
        self.app.add_middleware(GZipMiddleware, minimum_size=1000)

        ## routers
        self.app.include_router(
            HealthcheckRouter(
                Probe(
                    name="readiness",
                    checks=[
                        self.odoo.get_healthcheck()
                    ],
                ),
                Probe(
                    name="liveness",
                    checks=[
                        self.odoo.get_healthcheck()
                    ]
                )
            ),
            prefix="/health"
        )
