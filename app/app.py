from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select

from app.database import get_session
from app.models import User
from app.schemas import UserDB, UserList, UserPublic, UserSchema

app = FastAPI(title='FastApi Study!')
database = []


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(
    user: UserSchema,
    session=Depends(get_session),  # noqa: B008
):

    db_user: User | None = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='Email already exists'
            )
        elif db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username already exists',
            )

    db_user = User(
        username=user.username, email=user.email, password=user.password
    )
    session.add(instance=db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def get_users(
    limit = 10,
    offset = 0,
    session=Depends(get_session)
):  # noqa: B008
    users_db = session.scalars(
        select(User)
        .limit(limit)
        .offset(offset)
    )
    return {'users': users_db}


@app.get(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def get_user_id(user_id: int):
    try:
        return database[user_id - 1]
    except IndexError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )


@app.put(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(user_id: int, user: UserSchema):
    update_user_with_id = UserDB(**user.model_dump(), id=user_id)

    try:
        database[update_user_with_id.id - 1] = update_user_with_id
    except IndexError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return update_user_with_id


@app.delete(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def delete_user(user_id: int):
    try:
        return database.pop(user_id - 1)
    except IndexError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
