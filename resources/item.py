import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field can not be empty one!'
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()

        return {'message': f'Item `{name}` not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f'An item with name `{name}` already exists'}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, data.get('price'))

        try:
            item.insert()
        except:
            return {'message': f'An error occured inserting the item with name `{name}`'}, 500

        return item.json(), 201

    def delete(self, name):
        with sqlite3.connect('data.db') as connection:
            cursor = connection.cursor()

            query = "DELETE FROM items WHERE name=?"
            cursor.execute(query, (name,))
            connection.commit()

        return {'message': f'Item with name `{name}` deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data.get('price', 0))

        if item is None:
            try:
                updated_item.insert()
            except:
                return {'message': f'An error occured inserting the item with name `{name}`'}, 500
        else:
            try:
                updated_item.update()
            except:
                return {'message': f'An error occured updating the item with name `{name}`'}, 500

        return updated_item.json()


class ItemList(Resource):
    def get(self):
        with sqlite3.connect('data.db') as connection:
            cursor = connection.cursor()

            query = "SELECT * FROM items"
            result = cursor.execute(query)
            items = result.fetchall()
            return {'items': items}
