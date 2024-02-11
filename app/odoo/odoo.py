import odoorpc
import urllib.request

class OdooClient:
    conn = None

    def __init__(self, host, port, database, username, password, protocol, user_agent) -> None:
        if not host:
            print("host not set")
            return
        if not port:
            print("pord not set")
            return
        if not database:
            print("database not set")
            return
        if not username:
            print("username not set")
            return
        if not password:
            print("password not set")
            return
        if not protocol:
            print("protocol not set")
            return

        ####### set custom user agent #######
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent', user_agent)]
        ####### end custom user agent #######

        self.conn = odoorpc.ODOO(
            host,
            port=port,
            protocol=protocol,
            opener=opener,
        )
        self.conn.login(
            database,
            username,
            password,
        )

    def _debug_env(self):
        print(self.conn.env)

    def get_user(self):
        user_id = self.conn.env.user.id
        r = self.conn.execute('res.users', 'read', [user_id])
        return r

    def create_todo(self, name, description):
        Todo = self.conn.env['project.task']
        todos = Todo.create({
            'name': name,
            'user_ids': [self.conn.env.user.id],
            'description': description
        })
        return todos