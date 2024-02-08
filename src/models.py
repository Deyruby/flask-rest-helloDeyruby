from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__= "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique= True)
    password = db.Column(db.String(250),unique=False, nullable=False)
    subscription_date = db.Column(db.Integer, nullable=False)


    def serialize_1(self):
        return {
        "id": self.id,
        "name": self.name,
        "last_name": self.last_name,
        "email": self.email,
        "subscription_date": self.subscription_date
    }
    

class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.db.String(250), unique=True)
    status = db.Column(db.String(250), nullable=False)
    species = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(250), nullable=False)    
    
    def serialize_2(self):
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "species": self.species,
            "gender": self.gender  
            }

class CharacterEpisodeAndLocation(db.Model):
     __tablename__ = 'characterepisodeandlocation'
     id = db.Column (db.Integer, primary_key= True)
     id_character = db.Column (db.Integer, db.ForeignKey('character.id'))
     character= db.relationship(Character)
     episode= db.Column(db.String, nullable= False)
     location= db.Column(db.String, nullable=False)
    
     def serialize_3(self):
         return {
            "id_character": self.id_character,
            "episode": self.episode,
            "location": self.location
            }

class Favoritecharacter(db.Model):   
   __tablename__ = 'favoritecharacter'
   id = db.Column(db.Integer, primary_key=True)
   id_user =db.Column(db.Integer, db.ForeignKey('user.id')) # Marca el id del usuario que selecciona un personaje como favorito
   user = db.relationship(User)
   id_character = db.Column(db.Integer,db.ForeignKey('character.id')) # Marca el id del personaje que ha sido seleccionado como favorito
   character = db.relationship(Character)

   def serialize(self):
         return {

            "id": self.id,
            "id_user": self.user.id,
            "id_ character": self.character.id,
            "character_name": self.character.name
        }
  
    
    
    