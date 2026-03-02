from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    correo: str
    nombres: str
    apellidos: str
    telefono: str


class UserCreate(UserBase):
    password: str = Field(..., min_length=1)
    frase_seguridad: str = Field(..., min_length=1)


class UserUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    telefono: Optional[str] = None
    password: Optional[str] = Field(default=None, min_length=1)


class UserResponse(UserBase):
    id: int
    fecha_registro: datetime


class UserInDB(UserResponse):
    contrasenia_hash: str
    frase_seguridad_hash: str


class UserLogin(BaseModel):
    correo: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenPayload(BaseModel):
    sub: str
    correo: str
    exp: int

class PasswordResetRequest(BaseModel):
    correo: str
    frase_seguridad: str = Field(..., min_length=1)

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(..., min_length=6)

class PasswordResetRequestResponse(BaseModel):
    message: str
    token: Optional[str] = None