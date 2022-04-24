from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity

# A Model is an internal representation of an entity whereas a Resource is an external representation of an entity.
# Resources are those classes with which the API interacts.
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from db import db

app = Flask(__name__)
app.secret_key = 'Fatima'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # It will disable Flask SQLAlchemy modifications tracker but
# SQLAlchemy modifications tracker will still be enabled.
db.init_app(app)
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)  # auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
