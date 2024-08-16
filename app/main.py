from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine, get_db
from .routers import post, user, auth, vote
from .config import settings

# create database objects based on the models, with alembic, this is redundant
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True
    # rating: Optional[int] = None

# my_posts = [{"title": "title 1", "content": "content 1", "id": 1}, {"title": "favortie food", "content": "pizza", "id": 2}]

# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p

# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i
#     return None

origins = [
#    "https://www.google.com",
#     "http://localhost",
#     "http://localhost:8080",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(vote.router)
app.include_router(auth.router)
        
@app.get("/")
def root():
    return {"message": "Hello buds: we are hosted"}
