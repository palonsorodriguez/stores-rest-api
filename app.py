from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #Turns off flask sql alchemy modification tracker, doesn't turn off sql alchemy modificaion tracker
# #Only changing the extensions behaviour not the underlying sqlalchemy behaviour
app.secret_key = 'jose'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all() # before first request runs it will run this and create data.db and create all the tables unless they exist already


jwt= JWT(app, authenticate, identity) # /auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)