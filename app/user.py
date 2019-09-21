class User:
    def __init__(self, id_: int, username: str = None, firstname: str = None, lastname: str = None,
                 mobile: str = None, email: str = None, empid: str = None,
                 organization: str = None, status: str = "ACTIVE", roles: set = None,
                 last_update=0):
        self.id = id_
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.mobile = mobile
        self.email = email
        self.empid = empid
        self.organization = organization
        self.status = status
        self.roles = roles
        self.last_update = last_update

    def params(self):
        return (
            self.id, self.username, self.firstname, self.lastname, self.mobile,
            self.email, self.empid, self.organization, self.status, self.roles,
            self.last_update
        )

    def __eq__(self, other):
        for (key, value) in self.__dict__.items():
            if key == 'last_update':
                continue
            if value != getattr(other, key):
                return False
        return True

    def __repr__(self):
        return f"User(" \
               f"id_={self.id}," \
               f"username='{self.username}'," \
               f"firstname='{self.firstname}'," \
               f"lastname='{self.lastname}'," \
               f"mobile='{self.mobile}'," \
               f"email='{self.email}'," \
               f"empid='{self.empid}'," \
               f"roles={self.roles}," \
               f"organization='{self.organization}'," \
               f"status='{self.status}'" \
               f"last_update={self.last_update})"
