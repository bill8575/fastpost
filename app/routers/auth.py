from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models, schemas, utils, oauth2
from sqlalchemy.orm import Session

from .. import database
router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token)
# def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):  

  # from RequestForm
  # username
  # password
  # user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
  user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
  
  if not utils.verify(user_credentials.password, user.password):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
  
  # create a token
  # return token
  access_token = oauth2.create_access_token(data = {"user_id": user.id})
  return {"access_token": access_token, "token_type": "bearer"}