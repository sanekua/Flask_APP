from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Store ID!"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message":"Item wasnt found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'], data['store_id'])
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurs inserting the item"}, 500
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "INSERT INTO items VALUES (?,?)"
        # cursor.execute(query, (item['name'], item['price']))
        #
        # connection.commit()
        # connection.close()
        return item.json(), 201


    #@jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"message":"Item was deleted"}

    #@jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item=ItemModel(name, data['price'], data['store_id'])
        else:
            item.price=data['price']

        item.save_to_db()

        return item.json()



class ItemList(Resource):
    TABLE_NAME = 'items'

    def get(self):
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}