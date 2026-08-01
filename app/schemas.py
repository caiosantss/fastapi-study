from pydantic import BaseModel, EmailStr


class Mensagem(BaseModel):
    mensagem: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserDB(UserSchema):
    id: int


class UserPublic(BaseModel):
    username: str
    email: EmailStr
    id: int
