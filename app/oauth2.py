from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#SECRET_KEY 
#Algorithm: HS256
#Expiration duration: 

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
  to_encode = data.copy()

  print(datetime.now())
  expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  print(expire)
  to_encode.update({"exp": expire})

  print (to_encode)
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

  return encoded_jwt

def verify_access_token(token: str, credential_exception):

  try:
    print (token)
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    print (payload)
    #id: str = payload.get("user_id")
    id = str(payload.get("user_id"))
    print (id)
    if id is None: 
      raise credential_exception
    print ("hello world2")
    #print (schemas.TokenData(id=id))
    token_data = schemas.TokenData(id=id)
    #token_data = 15
    print (token_data)

  except JWTError:
    #print (e)
    raise credential_exception
  
  print ("returning")
  print (token_data)
  return token_data
  
def get_current_user(token: str = Depends(oauth2_scheme)):

  credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-authenticate": "Bearer"})

  return verify_access_token(token, credential_exception)