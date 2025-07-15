from pydantic import BaseModel
from typing import Any, Optional

class DefaultOutput(BaseModel):
    message: Optional[str] = ""
    data: Optional[Any] = {}