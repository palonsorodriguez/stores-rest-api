#import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()  # go through and see what arguments match
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
    )  # we added price to the parser. if we add other arguments to the payload they will get erased
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id!"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            # return item # we cannot return item as is an object as opposed to dictionary --> we need to return a dictionary
            return item.json()
        return {'message' : 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message' : "An item with name '{}' already exists.".format(name)}, 400 # 400 bad request

        data = Item.parser.parse_args()

        # item = {'name' : name, 'price' : data['price']} #here we need to ensure that is not a dictionary but an itemmodel object
        #item= ItemModel(name, data['price'], data['store_id'])
        # we can simplify ItemModel(name, data['price'], data['store_id']) to item= ItemModel(name, **data)
        item= ItemModel(name, **data)

        try:
            #ItemModel.insert(item)
            #item.insert()
            item.save_to_db()
        except:
            return {"message" : "An error occurred inserting the item."}, 500 #Internal server error

        return item.json(), 201


    def delete(self, name):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "DELETE FROM items WHERE name=?"
        # cursor.execute(query, (name,))
        #
        # connection.commit()
        # connection.close()

        # return {'message' : 'Item deleted'}
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message' : 'Item deleted'}

    def put(self, name):
        # parser = reqparse.RequestParser() # go through and see what arguments match
        # parser.add_argument('price',
        #     type=float,
        #     required=True,
        #     help="This field cannot be left blank!"
        # ) #we added price to the parser. if we add other arguments to the payload they will get erased
        # #data = request.get_json() #this line was before adding parser
        # data = parser.parse_args() # parse through the arguments and puts the valid ones in data
        # ##print(data['another'])
        data= Item.parser.parse_args()

        item = ItemModel.find_by_name(name) #the item is an item object
        # updated_item = {'name': name, 'price': data['price']} # is a dictionary. we need to ensure that is an item model
        ##updated_item = ItemModel(name, data['price'])

        # if item is None: # wasn't found in database --> we want to insert the updated item
        #     try:
        #         #ItemModel.insert(updated_item)
        #         #updated_item.insert()
        #         item = ItemModel(name, data['price'])
        #     except:
        #         return {"message": "An error occurred inserting the item."}, 500
        # else:
        #     try:
        #         #ItemModel.update(updated_item)
        #         #updated_item.update()
        #         item.price = data['price']
        #
        #     except:
        #         return {"message": "An error occurred updating the item."}, 500
        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
        item.save_to_db()
        #return updated_item
        #return updated_item.json() # ensure to retrieve json
        return item.json()



class ItemList(Resource):
    def get(self):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM items"
        # result = cursor.execute(query)
        # items = []
        # for row in result:
        #     items.append({'name': row[0], 'price': row[1]})
        #
        # connection.close()
        #
        # return {'items' : items}
        # item list returned {'items': [item#json()]}
        # return {'items': ItemModel.query.all()} --> we do with list comprehension
        return {'items': [item.json() for item in ItemModel.query.all()]}
        # we could do using lambda return {'items': list(map(lambda x: x.json(), ItemModel.query.all())))} --> we would apply the function lambda x: x.json() in each element in the list ItemModel.query.all()
        #so mapping of functions to elements and then convert into list. map filter reduces methods, more stackable. they recommend list comprehension unless working with other languages (ej javascript)