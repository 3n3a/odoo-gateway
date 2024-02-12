

class Hooks:
    def __init__(self, logger, odoo) -> None:
        self.logger = logger
        self.odoo = odoo

        self.list = {
            "user": self.hook_user,
            "fb_todo": self.hook_fb_todo,
        }

    def get(self, hook_name):
        return self.list.get(hook_name, self.hook_default)
    
    ## hooks
    def __template_hook(self, body):
        # needs self and body
        
        # logging
        self.logger.info("Test String")

        # accessing odoo
        self.odoo.get_user()

        # doesn't return anything

    def hook_default(self, body):
        self.logger.info("Default Webhook")
        self.logger.info(f"Body: {body}")

    def hook_user(self, body):
        user_details = self.odoo.get_user()
        username = user_details[0].get("name", "No User Found")
        self.logger.info(f"User: {username}")

    def hook_fb_todo(self, body):
        templ = """<table class="table table-bordered o_table" style="height: 165.25px; width: 1182px;" data-last-history-steps="1785015246683131"><tbody>{}</tbody></table><p><br></p>"""
        line_templ = """<tr style="height: 56.25px;"><td style="width: 136px;"><p><strong>{}</strong><br></p></td><td style="width: 1045px;"><p>{}<br></p></td></tr>"""
        inner = ""

        data = body.get('data').get('data')
        name = data.get('reason')

        for key, value in data.items():
            inner += line_templ.format(key, value)

        desc = templ.format(inner)
        todo_details = self.odoo.create_todo(name, desc)
        self.logger.info(f"Todo Create: {todo_details}")