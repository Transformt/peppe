from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
from sqlalchemy import *
import datetime
import md5
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import relationship, backref
from database import Base
import time




class User(Base):
  __tablename__ = 'signup'
  id = Column(Integer, primary_key = True)
  firstname = Column(String(100))
  lastname = Column(String(100))
  phone = Column(String(15), unique=True)
  country_id = Column(Integer)
  email = Column(String(120), unique=True)
  pwdhash = Column(String(15))
  post = relationship('Post', backref='signup', lazy='dynamic')
  wallet = relationship('Wallet', backref="signup", lazy='dynamic')
  stock = relationship('Stock', backref="signup", lazy='dynamic')
  
   
  def __init__(self, firstname, lastname, phone, country_id, email, pwdhash):
    self.firstname = firstname.title()
    self.lastname = lastname.title()
    self.phone = phone
    self.country_id = country_id
    self.email = email.lower()
    self.pwdhash = pwdhash.lower()
    
   
  
    
  def set_password(self, password):
    self.pwdhash = generate_password_hash(password)
  
  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)
      
  def __repr__(self):
    return '<user %r="">' % (self.firstname, self.lastname, self.phone, self.country_id, self.email)
    
    
class Post(Base):
  __tablename__ = 'posts'
  uid = Column(Integer, primary_key = True)
  subject = Column(String(30))
  simage = Column(String(400))
  body = Column(String(200))
  timestamp = Column(DateTime(timezone=True))
  user_id = Column(Integer, ForeignKey('signup.id'))
  author = Column(String(50))
  
  
  
  def __init__(self, subject, simage, body, timestamp=None, user_id=None, author=None):
        self.subject = subject.title()
        self.simage = simage
        self.body = body.lower()
        self.timestamp = datetime.datetime.now()
        self.user_id = user_id
        self.author = author
        
        
        
  
  def __repr__(self):
    return '<Post %r %r %r %r>' % (self.subject, self.body, self.simage, self.author)
    
    
    
class Wallet(Base):
  __tablename__ = 'wallet'
  id = Column(Integer, primary_key = True)
  ownuser_id = Column(Integer, ForeignKey('signup.id'))
  amount = Column(Float, default=1000.0)
  squestion = Column(String(100))
  sanswer = Column(String(100))
  
  def __init__(self, ownuser_id, squestion, sanswer, amount):
    self.ownuser_id = ownuser_id
    self.squestion = squestion
    self.sanswer = sanswer
    self.amount = amount
    
    
  def __repr__(self):
    return '<Wallet %r %r %r %r>' % (self.squestion, self.sanswer, self.amount)
    
    
  
class Stock(Base):
  __tablename__ = 'stock'
  item_id = Column(Integer, primary_key = True)
  owner_id = Column(Integer, ForeignKey('signup.id'))
  owner_last = Column(String(100))
  owner_email = Column(String(120))
  itemname = Column(String(100))
  num_of_item = Column(Integer)
  itemprice = Column(String(100))
  
  
  def __init__(self, owner_id, owner_last, owner_email, itemname, num_of_item, itemprice):
    self.owner_id = owner_id
    self.owner_last = owner_last.title()
    self.owner_email = owner_email.lower()
    self.itemname = itemname
    self.num_of_item = num_of_item
    self.itemprice = itemprice
    
  def __repr__(self):
    return '<Wallet %r %r %r %r %r>' % (self.owner_last, self.owner_email, self.itemname, self.num_of_item, self.itemprice)
    
   
    
#class Image(Base):
#  __tablename__ = 'stockimage'
#  picsid = Column(Integer, primary_key=True)
#  description = Column(String(200))
#  simage = Column(String(400))
  
#  def __init__(self, description, simage):
#    self.description = description
#    self.simage = simage
    
#  def __repr__(self):
#    return 'Image %r' % (self.description, self.image)    
   
    
