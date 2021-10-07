import sqlite3
from db import db

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80)) #https://stackoverflow.com/questions/58069745/sqlalchemy-warning-column-wont-be-part-of-the-declarative-mapping
    password = db.Column(db.String(80))

    def __init__(self,  username, password):
        #self.id = _id #we got rid of the id because is primary key autoincremented --> we don't need to insert explicitly
        #when we create the object we dont need to specify teh id. when we use sqlalchemy it will give us the id (so we can say self.id)
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM users WHERE username = ?"
        # result = cursor.execute(query, (username,))
        # row = result.fetchone()
        # if row is not None: # if row:
        #     #user = User(row[0], row[1], row[2]) --> old returning user
        #     #user = cls(row[0], row[1], row[2]) # new with @classmethod but not with set
        #     user = cls(*row) # new with @classmethod with set
        # else:
        #     user = None
        #
        # connection.close()
        # return user
        return cls.query.filter_by(username=username).first() # select * from users

    @classmethod
    def find_by_id(cls, _id):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM users WHERE id = ?"
        # result = cursor.execute(query, (_id,))
        # row = result.fetchone()
        # if row is not None: # if row:
        #     user = cls(*row)
        # else:
        #     user = None
        #
        # connection.close()
        # return user
        return cls.query.filter_by(id=_id).first()
