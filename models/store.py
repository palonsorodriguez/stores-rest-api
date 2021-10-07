# import sqlite3
from db import db

class StoreModel(db.Model):
        __tablename__ = 'stores'

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(80))

        #we are doing back reference. allows the store to see what items are in the items table with a certain store id
        items = db.relationship('ItemModel', lazy='dynamic') # this is a list as it is a one to many (1 store id many items)
        #not go into the items table and create an object for each item yet, as it can be a very expensive operation

        def __init__(self, name):
                self.name = name

        def json(self):
                # before setting lazy='dynamic' return {'name': self.name, 'items': [item.json() for item in self.items]}
                # when we use lazy dynamic, self.items is no longer a list of items now is a query builder that has the ability to look into the items table, so we
                # use .all() to retrieve all the items in that table which means that until we call the json method we're not looking into the table which
                # means that creating stores is very simple, however also means that every time we call the json method we have to go into the table
                # so then it is going to be slower. so that means that we create a store so we load all the items and then we call the json method many times for free
                # if we use lazy dynamic everytime we call the json method we have to go into the table so it's slower
                # there's a trade between speed of creation of the store and speed of calling the json method that you need to think about which one is more important
                # in our case as the store model is created when we want to access the data is gonna be like that a resource so we stick with that

                return {'name': self.name, 'items': [item.json() for item in self.items.all()]}


        @classmethod
        def find_by_name(cls, name):
                return cls.query.filter_by(name=name).first() # select * from items where name=name limit 1 --> returns the first row only [or .filter_by(id=1)]

        def save_to_db(self): #this is useful both for update and insert--> is not longer inserting, but "upserting", so we change to save_to_db
                db.session.add(self) #collection of objects that we want to write to the db
                db.session.commit()

        def delete_from_db(self): #was update. now delete_from_db
                db.session.delete(self)
                db.session.commit()
