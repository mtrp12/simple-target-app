main_db = "data/user_data.db"
test_db = "data/user_data_test.db"

# attributes
req_attrs = {'username', 'lastname', 'organization'}
all_attrs = {"id", "username", "firstname", "lastname", "mobile", "email", "empid",
             "organization", "status", "roles", "last_update"}

# configs are also in start_app.sh
host = "localhost"
port = 5000
flask_env = True
