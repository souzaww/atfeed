from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from flask_login import UserMixin
import datetime, feedparser
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
engine = create_engine('sqlite:///database.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

#função para criar as tabelas no banco de dados
def create_db():
    Base.metadata.create_all(engine)
    #verifica se já existe um usuário 'admin' no banco de dados
    user = session.query(User).filter_by(email='admin').first()
    if user is None:
        user = User(email='admin', firstName='admin', password='admin')
        session.add(user)
        session.commit() 

class User(Base, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String(150), unique=True)
    firstName = Column(String(150))
    password = Column(String(150))
    notes = relationship('Note')
    feeds = relationship('Feed')

    def __repr__(self):
        return f"User(email='{self.email}', firstName='{self.firstName}')"
            
class Feed(Base):
    __tablename__ = 'feed'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    feed_url = Column(String(200), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    feed_items = relationship('FeedItem')

    def __repr__(self):
        return f"Feed(name='{self.name}', feed_url='{self.feed_url}')"
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
class FeedItem(Base):
    __tablename__ = 'feed_item'

    id = Column(Integer, primary_key=True)
    sku = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    price = Column(String(20), nullable=False)
    sale_price = Column(String(20))
    sale_price_effective_date = Column(DateTime)
    installment_months = Column(Integer)
    installment_amount = Column(String(20))
    description = Column(String(1000))
    link = Column(String(1000))
    image_link = Column(String(1000))
    condition = Column(String(100))
    availability = Column(String(100))
    brand = Column(String(100))
    gtin = Column(String(100))
    mpn = Column(String(100))
    google_product_category = Column(String(100))
    product_type = Column(String(100))
    shipping = Column(String(100))
    custom_label_0 = Column(String(100))
    custom_label_1 = Column(String(100))
    custom_label_2 = Column(String(100))
    custom_label_3 = Column(String(100))
    custom_label_4 = Column(String(100))
    feed_id = Column(Integer, ForeignKey('feed.id'))

    def __repr__(self):
        return f"FeedItem(sku='{self.sku}, name='{self.name}', price='{self.price}')"
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    

class Note(Base):
    __tablename__ = 'note'

    id = Column(Integer, primary_key=True)
    data = Column(String(10000))
    user_id = Column(Integer, ForeignKey('user.id'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def __repr__(self):
        return f"Note(data='{self.data}')"
    def as_dict(self):
        as_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}


    
class Queries(): 
    ### DATABASE FUNCTIONS
    ## Create database
    # função para criar as tabelas acima no banco de dados

    
    ## User functions
    #função para consultar id do usuário
    @staticmethod
    def get_user_by_id(id):
        return session.query(User).get(int(id))
    
    #adiciona user no banco de dados
    @staticmethod
    def add_user_to_db(email, firstName, password):
        new_user = User(email=email, firstName=firstName, password=password)
        session.add(new_user)
        session.commit()
        return new_user
    
    #filtra usuario por email
    @staticmethod
    def get_user_by_email(email):
        return session.query(User).filter_by(email=email).first()
    

    ## Note functions
    #add note to database
    @staticmethod
    def add_note_to_db(note, user_id):
        new_note = Note(data=note, user_id=user_id)  #providing the schema for the note 
        session.add(new_note) #adding the note to the database 
        session.commit()
        return new_note
    

    ## Feed functions
    #add feed to database
    @staticmethod
    def add_feed_to_db(name, feed_url, user_id):
        new_feed = Feed(name=name, feed_url=feed_url, user_id=user_id)
        session.add(new_feed)
        session.commit()
        return new_feed
    
    #get feed by id
    @staticmethod
    def get_feed_by_id(feed_id):
        return session.query(Feed).get(int(feed_id)) 
    
    ## FeedItem functions
    #add temp_item from process_feed to database
    @staticmethod
    def add_item_to_db(temp_item, feed_id):
        new_item = FeedItem(sku=temp_item['sku'], name=temp_item['name'], price=temp_item['price'], link=temp_item['link'], feed_id=feed_id)
        session.add(new_item)
        session.commit()
        return new_item
    
##Cria funções de feedparser/xmltodict para processar o feed
class FeedParser():
    @staticmethod
    def parse_xml_feed(add_item):
        feed_items_parse = feedparser.parse(add_item)
        return feed_items_parse
    
 

