# odoo-gateway

> gateway for webhooks between odoo and other applications

## env

> setup

```sh
cp env.template .env
echo "Fill out '.env'"
```

> additional env variables

| variable | description | value example |
| --- | --- | --- |
| `WEBHOOK_TASK_ASSIGNEE_OVERRIDE_ID` | User ID used as assignee when creating tasks via "fb_todo". *Value*: Integer | `2` |

## web

> setup

```sh
python3 -m venv venv
```

> run

```sh
source venv/bin/activate
./run.sh
```

### httpx

[source](https://www.python-httpx.org/)

### fastapi

[source](https://fastapi.tiangolo.com/)

### odoorpc

[source](https://github.com/OCA/odoorpc)


## cli

> run

```sh
source venv/bin/activate
python cli.py --help
```

### click

[source](https://click.palletsprojects.com/en/8.1.x/)

### rich

[source](https://rich.readthedocs.io/en/stable/tables.html)