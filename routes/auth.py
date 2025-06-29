import sys
sys.path.append('./')
from fastapi import APIRouter, status, Response, Request, Depends, HTTPException
from connection import db_session
import all_routes
from model.pydantic_model import Users, SUserAuth
import operations.crud as db
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import bcrypt

if not hasattr(bcrypt, '__about__'):
    bcrypt.__about__ = type('about', (object,), {'__version__': bcrypt.__version__})

auth_route = APIRouter()

# Секретный ключ для подписи токенов
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"  # Алгоритм подписи
ACCESS_TOKEN_EXPIRE_MINUTES = 3  # Время жизни токена

# Функция для создания JWT-токена
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    auth_data =  {"secret_key": SECRET_KEY, "algorithm": ALGORITHM}
    encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return encode_jwt

# Функция для проверки токена
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None  # Если токен недействителен или истёк

# Настраиваем контекст для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Схема аутентификации
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user_auth")

# Функция для хеширования пароля
def get_password_hash(password):
    return pwd_context.hash(password)

# Функция для проверки пароля
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Аутентификация пользователя
def authenticate_user(name: str, password: str):
    user = db.get_user(name)
    if not user or verify_password(password, user.hashedpassword) is False:
        return None
    return user    

@auth_route.post(all_routes.user_reg)
def add_user(doc: Users):
    doc_type = str(type(doc))
    doc = dict(doc)
    #return doc    
    name = doc['name']
    fullname = doc['fullname']
    hashedpassword = get_password_hash(doc['hashedpassword'])
    email = doc['email']
    res = db.add_user(name,fullname,hashedpassword,email)
    res['input type'] = doc_type
    return res


""" @auth_route.post(all_routes.user_auth)
def login(user_name: str, user_pas: str):
    login_user = authenticate_user(user_name, user_pas)
    if login_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail='Неверый логин или пароль')    
    return {'status':'login sucsess!', 'user': user_name}   """   

@auth_route.post(all_routes.user_auth)
def auth_user(response: Response, user_data: SUserAuth):
    check = authenticate_user(name=user_data.name, password=user_data.password)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Неверный логин или пароль')
    access_token = create_access_token({"sub": str(check.name)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {'access_token': access_token, 'refresh_token': None}

### Использование токена в куках
def get_token(request: Request):
    token = request.cookies.get('users_access_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token not found')
    return token

async def get_current_user(token: str = Depends(get_token)):
    try:
        auth_data =  {"secret_key": SECRET_KEY, "algorithm": ALGORITHM}
        payload = jwt.decode(token, auth_data['secret_key'], algorithms=[auth_data['algorithm']])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен не валидный!')

    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен истек')

    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Не найден ID пользователя')

    user = await UsersDAO.find_one_or_none_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')

    return user