class User:
    def __init__(self, username: str, firstname: str = None, lastname: str = None,
                 mobile: str = None, email: str = None, empid: str = None,
                 organization: str = None, roles: tuple = (), last_update=0, id_=0):
        self.id = id_
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.mobile = mobile
        self.email = email
        self.empid = empid
        self.organization = organization
        self.roles = roles
        self.last_update = last_update

    def params(self):
        return (
            self.id, self.username, self.firstname, self.lastname, self.mobile,
            self.email, self.empid, self.organization, self.roles, self.last_update
        )

    def __repr__(self):
        return f"User(" \
               f"id={self.id}," \
               f"username={self.username}," \
               f"firstname={self.firstname}," \
               f"lastname={self.lastname}," \
               f"mobile={self.mobile}," \
               f"email={self.email}," \
               f"empid={self.empid}," \
               f"roles={self.roles}," \
               f"organization={self.organization}," \
               f"last_update={self.last_update})"
