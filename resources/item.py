from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This is a required field')
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help='This is a required field')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        return item.json() if item else {'message': 'item not found'}, 404

    def post(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return {'message': 'item {} already exists'.format(name)}, 400

        data = Item.parser.parse_args()
        # data = request.get_json()
        new_item = ItemModel(name, **data)

        try:
            new_item.save_to_db()
        except:
            return {'message': 'An error occurred'}, 500  # Internal Server Error

        return new_item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()

    # def patch(self, name):  It refers to the partial modification of a resource
    #     data = request.get_json()
    #     item = next(filter(lambda x: x['name'] == name, items), None)
    #     if item is None:
    #         return {'message': 'item not found'}, 404
    #     else:
    #         item.update(data)
    #         return item


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
