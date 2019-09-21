import sqlite3

from src.app.user import User


class UserManager:
    def __enter__(self, db_name="user_data.db"):
        class DBHandler:
            def __init__(self):
                # open db connection
                self.conn = sqlite3.connect(db_name)

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
                pass

            def add_role(self, user: User, roles: tuple) -> bool:
                pass

            def delete_role(self, user: User, roles: tuple) -> bool:
                pass

            def get_role_list(self) -> list:
                pass

            def get_org_list(self) -> list:
                pass

            def get_username_list(self) -> list:
                pass

            def get_user_details_by_username(self, username: str) -> User:
                pass

            def update_timestamp(self):
                pass

        self.db_handler = DBHandler()
        return self.db_handler

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db_handler.close()
