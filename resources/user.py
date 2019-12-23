import sqlite3
from flask_restful import Resource, reqparse

from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='This field is mandatory'
                        )

    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='This field is mandatory'
                        )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data.get('username')):
            return {'message': f'User with username `{data.get("username")}` already exists'}, 400

        with sqlite3.connect('data.db') as connection:
            cursor = connection.cursor()

            query = "INSERT INTO users VALUES (NULL, ?, ?)"
            cursor.execute(query, (data.get('username'), data.get('password')))
            connection.commit()

        return {'message': 'User created successfully'}, 201
