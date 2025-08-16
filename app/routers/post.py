from .. import models, schemas, utils, database, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import engine, SessionLocal, get_db
from typing import List, Optional
from sqlalchemy import func


router = APIRouter(
    prefix="/posts",
    tags=['posts']
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.PostOut])
def test_post(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    print(search)
    # posts = db.query(models.Post).filter(
    #    models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostReturn)
def create_post(post: schemas.Post, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id,
                           **post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # single_post = db.query(models.Post).filter(models.Post.id == id).first()
    single_post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not single_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} doesn't exist!!")

    return single_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:  int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The item with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action!")

    post_query.delete(synchronize_session=False)
    db.commit()


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, updated_post: schemas.Post, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The item with id: {id} does not exist"
        )

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action!")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
