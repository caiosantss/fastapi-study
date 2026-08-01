from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.schemas import Mensagem, UserDB, UserPublic, UserSchema

app = FastAPI(title='FastAPI TOP!')
database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Mensagem)
def read_root():
    return Mensagem(mensagem='Hello World')


@app.get(
    '/hello-world/', status_code=HTTPStatus.OK, response_class=HTMLResponse
)
def render_hello_word():
    return """
        <html>
        <head>
            <title>Sem titulo</title>
        </head>
        <body>
            <h1>Hello World</h1>
            <p>PA!</p>
        </body>
        </html>"""


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)
    database.append(user_with_id)
    return user_with_id
