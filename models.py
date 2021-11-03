from sqlalchemy import Column, String, create_engine ,Integer, Date
from flask_sqlalchemy import SQLAlchemy
import os
import json
import dateutil.parser
import babel
from babel.dates import format_date, format_datetime, format_time

from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

database_name ='casting_agency'
default_database_path= "postgres://{}:{}@{}/{}".format('postgres', 'password', 'localhost:5432', database_name)
database_path = os.getenv('DATABASE_URL', default_database_path)
if database_path.startswith("postgres://"):
     database_path = database_path.replace("postgres://", "postgresql://", 1)
db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.create_all()

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

def format_date(value, format='medium'):
        date = dateutil.parser.parse(value)
        if format == 'full':
            format="EEEE MMMM, d, y 'at' h:mma"
        elif format == 'medium':
            format="EE MM, dd, y "
        return babel.dates.format_date(date, format, locale='en')

'''
Movies
Have title and release Date
'''
class Movies(db.Model):

    # Autoincrementing, unique primary key
    id = Column(Integer, primary_key=True)
    # String Title
    title = Column(String(80), unique=True)
    # Datetime release date 
    release_date = Column(Date, nullable=False)
    actors = relationship('Actors', backref='movies')

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date


    def format(self):
        formatted_actors=[actor.name.format() for actor in self.actors]

        return [{
            'id': self.id,
            'title': self.title,
            'release_date':  format_date(str(self.release_date)),
            'actors': formatted_actors

            }]

    
    
    def insert(self):
        db.session.add(self)
        db.session.commit()


    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def update(self):
        db.session.commit()      

'''
Actors 
Have name, age and gender
'''
class Actors(db.Model):  

    # Autoincrementing, unique primary key
    id = Column(Integer, primary_key=True)
    # String name
    name = Column(String ,nullable=False)
    # Integer age
    age = Column(Integer)
    # String gender
    gender = Column(String)
    movie_id= Column(Integer, ForeignKey('movies.id'))

    def __init__(self, name, age,gender):
        self.name = name
        self.age = age
        self.gender = gender


    def format(self):
        return [{
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            }]

    def insert(self):
        db.session.add(self)
        db.session.commit()

    

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def update(self):
        db.session.commit()