from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from . import token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token2: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    return token.verify_token(token2, credentials_exception)