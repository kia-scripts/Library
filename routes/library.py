import sys
sys.path.append('./')
from fastapi import APIRouter
from model.pydantic_model import Books, Readers
import all_routes
import operations.crud as db

library_route = APIRouter()

@library_route.post(all_routes.book_create)
def new_book(doc: Books):
    doc = dict(doc)
    #return doc
    label = doc['label']
    author = doc['author']
    year = doc['year']
    ibsn = doc['ibsn']
    value = doc['value']
    res = db.add_new_books(label,author,year,ibsn,value)
    return res

@library_route.get(all_routes.books_get_all)
def get_all_books():
    res = db.get_all_books()
    return res

@library_route.get(all_routes.books_by_params)
def get_books_by_param(id: int=None, label: str=None, author: str=None):
    res = db.get_book_by_params(id,label,author)
    return res
