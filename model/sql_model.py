from sqlalchemy.orm import  declarative_base
from sqlalchemy import Column, String, Integer, DateTime, CheckConstraint, ForeignKeyConstraint
import datetime

def get_currtime():
    return datetime.datetime.now()

BASE = declarative_base()

class Books(BASE):
    __tablename__ : str = 'books'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    label = Column(String, nullable=False, index=True)
    author = Column(String, nullable=False,index=True)
    year = Column(Integer, nullable=True,index=True)
    ibsn = Column(String, unique=True, nullable=True)
    value = Column(Integer, default=1)
    __table_args__ = (
        CheckConstraint(value >= 0, name='check_value'),
        {} )
    
    def __init__(self, label, author, year, ibsn=None, value=1):
        self.label = label
        self.author = author
        self.year = year
        self.ibsn = ibsn
        self.value = value

    
class Readers(BASE):
    __tablename__ : str = 'readers'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)    
    name = Column(String, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False)
    comment = Column(String, nullable=True)

    def __init__(self, name, email, comment):
        self.name = name
        self.email = email
        self.comment = comment

class BorrowedBooks(BASE):
    __tablename__ : str = 'borrowedbooks'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True) 
    book_id =  Column(Integer, nullable=False)
    reader_id = Column(Integer, nullable=False)
    borrow_date = Column(DateTime, default=get_currtime())
    return_date = Column(DateTime, default=None)
    ForeignKeyConstraint(['book_id'],['Books.id'])
    ForeignKeyConstraint(['reader_id'],['Readers.id'])


class Users(BASE):
    __tablename__ : str = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)    
    name = Column(String, nullable=False, index=True)
    fullname = Column(String, nullable=False, index=True)
    hashedpassword = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    def __init__(self, name, fullname, hashedpassword, email):
        self.name = name
        self.fullname = fullname
        self.hashedpassword = hashedpassword
        self.email = email
