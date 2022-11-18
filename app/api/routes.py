from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Drink, drink_schema, drinks_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'haw'}

@api.route('/drinks', methods = ['POST'])
@token_required
def create_drink(current_user_token):
    name = request.json['name']
    kind = request.json['kind']
    year = request.json['year']
    price = request.json['price']
    quantity = request.json['quantity']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    drink = Drink(name, kind, year, price, quantity, user_token = user_token )

    db.session.add(drink)
    db.session.commit()
    response = drink_schema.dump(drink)
    return jsonify(response)

@api.route('/drinks', methods = ['GET'])
@token_required
def get_drink(current_user_token):
    a_user = current_user_token.token
    drinks = Drink.query.filter_by(user_token = a_user).all()
    response = drinks_schema.dump(drinks)
    return jsonify(response)

@api.route('/drinks/<id>', methods = ['GET'])
@token_required
def get_drink_two(current_user_token, id):
    fan = current_user_token.token
    if fan == current_user_token.token:
        drink = Drink.query.get(id)
        response = drink_schema.dump(drink)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401

# UPDATE endpoint
@api.route('/drinks/<id>', methods = ['POST','PUT'])
@token_required
def update_drink(current_user_token,id):
    drink = Drink.query.get(id) 
    drink.name = request.json['name']
    drink.kind = request.json['kind']
    drink.year = request.json['year']
    drink.price = request.json['price']
    drink.quantity = request.json['quantity']
    drink.user_token = current_user_token.token

    db.session.commit()
    response = drink_schema.dump(drink)
    return jsonify(response)


# DELETE drink ENDPOINT
@api.route('/drinks/<id>', methods = ['DELETE'])
@token_required
def delete_drink(current_user_token, id):
    drink = Drink.query.get(id)
    db.session.delete(drink)
    db.session.commit()
    response = drink_schema.dump(drink)
    return jsonify(response)
