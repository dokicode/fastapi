from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, database, models


router = APIRouter()
get_db = database.get_db

# show all blogs
@router.get("/blog", response_model=list[schemas.ShowBlog], tags=['blog'])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


# add new blog
@router.post("/blog", status_code=status.HTTP_201_CREATED, tags=['blog'])
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# show blog by id
@router.get("/blog/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=['blog'])
def show(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"error" : f"Blog with ID {id} not exists"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with ID {id} not exists")
    return blog


# delete
@router.delete("/blog/{id}", tags=['blog'])
def delete_blog(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with ID {id} not exists")
    
    blog.delete(synchronize_session=False)
    db.commit()
    return blog


# update
@router.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=['blog'])
def update_blog(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with ID {id} not exists")
    print(request)
    blog.update(request.dict())
    db.commit()
    return "updated"