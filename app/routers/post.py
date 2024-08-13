from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
# @router.get("/")
# def get_posts():
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # return {"data": "These are your posts"}
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).all()
    # print(current_user.id)
    # posts = db.query(models.Post).filter(models.Post.owner_id == int(current_user.id)).all()
    # posts = db.query(models.Post).filter(
    #     models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts_query = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id)
    posts = posts_query.filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print (posts_query)
    # print(posts)
    #return {"data": my_posts}
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
#def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #print(post)
    #print(post.__dict__)
    #print(new_post.dict())
    #return {"new_post": f"title: {payload['title']}, content: {payload['content']}"}
    # post_dict = post.model_dump();
    # post_dict['id'] = randrange(0, 1000000)
    # print(post_dict)
    #my_posts.append(post.__dict__)
    # my_posts.append(post_dict)

    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    print(post.model_dump())
    print('current_user.id = ', current_user.id)
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(
        owner_id=current_user.id, 
        **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    # return {"data": new_post}
    return new_post

# title str, content str

@router.get("/{id}", response_model=schemas.PostOut)
# @router.get("/{id}", response_model=schemas.Post)
# def get_post(id: int, response: Response):
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):    
    # print(id)
    # post = find_post(id)
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # found_post = cursor.fetchone()

    # found_post = db.query(models.Post).filter()
    # found_post = db.query(models.Post).filter(models.Post.id == id).first()
    found_post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    # print(found_post)
    if not found_post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} NOT Found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} NOT Found")
    #return {"post_detail": f"This get a post {id}"} 
    # return {"data": found_post}

    # if found_post.owner_id != int(current_user.id):
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
    #                         detail=f"not authorized to display post with id: {id}")

    return found_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(id)
    # index = find_index_post(id)
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # print(deleted_post)
    # conn.commit()
    # print(index)
    # if index == None:

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    # if deleted_post == None:
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    
    # print('owner_id: ', post.owner_id)
    # print('current_user.id: ', int(current_user.id))
    if post.owner_id != int(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"not authorized to delete post with id: {id}")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    # my_posts.pop(index)
    #return {"message": "post was successfully removed"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # index = find_index_post(id)

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()

    
    # conn.commit()
    # print(index)
    post_query = db.query(models.Post).filter(models.Post.id == id)

    update_post = post_query.first()
    print(update_post)
    if update_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    # post_dict = post.model_dump()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    # return {"data": post_dict}
    # post_query.update({'title':'updated title', 'content':'updated content'}, synchronize_session=False)

    if update_post.owner_id != int(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"not authorized to update post with id: {id}")
   
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    #return {"data": update_post} 
    #return {"data": "success"} 
    # return {"data": post_query.first()} 
    return post_query.first() 