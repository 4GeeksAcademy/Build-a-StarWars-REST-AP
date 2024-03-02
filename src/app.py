"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Favorite_planet, Favorite_people
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#------------------------------------------Metodo GET para obtener todos los User----------------------------------#
@app.route('/user', methods=['GET'])
def handle_hello():

    people_query = User.query.all()
    all_user = list(map(lambda x: x.serialize(), people_query))
    return jsonify(all_user), 200


#------------------------------------------Metodo GET para obtener todos los personajes y un personaje----------------------------------#
@app.route('/people', methods=['GET'])
def get_people():

    people_query = People.query.all()
    all_people = list(map(lambda x: x.serialize(), people_query))
    return jsonify(all_people), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_one_people(people_id):
   
    one_people = People.query.get(people_id)

    if one_people:
        person_detail = one_people.serialize()
        return jsonify(person_detail), 200
    else:
        return jsonify({"msg": "People not found."}), 404
#------------------------------------------Metodo GET para obtener todos los personajes y un personaje----------------------------------#

#------------------------------------------Metodo GET para obtener todos los planetas y un planeta----------------------------------#
@app.route('/planet', methods=['GET'])
def get_planet():

   people_query = Planet.query.all()
   all_planet = list(map(lambda x: x.serialize(), people_query))
   return jsonify(all_planet), 200


@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
   
    one_planet = Planet.query.get(planet_id)

    if one_planet:
        # Utiliza el método serialize() para convertir el objeto a JSON
        return jsonify(one_planet.serialize()), 200
    else:
        return jsonify({"message": "Planet not found"}), 404
#------------------------------------------Metodo GET para obtener todos los planetas y un planeta----------------------------------#

#------------------------------------------Metodo GET para obtener favoritos----------------------------------#
@app.route('/users/favorite', methods=['GET'])
def get_favorite_user():
    
    favorite_planets= Favorite_planet.query.all()  #GET obtener todos los planetas favoritos
    favorite_people = Favorite_people.query.all() #GET obtener todos los personajes favortios

    list_favorite_planets= list(map(lambda x: x.serialize(), favorite_planets)),
    list_favorite_people = list(map(lambda x: x.serialize(), favorite_people))

    return jsonify({"Planets": list_favorite_planets}, {"People": list_favorite_people}), 200
#------------------------------------------Metodo GET para obtener favoritos----------------------------------#

#------------------------------------------Metodo POST para crear favoritos----------------------------------#
@app.route('/favorites/people', methods=['POST'])
def add_favorite_people():

    request_body = request.get_json()
    new_favorite_people = Favorite_people(user_id = request_body['user_id'], people_id = request_body['People_id'])
    db.session.add(new_favorite_people)
    db.session.commit()
    return jsonify({"msg": "Add favorite."}), 200

@app.route('/favorites/planet', methods=['POST'])
def add_favorite_planet():

    request_body = request.get_json()
    new_favorite_planet = Favorite_planet(user_id = request_body['user_id'], planet_id = request_body['Planet_id'])
    db.session.add(new_favorite_planet)
    db.session.commit()
    return jsonify({"msg": "Add favorite."}), 200
#------------------------------------------Metodo POST para crear favoritos----------------------------------#

#------------------------------------------Metodo DELETE para eliminar favoritos----------------------------------#
@app.route('/favorites/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):

    to_delete = Favorite_people.query.filter_by(people_id = people_id).first()
    if to_delete is None:
        raise APIException("People not found.", status_code= 404)
    db.session.delete(to_delete)
    db.session.commit()
    return jsonify({"msg": "People delete."}), 200 

@app.route('/favorites/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):

    to_delete = Favorite_planet.query.filter_by(planet_id = planet_id).first()
    if to_delete is None:
        raise APIException("Planeta not found.", status_code= 404)
    db.session.delete(to_delete)
    db.session.commit()
    return jsonify({"msg": "Favorite planet delete."}), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
