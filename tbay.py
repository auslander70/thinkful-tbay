from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('postgresql://ubuntu:thinkful@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


from datetime import datetime
from sqlalchemy.sql.expression import func 
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    
    bids = relationship("Bid", backref="item")
    
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
  

Base.metadata.create_all(engine)

# Users
elsa = User(username="Elsa", password="1d1n4")
anna = User(username="Anna", password="b3ll")
kristoff = User(username="Kristoff", password="gr0ff")
session.add_all([elsa, anna, kristoff])
session.commit()

# Items
olaf = Item(name="Olaf", description="snowman", user_id=1)
sven = Item(name="Sven", description="reindeer", user_id=3)
marshmallow = Item(name="Marshmallow", description="snow monster", user_id=2)
baseball = Item(name="baseball", description="rawhide", user_id=3)
session.add_all([olaf, sven, marshmallow, baseball])
session.commit()

# Bids
bid1 = Bid(price=50.0, user_id=elsa.id, item_id=baseball.id)
bid2 = Bid(price=67.0, user_id=anna.id, item_id=baseball.id)
bid3 = Bid(price=80.0, user_id=kristoff.id, item_id=baseball.id)
bid4 = Bid(price=27.0, user_id=elsa.id, item_id=baseball.id)
bid5 = Bid(price=101.0, user_id=anna.id, item_id=baseball.id)
bid6 = Bid(price=99.0, user_id=kristoff.id, item_id=baseball.id)
session.add_all([bid1, bid2, bid3, bid4, bid5, bid6])
session.commit()


records = session.query(Bid).all()

def GetMaxBidRecord(records):
  max_bid = records[0]
  for record in records:
      if record.price > max_bid.price:
        max_bid = record
  return max_bid

max_bid = GetMaxBidRecord(session.query(Bid).all())
print(max_bid.bidder.username, max_bid.price)