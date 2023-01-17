#import sys
#sys.path.append(".")
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Response
from .database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from .routers import blog, user

from . import schemas, models, hashing


models.Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(blog.router)
app.include_router(user.router)

"""
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""    

@app.get("/")
def index():
    return "hello"


"""
# show all blogs
@app.get("/blog", response_model=list[schemas.ShowBlog], tags=['blog'])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


# add new blog
@app.post("/blog", status_code=status.HTTP_201_CREATED, tags=['blog'])
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog




# show blog by id
@app.get("/blog/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=['blog'])
def show(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"error" : f"Blog with ID {id} not exists"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with ID {id} not exists")
    return blog


# delete
@app.delete("/blog/{id}", tags=['blog'])
def delete_blog(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with ID {id} not exists")
    
    blog.delete(synchronize_session=False)
    db.commit()
    return blog


# update
@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=['blog'])
def update_blog(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with ID {id} not exists")
    print(request)
    blog.update(request.dict())
    db.commit()
    return "updated"


@app.post("/user", tags=['users'])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    password_hash = hashing.Hash.get_password_hash(request.password)
    new_user = models.User(username=request.username, password=password_hash, email=request.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/user/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowUser, tags=['users'])
def show_user(id, response: Response, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not exists")
    return user

"""
