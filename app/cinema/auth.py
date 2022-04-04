from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.cinema import crud
from app.cinema.models import User
from app.cinema.security import verify_password

base_auth = HTTPBasic()


def auth_user(credentials: HTTPBasicCredentials = Depends(base_auth)) -> User:
    user = crud.users.get_user_by_login(credentials.username)

    if not user or not verify_password(user.password, credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Basic'},
        )

    return user
