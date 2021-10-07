import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

# retrieve user objects from database

class UserRegister(Resource):

    parser = reqparse.RequestParser() # because we have a parser won't have anything more or less that the parameters defined
    parser.add_argument('username',
        type=str,
        required=True,
        help = "This field cannot be blank."
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help = "This field cannot be blank."
    )

    def post(self):

        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']) is not None:
            return {"message": "An user with that username already exists"}, 400

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "INSERT INTO users VALUES (NULL, ?, ?)"
        # cursor.execute(query, (data['username'], data['password'],)) # username and password must be a tuple. we don't need the comma in the end of the table, but we can add it
        #
        # connection.commit()
        # connection.close()

        #user = UserModel(data['username'], data ['password'])
        user = UserModel(**data) # for each of the keys in data username=value password=value
        user.save_to_db()

        return {"message": "User created successfully."}, 201
