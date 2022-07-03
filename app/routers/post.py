from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models,schemas,oauth2
from ..database import get_db

router = APIRouter( 
    prefix="/posts",
    tags=['Posts']
)
#NOTE: HE MADE ALL POSTS ENDPOINT PUBLIC (NOT POSTS SPECIFIC TO THE USER)
#get all the posts 
@router.get("/", response_model=List[schemas.Post])
#whatever type of you put for the dependency returns doesn't matter 
#limit - brings back only a certain number of posts but max 10 
#skip - skips over posts (useful for pagination)
def get_posts(db: Session = Depends(get_db), current_user: object = Depends(oauth2.get_current_user),
limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    #grab every entry in the post table and performs a query 
    #posts = db.query(models.Post).all()

    #posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).all()
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

#adding a new post
@router.post("/", status_code=status.HTTP_201_CREATED) #by default send a 201 status code 
#added a dependency saying the user has to be logged in (oauth2) 
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: object = Depends(oauth2.get_current_user)): 
    #create a new post with the model 
    #new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(user_id=current_user.id, **post.dict()) #the ** helps us avoid typing it all out like above 
    db.add(new_post)
    #commit the changes 
    db.commit()
    #to get the return post 
    db.refresh(new_post)

    return new_post

@router.get("/{id}", response_model=schemas.Post)
#still want it as an int to make sure the type validation for the route works (user doesn't type in the route incorrectly)
#don't use .all() because it will keep looking for all matches, we know it only exists once 
def get_posts(id: int, db: Session = Depends(get_db), current_user: object = Depends(oauth2.get_current_user)): 
    #print(current_user.email)
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post: 
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    return  post

#for delete technically you shouldn't send any data back for 204
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db: Session = Depends(get_db), current_user: object = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    #return the first 
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    #making sure the user is only deleting their own posts 
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")

    #read docs to understand this 
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),current_user: object = Depends(oauth2.get_current_user)):
    #set up a query to find the post with the specific id 
    post_query = db.query(models.Post).filter(models.Post.id == id)
    #grab the post 
    post = post_query.first()
    #if it doesn't exist 
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")

    #chaining to the query method
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    #return the updated post 
    return post_query.first()