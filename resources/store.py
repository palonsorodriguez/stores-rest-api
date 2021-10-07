from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    #not allow editing store

    def get (self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200 # Default is 200. it's not needed
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists.".format(name)},400
        #if that doesn't happen, store doesn't exist --> well create
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'An error occurred while creating the store.'}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name) # if it was not there before the user doesn't care. only cares if deleted
        if store:
            store.delete_from_db()
        return {'message': 'Store deleted'}
class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
    pass