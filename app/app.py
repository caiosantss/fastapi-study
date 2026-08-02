from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from app.schemas import UserDB, UserList, UserPublic, UserSchema

app = FastAPI(title='FastApi Study!')
database = []


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)
    database.append(user_with_id)
    return user_with_id


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users():
    return {'users': database}


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
