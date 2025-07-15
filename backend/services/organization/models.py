import datetime

from pydantic import BaseModel
from typing import Optional
from services.organization.dtos.custom_types import OrganizationName

class Organization(BaseModel):
    id: Optional[int] = None
    name: OrganizationName
    admin_id: int