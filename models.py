import os
from sqlalchemy import Column
from flask_sqlalchemy import SQLAlchemy

database_path = os.environ['DATABASE_URL']
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
    db.create_all()


'''
Movies
'''
class Movies(db.Model):  
  __tablename__ = 'movies'

  id = Column(db.Integer, primary_key=True)
  title = Column(db.String(120))
  release_date = Column(db.String(120))
  

  def __init__(self, title, release_date):
    self.title = title
    self.release_date = release_date

  def format(self):
    return {
      'id': self.id,
      "title": self.title,
      'release_date': self.release_date
    }
  
'''
Actors
'''
class Actors(db.Model):  
  __tablename__ = 'actors'

  id = Column(db.Integer, primary_key=True)
  name = Column(db.String(120))
  age = Column(db.Integer)
  gender = Column(db.String(120))
  

  def __init__(self, name, age, gender):
    self.name = name
    self.age = age
    self.gender = gender

  def format(self):
    return {
      'id': self.id,
      'age': self.age,
      'gender': self.gender
    }
