import unittest

from src.app.user import User
from src.app.user_dao import UserManager

username = "usrt"
firstname = "Fname"
lastname = "Lname"
mobile = "01234"
email = "usrt@example.com"
empid = "0123t"
organization="IT"
id_ = 0


class UserManagerTests(unittest.TestCase):

    def test_that_connection_works(self):
        with UserManager() as manager:
            pass

    def test_that_create_user_works(self):
        user = User(username, firstname, lastname, mobile, email, empid, organization)

        with UserManager() as manager:
            id = manager.create_user(user)
            print(f"ID={id}")
            global id_
            id_ = id

    def test_that_delete_user_works(self):
        user = User(username, id_=id_)

        with UserManager() as manager:
            id = manager.delete_user(user)
            self.assertEqual(id_, id)

