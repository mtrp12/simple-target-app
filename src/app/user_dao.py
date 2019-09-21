import sqlite3
import time
import itertools

from src.app.user import User

_db_name = ""


class UserManager:
    def __init__(self, db_name="user_data.db"):
        global _db_name
        _db_name = db_name

    def __enter__(self):
        class DBHandler:
            def __init__(self):
                # open db connection
                self.conn = sqlite3.connect(_db_name)

            def close(self):
                # close db connection
                self.conn.close()

            # returns UID
            def create_user(self, user: User) -> str:
                obj = self.conn.cursor()
                sql = "INSERT INTO USERS(username, firstname, lastname, mobile, email, " \
                      "empid, organization) VALUES (?,?,?,?,?,?,?)"
                obj.execute(sql, user.params()[1:8])
                self.conn.commit()

                sql = "SELECT ID FROM USERS WHERE USERNAME=?"
                obj.execute(sql, (user.username,))
                rows = obj.fetchall()

                # row 0, col 0
                return rows[0][0]

            def delete_user(self, user: User) -> str:
                obj = self.conn.cursor()
                sql = "DELETE FROM USERS WHERE ID=?"
                obj.execute(sql, (user.id,))
                self.conn.commit()
                return user.id

            def update_user(self, user: User) -> str:
                cols = []
                values = []
                for (key, value) in user.__dict__.items():
                    if value is None or key in ['roles', 'id', 'last_update']:
                        continue
                    cols.append(f"{key.upper()}=?")
                    values.append(value)
                cols.append("LAST_UPDATE=?")
                values.append(time.time_ns())

                sql = "UPDATE USERS " \
                      f"SET {','.join(cols)} " \
                      "WHERE ID=?"
                values.append(user.id)

                # print(sql)

                obj = self.conn.cursor()
                obj.execute(sql, values)
                self.conn.commit()

                return user.id

            def add_role(self, user: User, roles: tuple) -> bool:
                pass

            def delete_role(self, user: User, roles: tuple) -> bool:
                pass

            def get_role_list(self) -> dict:
                sql = "SELECT ROLE_NAME, ROLE_ID FROM ROLES"
                obj = self.conn.cursor()
                obj.execute(sql)
                rows = obj.fetchall()
                return {role_name: role_id for (role_name, role_id) in rows}

            def get_org_list(self) -> dict:
                sql = "SELECT ORG_NAME, ORG_ID FROM ORGS"
                obj = self.conn.cursor()
                obj.execute(sql)
                rows = obj.fetchall()

                return {org_name: org_id for (org_name, org_id) in rows}

            def get_userid_list(self) -> list:
                sql = "SELECT ID FROM USERS"
                obj = self.conn.cursor()
                obj.execute(sql)
                rows = obj.fetchall()
                return list(itertools.chain(*rows))

            def get_user_details_by_id(self, id_: str) -> User:
                sql = "SELECT * FROM USERS WHERE ID=?"
                obj = self.conn.cursor()
                obj.execute(sql, (id_,))
                row = obj.fetchone()

                user = None
                if row is not None:
                    user = User(*row[1:8], last_update=row[8], id_=row[0])
                return user

            def update_timestamp(self):
                pass

        self.db_handler = DBHandler()
        return self.db_handler

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db_handler.close()
