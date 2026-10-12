from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_session
from app.models import User
from app.schemas import Message, UserList, UserPublic, UserSchema
from app.security import get_hash, verify_hash_password

app = FastAPI(title='FastApi Study!')


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(
    user: UserSchema,
    session: Session = Depends(get_session),
):
    db_user: User | None = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user and (
        (db_user.email == user.email) or (db_user.username == user.username)
    ):
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or email already exists',
        )

    hashed_password = get_hash(user.password)

    db_user = User(
        username=user.username, email=user.email, password=hashed_password
    )
    session.add(instance=db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(
    limit=10,
    offset=0,
    session: Session = Depends(get_session),
):
    users_db = session.scalars(select(User).limit(limit).offset(offset))

    return {'users': users_db}


@app.get(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def read_user_id(
    user_id: int,
    session: Session = Depends(get_session),
):
    user_db: User | None = session.scalar(
        select(User).where(User.id == user_id)
    )

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User does not exist'
        )
    return user_db


@app.put(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(
    user_id: int,
    user: UserSchema,
    session: Session = Depends(get_session),
):
    user_db: User | None = session.scalar(
        select(User).where(User.id == user_id)
    )

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User does not exist'
        )

    try:
        user_db.username = user.username
        user_db.email = user.email
        user_db.password = get_hash(user.password)

        session.add(user_db)
        session.commit()

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or email already exists',
        )

    return user_db


@app.delete(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=Message,
)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user: User | None = session.scalar(
        select(User).where(User.id == user_id)
    )

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User does not exist'
        )

    session.delete(db_user)
    session.commit()

    return {'message': 'User deleted successfully'}


# Nomenclaturas seguem o padrão oficial do FastAPI com OAuth2
@app.post('/token')
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):

    db_user: User | None = session.scalar(
        select(User).where(User.email == form_data.username)
    )

    # Verifica email
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )

    # Verifica hash da senha
    if not (
        verify_hash_password(
            plain_password=form_data.password, hash_password=db_user.password
        )
    ):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )

    # Se passar, criamos token JWT e enviamos o token para o cliente

    # retorna 200 ou 201
