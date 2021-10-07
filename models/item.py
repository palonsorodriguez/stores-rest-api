# import sqlite3
from db import db

class ItemModel(db.Model):
        __tablename__ = 'items'

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(80))
        price = db.Column(db.Float(precision=2))

        store_id= db.Column(db.Integer, db.ForeignKey('stores.id'))
        store = db.relationship('StoreModel') #join in sql alchemy. now every item model has a property called store tht is the store that matches the store id in its id

        def __init__(self, name, price, store_id):
                self.name = name
                self.price = price
                self.store_id = store_id

        def json(self):
                return {'name': self.name, 'price': self.price}

        @classmethod
        def find_by_name(cls, name):
                # connection = sqlite3.connect('data.db')
                # cursor = connection.cursor()
                #
                # query = "SELECT * FROM items WHERE name=?"
                # result = cursor.execute(query, (name,))
                # row = result.fetchone()  # we should only get one row
                # connection.close()
                #
                # if row:  # if row exists
                #         #return {'item': {'name': row[0], 'price': row[1]}} # with this is the old method returning dictionary
                #         #return cls(row[0], row[1]). Row 0 is first parameter, Row 1 the second --> perfect example to use argument unpacking
                #         # using argument unpacking
                #         return cls(*row) # we are returning an object of type ItemModel
                return cls.query.filter_by(name=name).first() # select * from items where name=name limit 1 --> returns the first row only [or .filter_by(id=1)]

        def save_to_db(self): #this is useful both for update and insert--> is not longer inserting, but "upserting", so we change to save_to_db
                # connection = sqlite3.connect('data.db')
                # cursor = connection.cursor()
                #
                # query = "INSERT INTO items VALUES (?, ?)"
                # cursor.execute(query, (self.name, self.price))
                #
                # connection.commit()
                # connection.close()
                db.session.add(self) #collection of objects that we want to write to the db
                db.session.commit()

        def delete_from_db(self): #was update. now delete_from_db
                # connection = sqlite3.connect('data.db')
                # cursor = connection.cursor()
                #
                # query = "UPDATE items SET price=? WHERE name=?"
                # cursor.execute(query, (self.price, self.name))
                #
                # connection.commit()
                # connection.close()
                db.session.delete(self)
                db.session.commit()
