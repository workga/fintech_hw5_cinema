from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.engine.row import Row

from app.cinema.crud.utils import handle_db_exception
from app.cinema.models import User
from app.cinema.pagination import Page, paginated_stmt
from app.cinema.schemas.users import UserCreate
from app.cinema.security import hash_password
from app.database import create_session


def get_user(user_id: int) -> Row:
    with create_session() as session:
        db_user = session.execute(select(User).where(User.id == user_id)).one_or_none()
        return db_user


@handle_db_exception
def get_user_by_login(login: str) -> Optional[User]:
    with create_session() as session:
        db_user = session.execute(select(User).where(User.login == login)).one_or_none()

        return db_user.User if db_user else None


@handle_db_exception
def get_user_by_id(user_id: int) -> Optional[User]:
    db_user = get_user(user_id)

    return db_user.User if db_user else None


@handle_db_exception
def get_users(page: Page = Page()) -> List[User]:
    with create_session() as session:
        db_users = session.execute(paginated_stmt(select(User), page, User)).all()

        return [u.User for u in db_users]


@handle_db_exception
def create_user(user: UserCreate) -> User:
    with create_session() as session:
        if get_user_by_login(user.login):
            raise HTTPException(status_code=400, detail='Login already registered')

        user.password = hash_password(user.password)
        db_user = User(**user.dict())

        session.add(db_user)

        return db_user
