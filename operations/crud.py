import sys
sys.path.append('./')
from fastapi import FastAPI, HTTPException, Depends
from connection import db_session
from model.sql_model import Users,Books, Readers, BorrowedBooks
import decoders.books as decoder


def get_user(name):
    existing_user = db_session.query(Users).filter(Users.name == name).first()
    return existing_user

def add_user(name, fullname, hashedpassword, email):
    existing_user = db_session.query(Users).filter(Users.name == name).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")    
    try:        
        new_row = Users(name, fullname, hashedpassword, email)
        db_session.add(new_row)   
        db_session.commit()
        return { 
            'status': 'ok',
            'data': 'User succefully added'
        }        
    except Exception as e:
        return {
            'status': 'error user adding',
            'data:': str(e)
        }

def add_new_books(name, author, year, ibsn=None , value=1):
    try:        
        new_row = Books(name, author, year, ibsn, value)
        db_session.add(new_row)   
        db_session.commit()
        return { 
            'status': 'ok',
            'data': 'Succefully added'
        }        
    except Exception as e:
        return {
            'status': 'error record adding',
            'data:': str(e)
        }

def get_all_books():
    try:
        res = db_session.query(Books).all()
        docs = decoder.decode_books(res)
        return { 
            'status': 'ok',
            'data': docs
        }
    except Exception as e:
        return {
            'status': 'error',
            'data:': str(e)
        }

def get_book_by_params(id=None, label=None, author=None):
    criteria = {'id': id} if id != None else dict()
    if label != None:
        criteria['label'] = label.replace('\'','')
    if author != None:
        criteria['author'] = author.replace('\'','')
    #return criteria
    try:
        res = db_session.query(Books).filter_by(**criteria).all()
        docs = decoder.decode_books(res)
        if docs:            
            return { 
                'status': 'ok',
                'data': docs
            }
        else:
            return { 
                'status': 'error',
                'data': f'Record with label = {label} , author = {author}, id ={id} not exists!'
            }
    except Exception as e:
        return {
            'status': 'error',
            'data:': str(e)
        }

# Update BOOK record  by id
def update_book_by_id(id, label=None, author=None, year=None , ibsn=None, value=None):
    criteria = {'id': id }
    fields = dict()
    if label != None:
        fields['label'] = label
    if author != None:
        fields['author'] = author
    if year != None:
        fields['year'] = year
    if ibsn != None:
        fields['ibsn'] = ibsn
    if value != None:
        fields['value'] = value 

    try:
        if not fields:
            raise Exception('Update params empty!')
        res = db_session.query(Books).filter_by(**criteria).update(fields, synchronize_session = 'fetch')
        db_session.commit()
        if res != None:
            return { 
                'status': 'updated ok',
                'records updated': res
            }
        else:
            return { 
                'status': 'error',
                'data': f'Record with id = {id} not exists!'
            }
    except Exception as e:
        return {
            'status': 'update error',
            'data:': str(e)
        }

# Delete BOOK by id
# Update BOOK record  by id
def delete_book_by_id(id):
    criteria = {'id': id }
    try:
        res = db_session.query(Books).filter_by(**criteria).one()
        print(res)
        db_session.delete(res)
        db_session.commit()
        if res != None:
            return { 
                'status': 'ok',
                'records ': 'Record {res} deleted'
            }
        else:
            return { 
                'status': 'delete error',
                'data': f'Record with id = {id} not exists!'
            }
    except Exception as e:
        return {
            'status': 'delete  error',
            'data:': str(e)
        }



#add_new_books('Вий', 'Гоголь',1898)
#res = get_all_books()
#res = get_book_by_params( id = 7, label = 'Вий', author = 'Гоголь')

#res = update_book_by_id(4, 'Новая книга', year = 2000)
#res = delete_book_by_id(4)
#print(res)
    
    

