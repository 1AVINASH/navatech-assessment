import datetime

from pydantic import BaseModel, Field
from typing import Optional
from services.admin.dtos.custom_types import UserPassword

class Admin(BaseModel):
    id: Optional[int] = None
    email: str
    password: UserPassword