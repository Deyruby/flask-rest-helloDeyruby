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
from models import db, User, Character, Favoritecharacter, CharacterEpisodeAndLocation
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

#db_url = os.getenv("DATABASE_URL")
#if db_url is not None:
  #  app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
#else:
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/') 
def sitemap():
    return generate_sitemap(app)  

#Creamos un usuario
@app.route('/createuser', methods=["POST"])
def create():
  get_from_body = request.json.get("email")
  user = User() 
  usuario_existente = User.query.filter_by(email=get_from_body).first()
  if usuario_existente is not None:
    return "The User already exist"
  else:
    user.name = request.json.get("name")
    user.last_name = request.json.get("lastname")
    user.email = request.json.get("email")
    user.password = request.json.get("password")
    user.subscription_date =request.json.get("subscription_date")

    db.session.add(user)
    db.session.commit()  

    return f"Se creo el usuario", 201
 
 #Actualizo un usuario
@app.route('/updateuser', methods=["PUT"])
def update():
  email_to_search = request.json.get("email")
  usuario = User.query.filter_by(email=email_to_search).first()
  if usuario is None:
    return "The user does not exist", 401
  else:
    usuario.name = request.json.get("name")
    usuario.last_name = request.json.get("lastname")
    usuario.email = request.json.get("email")
    usuario.password = request.json.get("password")
  
    db.session.add(usuario)
    db.session.commit()

    return f"Se actualizo el usuario", 201
 
 #Eliminar un usuario
@app.route("/deleteuser/<int:id>", methods=['DELETE'])
def delete_user(id):
  usuario = User.query.filter_by(id=id).first()
  print(usuario)
  if usuario is not None:
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({
      "msg": "Usuario eliminado",
      "status": "Success"
    }), 203
  else:
    return jsonify({"error":"Usuario no encontrado"}),404

 
# Listo todos los usuarios
@app.route('/users', methods=["GET"])
def home():
    users= User.query.all()
    users= list(map(lambda user: user.serialize_1(), users))
   
    return jsonify({
    "data": users,
    "status": 'success'
  }),200


  #Agregar Personaje
@app.route('/createcharacter', methods=["POST"])
def createcharacter():
 add_a_character = request.json.get("name")
 character = Character() 
 personaje_existente = Character.query.filter_by(name=add_a_character).first()
 if personaje_existente is not None:
    return "The character already exist"
 else:
    character.name = request.json.get("name")
    character.status = request.json.get("status")
    character.species= request.json.get("species")
    character.gender =request.json.get("gender")

    db.session.add(character)
    db.session.commit()  

    return f"Se creo el personaje", 201

#Muestro los personajes por su id
@app.route('/character/<int:id>', methods=["GET"])
def obtainig_character(id):
    characterbyid= Character.query.filter_by(id=id).first()
    if characterbyid is not None:
         return jsonify(characterbyid.serialize_2()), 200
    else:
         return jsonify({"error":"Character not found"}),404
    
    
#Listo los personajes
@app.route('/character', methods=["GET"])
def character():
    characters= Character.query.all()
    characters= list(map(lambda character: character.serialize_2(), characters))
   
    return jsonify({
    "data": characters,
    "status": 'success'
  }),200   


#Actualizo un Personaje
@app.route('/updatecharacter', methods=["PUT"])
def updatecharacter():
  name_to_search = request.json.get("name")
  charactertoupdate = Character.query.filter_by(name=name_to_search).first()
  if charactertoupdate is None:
    return "The character does not exist", 401
  else:
    charactertoupdate.name = request.json.get("name")
    charactertoupdate.status = request.json.get("status")
    charactertoupdate.species = request.json.get("species")
    charactertoupdate.gender = request.json.get("gender")
  
    db.session.add(charactertoupdate)
    db.session.commit()
    return f"Se actualizo el personaje", 201

#Elimino personaje  
@app.route("/deletecharacter/<int:id>", methods=['DELETE'])
def delete_character(id):
  character_delete = Character.query.filter_by(id=id).first()
  if character_delete is not None:
    db.session.delete(character_delete)
    db.session.commit()
    return jsonify({
      "msg": "Personaje eliminado",
      "status": "Success"
    }), 203
  else:
    return jsonify({"error":"Personaje no encontrado"}),404



#Agrego Episodios y locacion
@app.route('/addepisodeandlocation', methods=["POST"])
def addepisodeandlocation():
  episodeandlocation = CharacterEpisodeAndLocation() 
  episodeandlocation.id_character = request.json.get("character_id")
  episodeandlocation.name_character = request.json.get("name")
  episodeandlocation.episode = request.json.get("episode")
  episodeandlocation.location = request.json.get("location")
    

  db.session.add(episodeandlocation)
  db.session.commit()  
  
  return f"Se creo satisfactoriamente", 201

# Muestro episodios y locacion por id
@app.route('/characterepisodeandlocation/<int:id>', methods=["GET"])
def episode_location(id):
    characterepiandloc= CharacterEpisodeAndLocation.query.filter_by(id=id).first()
    if characterepiandloc is not None:
         return jsonify(characterepiandloc.serialize_3()), 200
    else:
         return jsonify({"error":"Character not found"}),404

#Actualizo episodios y locacion 
@app.route('/updateepisodeandlocation', methods=["PUT"])
def updateepisodeandlocation():
  id_to_search = request.json.get("id")
  episodeandlocationtoupdate = CharacterEpisodeAndLocation.query.filter_by(id=id_to_search).first()
  if episodeandlocationtoupdate is None:
    return "The episode and location do not exist", 401
  else:
    episodeandlocationtoupdate.id_character = request.json.get("id_character")
    episodeandlocationtoupdate.episode = request.json.get("episode")
    episodeandlocationtoupdate.location = request.json.get("location")
    
  
    
    db.session.commit()
    return f"Se actualizo episodio y locacion", 201     

  #Eliminar episodios y locacion por id    
@app.route("/deleteepisodeandlocation/<int:id>", methods=['DELETE'])
def delete_episodeandlocation(id):
  episodeandlocation_delete = CharacterEpisodeAndLocation.query.filter_by(id=id).first()
  if episodeandlocation_delete is not None:
    db.session.delete(episodeandlocation_delete)
    db.session.commit()
    return jsonify({
      "msg": "Episodio y locacion eliminado",
      "status": "Success"
    }), 203
  else:
    return jsonify({"error":"Episodio y locacion no encontrada"}),404
  

#Crear favoritos para un usuario
@app.route('/createfavorite', methods=["POST"])
def createfavorite():
 add_a_favorite = request.json.get("id_character")
 favoritecharacter = Favoritecharacter() 
 personaje_favorito = Favoritecharacter.query.filter_by(id_character=add_a_favorite).first()
 if personaje_favorito is not None:
    return "The Favorite character already exist"
 else:
    favoritecharacter.id_user = request.json.get("id_user")
    favoritecharacter.id_character = request.json.get("id_character")
   

    db.session.add(favoritecharacter)
    db.session.commit()  

    return f"Se agrego el personaje favorito", 201

#Listar los favoritos de un usuario
@app.route('/favoritecharacter', methods=["GET"])
def favorite_character():
  favoritocharacter= Favoritecharacter.query.all()
  favoritocharacter= list(map(lambda favoritecharacter: favoritecharacter.serialize(), favoritocharacter))
 
  return jsonify({
    "data": favoritocharacter,
    "status": 'success'
  }),200   

#Actualizar personaje favorito
@app.route('/updatefavoritecharacter', methods=["PUT"])
def updatefavoritecharacter():
  id_to_search = request.json.get("id")
  favorite_character_toupdate = Favoritecharacter.query.filter_by(id=id_to_search).first()
  if favorite_character_toupdate is None:
    return "The favorite character do not exist", 401
  else:
    favorite_character_toupdate.id_user = request.json.get("id_user")
    favorite_character_toupdate.id_character = request.json.get("id_character")

    db.session.add(favorite_character_toupdate)
    db.session.commit()
    return f"Se actualizo el personaje favorito", 201


 #Eliminar Favorito de un usuario          
@app.route("/deletefavorite/<int:id>", methods=['DELETE'])
def delete_favorite(id):
  favorite_delete = Favoritecharacter.query.filter_by(id=id).first()
  if favorite_delete is not None:
    db.session.delete(favorite_delete)
    db.session.commit()
    return jsonify({
      "msg": "Personaje favorito eliminado",
      "status": "Success"
    }), 203
  else:
    return jsonify({"error":"Personaje favorito no encontrado"}),404
    


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
