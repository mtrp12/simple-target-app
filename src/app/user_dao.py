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

                obj = self.conn.cursor()
                obj.execute(sql, values)
                self.conn.commit()

                return user.id

            def add_roles(self, user: User) -> bool:
                roles = self.get_user_roles(user.id)
                duplicates = roles.intersection(user.roles)
                if duplicates != set():
                    raise ValueError(f"Duplicate Roles: {duplicates}")

                sql = "INSERT INTO USER_ROLES(USER_ID, ROLE_ID) VALUES (?,?)"
                obj = self.conn.cursor()
                params = [(user.id, roleid) for roleid in user.roles]
                try:
                    obj.executemany(sql, params)
                except sqlite3.Error as e:
                    self.conn.rollback()
                    raise e

                self.conn.commit()
                return True


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
                    user = User(row[0], *row[1:8], last_update=row[8])
                return user

            def get_user_roles(self, id_) -> set:
                sql = "SELECT ROLE_ID FROM USER_ROLES WHERE USER_ID=?"
                obj = self.conn.cursor()
                obj.execute(sql, (id_,))
                rows = obj.fetchall()

                return set(itertools.chain(*rows))

            def update_timestamp(self):
                pass

        self.db_handler = DBHandler()
        return self.db_handler

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db_handler.close()
