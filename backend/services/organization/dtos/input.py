import re

from pydantic import BaseModel, Field
from typing import Optional

from services.organization.dtos.custom_types import OrganizationName


class CreateOrganization(BaseModel):
    admin_id: Optional[int] = None
    name: OrganizationName

class CheckOrganizationName(BaseModel):
    name: OrganizationName

class UpdateOrganization(BaseModel):
    id: int = Field(...)
    name: OrganizationName

class GetOrganization(BaseModel):
    name: OrganizationName

