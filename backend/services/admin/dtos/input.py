import re

from pydantic import BaseModel, Field, EmailStr
from typing import Optional

from services.admin.dtos.custom_types import UserPassword


class CreateAdmin(BaseModel):
    email: EmailStr = Field(...)
    password: UserPassword

class UpdateAdmin(BaseModel):
    id: int = Field(...)
    email: EmailStr = Field(...)
    password: UserPassword

class GetAdmin(BaseModel):
    id: int = Field(...)

class Login(BaseModel):
    email: EmailStr = Field(...)
    password: UserPassword
