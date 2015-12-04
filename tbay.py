from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('postgresql://ubuntu:thinkful@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    
    bids = relationship("Bid", backref="bids")
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    
class User(Base):
  __tablename__ = "users"
  
  id = Column(Integer, primary_key=True)
  username = Column(String, nullable=False)
  password = Column(String, nullable=False)
  
  items = relationship("Item", backref="seller")
  bids = relationship("Bid", backref="bidder")
  

class Bid(Base):
  __tablename__ = "bids"
  
  id = Column(Integer, primary_key=True)
  price = Column(Float, nullable=False)
  
  user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
  item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
  

"""
# Users
elsa = User(username="Elsa", password="1d1n4")
anna = User(username="Anna", password="b3ll")
kristoff = User(username="Kristoff", password="gr0ff")

# Items
olaf = Item(name="Olaf", description="snowman", user_id=1)
sven = Item(name="Sven", description="reindeer", user_id=3)
marshmallow = Item(name="Marshmallow", description="snow monster", user_id=2)
baseball = Item(name="baseball", description="rawhide", user_id=3)

# Bids
bid1 = Bid(price=50.0, user_id=1, item_id=4)
bid2 = Bid(price=67.0, user_id=2, item_id=4)





"""


Base.metadata.create_all(engine)

