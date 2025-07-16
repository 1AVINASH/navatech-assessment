from typing import List

from fastapi import HTTPException, status
from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError

from infra.postgres.setup import db

from utility.logger import app_logger
from services.organization.dtos.input import CreateOrganization, UpdateOrganization
from services.organization.dtos.custom_types import OrganizationName
from services.organization.models import Organization as OrganizationModel


class Organization:
    @staticmethod
    async def get_all_organizations()-> List[OrganizationModel]:
        query = "SELECT * FROM organization order by created_at"
        app_logger.debug(f"Db Url from inside organization {db.url}") 
        data = await db.fetch_all(query)

        return [OrganizationModel(**row) for row in data]
    
    @staticmethod
    async def get_organization_by_name(organization_name: OrganizationName)->OrganizationModel:
        query = "SELECT * FROM organization where name=:name"
        values = {"name": organization_name}
        data = await db.fetch_one(query, values=values)

        return OrganizationModel(**data)
    
    @staticmethod
    async def create_organization(organization: CreateOrganization)->OrganizationModel:
        query = "INSERT INTO organization (name, admin_id) VALUES (:name, :admin_id) returning id"
        values = organization.model_dump()
        try:
            new_organization_id = await db.fetch_val(query=query, values=values)
            data = OrganizationModel(**values)
            data.id = new_organization_id
        except ForeignKeyViolationError as e:
            raise ValueError(f"Admin with id {organization.admin_id} does not exist") from e
        except UniqueViolationError:
            # Catch the specific PostgreSQL unique constraint violation error
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, # 409 Conflict is appropriate for this
                detail=f"Organization with name '{organization.name}' already exists."
            )

        return data
    
    @staticmethod
    async def update_organization(organization: UpdateOrganization):
        query = "UPDATE organization set name=:name where id=:id"
        values = organization.model_dump()
        app_logger.debug(f"Query and value for updating organization {values} \n {query}")
        data = await db.execute(query=query, values=values)

        return data
    
    @staticmethod
    async def delete_organization(organization_id: int):
        query = "DELETE from organization where id=:id;"
        values = {"id": organization_id}
        data = await db.execute(query=query, values=values)

        return data
    