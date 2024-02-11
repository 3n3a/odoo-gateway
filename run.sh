#!/bin/bash
#
# run
#

docker build -t odoo-gateway-local .

docker run --env-file ./.env -p 3000:80 odoo-gateway-local