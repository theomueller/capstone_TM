import os
from datetime import datetime
from sqlalchemy import Column, String, Integer
from sqlalchemy.sql.expression import null
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)


db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app,database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db_drop_and_create_all()



'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have
     multiple verisons of a database
'''


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    # add one demo row which is helping in POSTMAN test
    movie1 = Movie(title='Big Blue')
    movie1.insert()
    movie2 = Movie(title='The 5th Element')
    movie2.insert()
    actor1 = Actor(name='John Doe')
    actor1.insert()
    actor2 = Actor(name='John Smith')
    actor2.insert()
    role = Role(movie_id=movie1.id, actor_id= actor1.id)
    role.insert()
    role = Role(movie_id=movie1.id, actor_id= actor2.id)
    role.insert()
    role = Role(movie_id=movie2.id, actor_id= actor2.id)
    role.insert()
   

'''
TABLES
Movies with attributes title and release date
Actors with attributes name, gender 
Roles associates actors with movies
'''

# Table MOVIE
class Movie(db.Model):
    __tablename__='movies'
    id = Column(db.Integer, primary_key=True)
    title = Column(db.String(80), unique=True)
    release = Column(db.DateTime, default=datetime.utcnow)
    actors = db.relationship('Actor',secondary="roles",back_populates="movies")
    #roles = db.relationship('Role', backref=db.backref('movie'), lazy='joined')

    def __init__(self,title):
        self.title=title

    def __repr__(self):
        return json.dumps(self.short())

    '''
    short()
        short form representation of the movie without date
    '''
    def short(self):
        return {
            'id': self.id,
            'name':self.title,
            'actors': [actor.name for actor in self.actors]
            }

    '''
    insert()
        inserts a new model into a database
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            movie = Movies.query.filter(movie.id == id).one_or_none()
            movie.title = 'Black Coffee'
            movie.update()
    '''
    def update(self):
        db.session.commit()

  

class Actor(db.Model):
    __tablename__ = "actors"
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String, nullable=False)
    age = Column(db.Integer)
    gender = Column(db.String)
    movies = db.relationship('Movie', secondary="roles",back_populates="actors")
    #roles = db.relationship('Role', backref=db.backref('actor'), lazy='joined')

    def __repr__(self):
        return f"<Actor {self.id} name:{self.name}>"

    '''
    short(): short form representation of the movie without date
    '''
    def short(self):
        return {
            'id': self.id,
            'name':self.name
            }

    '''
    insert(): inserts a new model into a database
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete(): deletes a new model into a database
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update(): updates a new model into a database
    '''
    def update(self):
        db.session.commit()

class Role(db.Model):
    __tablename__ = "roles"

    __mapper_args__ = {
        'confirm_deleted_rows': False
    }

    id = Column(db.Integer, primary_key=True)
    movie_id = Column(db.Integer, db.ForeignKey('movies.id'))
    actor_id = Column(db.Integer, db.ForeignKey('actors.id'))
    #movie = db.relationship(Movie, backref=db.backref("roles", cascade="all, delete-orphan"),overlaps="actors,movies")
    #actor = db.relationship(Actor, backref=db.backref("roles",cascade="all, delete-orphan"),overlaps="actors,movies")
   
    def __repr__(self):
        return f"<Role {self.id}>"

    '''
    short(): short form representation of the role
    '''
    def short(self):
        return {
            'id': self.id,
            'movie':self.movie,
            'actor': self.actor
            }
    '''
    insert(): inserts a new model into a database
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete(): deletes a new model into a database
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update(): updates a new model into a database
    '''
    def update(self):
        db.session.commit()