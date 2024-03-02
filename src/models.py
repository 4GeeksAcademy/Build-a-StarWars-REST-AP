# Importación de la clase SQLAlchemy desde la extensión Flask SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship, declarative_base

# Creación de una instancia de la clase SQLAlchemy
db = SQLAlchemy()

# Definición del modelo de la tabla 'User'
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    #favorito = relationship('Favoritos', back_populates='usuario')

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }


class People(db.Model):
    __tablename__ = 'people'
    people_id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(250), nullable=False)  
    height = db.Column(db.String(50), nullable=True)  
    color_eyes = db.Column(db.String(50), nullable=True)  
    gender = db.Column(db.String(20), nullable=True)  

    def __repr__(self):
        return '<People %r>' % self.nombre 

    # Método que serializa el objeto User en un diccionario
    def serialize(self):
        return {
            "id": self.people_id,
            "name": self.nome,
            "height": self.height,
            "color_eyes": self.color_eyes,
            "gender": self.gender
            
        }
    
class Planet(db.Model):
    __tablename__ = 'planet'
    planet_id = db.Column(db.Integer, primary_key=True)  # Clave primaria
    name = db.Column(db.String(250), nullable=False)  # Columna no nula
    surface= db.Column(db.String(50), nullable=True)  # Columna con valores nulos
    population = db.Column(db.String(50), nullable=True)  # Columna con valores nulos
    residents = db.Column(db.String(250), nullable=True)  # Columna con valores nulos
    climate = db.Column(db.String(50), nullable=True)  # Columna con valores nulos

    def __repr__(self):
        return '<Planet %r>' % self.nombre

    
    def serialize(self):
        return {
            "id": self.planet_id,
            "name": self.name,
            "surface": self.surface,
            "population": self.population,
            "residents": self.residents,
            "climate": self.climate
            
        }

class Favorite_people(db.Model):
    __tablename__ = 'favorite_people'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    people_id = db.Column(db.Integer, db.ForeignKey(People.people_id), nullable=False)
     

    def __repr__(self):
        return '<Favorite_people %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "personaje_id": self.people_id
        }
    
class Favorite_planet(db.Model):
    __tablename__ = 'favorite_planet'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey(Planet.planet_id), nullable=False)
        

    def __repr__(self):
        return '<Favorite_planet %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planeta_id": self.planet_id,
        }
