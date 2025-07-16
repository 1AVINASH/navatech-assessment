from typing import List

from fastapi import HTTPException, status
from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError

from infra.postgres.setup import db
from infra.elasticsearch.setup import get_es_client

from utility.logger import app_logger
from services.organization.dtos.input import CreateOrganization, UpdateOrganization
from services.organization.dtos.custom_types import OrganizationName
from services.organization.models import Organization as OrganizationModel, OrganizationSearchByName


class Organization:
    _es_client = None

    async def get_client(self):
        if self._es_client is None:
            self._es_client = await get_es_client()
        return self._es_client

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
    

    # Elastic Search Queries start from here
    async def search_organization_by_name(self, organization_name: str)->List[OrganizationSearchByName]:
        client = await self.get_client()
        app_logger.info(f"ES Client present {client}")
        search_body = {
            "query": {
                "wildcard": {
                    "name": f"*{organization_name}*"
                }
            },
            "_source": ["id", "name"],
            "size": 5,
            "from": 0
        }

        es_response = await client.search(
            index="organizations",
            body=search_body
        )

        organizations = [
            OrganizationSearchByName(
                id=hit["_source"]["id"],
                name=hit["_source"]["name"]
            )
            for hit in es_response["hits"]["hits"]
        ]

        return organizations