from pydantic import BaseModel
from typing import List, Union


class BlogBase(BaseModel):
    title: str
    body: str


class Blog(BlogBase):
    class Config():
        orm_mode = True
  


class User(BaseModel):
    username: str
    password: str
    email: str


class ShowUser(BaseModel):
    username: str
    email: str
    blogs: List[Blog] = []

    class Config():
        orm_mode = True


class ShowUserSimple(BaseModel):
    username: str
    email: str

    class Config():
        orm_mode = True



class ShowUserWithPassword(ShowUserSimple):
    password: str



class ShowBlog(Blog):
    title: str
    body: str
    creator: ShowUserSimple


class Login(BaseModel):
    username: str
    password: str



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None