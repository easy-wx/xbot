import sqlite3


class UserPermissionHelper:
    def __init__(self):
        self.op = PermissionOp()
        self.permissions = {}

    def check_user_permission(self, username, cmd, subcmd):
        permission = self.op.query_permissions_by_username(username)
        return permission.has_permission(cmd, subcmd)


class UserPermission:
    def __init__(self, username):
        self.username = username
        self.lines = []

    def add_line(self, cmd, subcmd, valid_until):
        class PermissionLine:
            def __init__(self, cmd_, subcmd_, valid_until_):
                self.cmd = cmd_
                self.subcmd = subcmd_
                self.valid_until = valid_until_
        self.lines.append(PermissionLine(cmd, subcmd, valid_until))

    def __str__(self):
        ret = f"Permission for {self.username}:\n"
        for line in self.lines:
            ret += f"cmd: {line.cmd}, subcmd: {line.subcmd}, valid_until: {line.valid_until}\n"
        return ret

    def has_permission(self, cmd, subcmd):
        for line in self.lines:
            if line.cmd == "*":
                return True
            if line.cmd == cmd and line.subcmd == "*":
                return True
            if line.cmd == cmd and line.subcmd == subcmd:
                return True
        return False


class PermissionOp:
    def __init__(self):
        self.conn = sqlite3.connect('local.db')

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS permissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            cmd TEXT NOT NULL,
            subcmd TEXT NOT NULL,
            valid_until DATE NOT NULL
        )
        ''')
        self.conn.commit()

    def insert_permission(self, username, cmd, subcmd, valid_until):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO permissions (username, cmd, subcmd, valid_until)
        VALUES (?, ?, ?, ?)
        ''', (username, cmd, subcmd, valid_until))
        self.conn.commit()

    def query_permissions(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM permissions')
        rows = cursor.fetchall()
        return rows

    def query_permissions_by_username(self, username):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM permissions WHERE username = ?', (username,))
        ret = UserPermission(username)
        for row in cursor.fetchall():
            ret.add_line(row[2], row[3], row[4])
        return ret

