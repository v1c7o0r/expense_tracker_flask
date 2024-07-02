from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, User, Category

# Initialize the flask application
app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class Index(Resource):
    def get(self):
        body = {
            "index": "Welcome to the Expense Tracker App"
        }

        response = make_response(body, 200)

        return response
    
api.add_resource(Index, '/')

class Users(Resource):
    def get(self):
        users = User.query.all()
        users_list = []

        for user in users:
            users_list.append(user.to_dict())

        body = {
            "count": len(users_list),
            "users": users_list
        }

        return make_response(body, 200)

    def post(self):
        new_user = User(
            username=request.json.get("username"),
            email=request.json.get("email")
        )

        db.session.add(new_user)
        db.session.commit()

        response = make_response(new_user.to_dict(), 201)

        return response

api.add_resource(Users, '/users')

class UsersByID(Resource):
    def get(self, id):
        user = User.query.filter_by(id=id).first()

        if user == None:
            body = {
                "message": "This record does not exist in our database. Please try again."
            }
            response = make_response(body, 404)

            return response
        else:
            user_dict = user.to_dict()

            response = make_response(user_dict, 200)

            return response

    def patch(self, id):
        user = User.query.filter_by(id=id).first()

        for attr in request.json:
                setattr(user, attr, request.json.get(attr))

        db.session.add(user)
        db.session.commit()

        user_dict = user.to_dict()

        response = make_response(user_dict, 200)

        return response

    def delete(self, id):
        user = User.query.filter_by(id=id).first()

        db.session.delete(user)
        db.session.commit()

        body = {
            "delete_successful": True,
            "message": "User deleted."
        }

        response = make_response(body, 200)

        return response

api.add_resource(UsersByID, '/users/<int:id>')

if __name__ == "__main__":
    app.run(port=5555, debug=True)