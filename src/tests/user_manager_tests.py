import unittest
import sqlite3
import os

from src.app.user import User
from src.app.user_dao import UserManager

username = "usrt"
firstname = "Fname"
lastname = "Lname"
mobile = "01234"
email = "usrt@example.com"
empid = "0123t"
organization = "IT"
id_ = 1

test_db = "user_data_test.db"


class UserManagerTests(unittest.TestCase):

    def setUp(self) -> None:
        with open("setup_db.sql", "r") as file:
            script = file.read()

        conn = sqlite3.connect(test_db)
        conn.executescript(script)
        conn.commit()
        conn.close()

    def tearDown(self) -> None:
        os.remove(test_db)

    def test_that_connection_works(self):
        with UserManager() as manager:
            pass

    def test_that_create_user_works(self):
        user = User(None, username, firstname, lastname, mobile, email, empid, organization)

        with UserManager(test_db) as manager:
            id = manager.create_user(user)
            self.assertEqual(8, id)

    def test_that_get_user_details_work(self):
        user_orig = User(id_=id_, username='usr1', firstname='User', lastname='One',
                         mobile='0123456701', email='usr1@example.com', empid='0001',
                         roles=(), organization='IT', last_update=1)

        with UserManager(test_db) as manager:
            user = manager.get_user_details_by_id(id_)
            self.assertEqual(user_orig, user)

    def test_that_update_user_works(self):
        user = User(id_=id_, username='usr11', firstname='User1', lastname='One1',
                    mobile='01234567011', email='usr11@example.com', empid='00011',
                    roles=(), organization='MK', last_update=1)

        with UserManager(test_db) as manager:
            id = manager.update_user(user)
            self.assertEqual(id_, id)

            changed_user = manager.get_user_details_by_id(id_)
            self.assertEqual(user, changed_user)

    def test_that_delete_user_works(self):
        user = User(id_, username)

        with UserManager(test_db) as manager:
            id = manager.delete_user(user)
            self.assertEqual(id_, id)

            user_deleted = manager.get_user_details_by_id(id_)
            self.assertIsNone(user_deleted)

    def test_that_get_user_list_works(self):
        with UserManager(test_db) as manager:
            usr_ids = manager.get_userid_list()
            self.assertEqual([1, 2, 3, 4, 5, 6, 7], usr_ids)

    def test_that_get_org_list_works(self):
        with UserManager(test_db) as manager:
            orgs = manager.get_org_list()
            self.assertEqual({'Information Technology': 'IT', 'Finance': 'FN', 'Marketing': 'MK',
                              'Sales': 'SL', 'Customer Care': 'CC'}, orgs)

    def test_that_get_role_list_works(self):
        with UserManager(test_db) as manager:
            roles = manager.get_role_list()
            self.assertEqual({'Admin': 'R1', 'Developer': 'R2', 'Agent': 'R3',
                              'Manager': 'R4'}, roles)

    # def test_that_add_role_works(self):
    #     user = User()


