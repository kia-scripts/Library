from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model.sql_model import BASE

db_user: str = 'postgres'
db_port: int = 5432
db_host: str = 'localhost'
db_password: str = '12345'

uri: str = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/library?client_encoding=utf8'
print(uri)
engine = create_engine(uri, client_encoding='utf8')
BASE.metadata.create_all(bind = engine)

session = sessionmaker(
    bind = engine,
    autoflush= True
)

db_session = session()

try:
    connection = engine.connect()
    connection.close()
    print('Connected')
except Exception as e:
    print('Connect error:', str(e))