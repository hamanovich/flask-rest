import sqlite3
from db import db


class ItemModel(db.model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        with sqlite3.connect('data.db') as connection:
            cursor = connection.cursor()

            query = "SELECT * FROM items where name=?"
            result = cursor.execute(query, (name,))
            item = result.fetchone()

            if item:
                return cls(*item)

    def insert(self):
        with sqlite3.connect('data.db') as connection:
            cursor = connection.cursor()

            query = "INSERT INTO items VALUES (?, ?)"
            cursor.execute(query, (self.name, self.price))
            connection.commit()

    def update(self):
        with sqlite3.connect('data.db') as connection:
            cursor = connection.cursor()

            query = "UPDATE items SET price=? WHERE name=?"
            cursor.execute(query, (self.price, self.name))
            connection.commit()
