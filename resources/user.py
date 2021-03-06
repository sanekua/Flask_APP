from flask_restful import Resource, reqparse
from models.user import UserModel

# class User(object):
#     def __init__(self, _id, username, password):
#         self.id = _id
#         self.username = username
#         self.password = password
#
#     @classmethod
#     def find_by_username(cls, username):
#         connection = sqlite3.connect('../data.db')
#         cursor = connection.cursor()
#
#         query = "SELECT * FROM users WHERE username=?"#.format(table=cls.TABLE_NAME)
#         result = cursor.execute(query, (username,))
#         row = result.fetchone()
#         if row:
#             user = cls(*row)
#         else:
#             user = None
#
#         connection.close()
#         return user
#
#
#     @classmethod
#     def find_by_id(cls, _id):
#         connection = sqlite3.connect('../data.db')
#         cursor = connection.cursor()
#
#         query = "SELECT * FROM users WHERE id=?"#.format(table=cls.TABLE_NAME)
#         result = cursor.execute(query, (_id,))
#         row = result.fetchone()
#         if row:
#             user = cls(*row)
#         else:
#             user = None
#
#         connection.close()
#         return user

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blanc")


    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field passw cannot be blanc")

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "User with that username already exists."}, 400

        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        return {"message": "User created successfully"}, 201