from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.schemas import Mensagem

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Mensagem)
def read_root():
    return Mensagem(mensagem='Hello World')


@app.get('/page', status_code=HTTPStatus.OK, response_class=HTMLResponse)
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
