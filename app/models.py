# from werkzeug.security import check_password_hash

# class User()
  
#     def __init__(self, username):
#         self.username = username

#     def is_authenticated(self):
#         return True

#     def is_active(self):
#         return True

#     def is_anonymous(self):
#         return False

#     def get_id(self):
#         return self.username

#     @staticmethod
#     def validate_login(password_hash, password):
#         return check_password_hash(password_hash, password)


class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

