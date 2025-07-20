import pickle
from typing import List, Self

from fastapi import HTTPException, status
from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError

from infra.postgres.setup import db_cli
from infra.elasticsearch.setup import es_cli
from infra.redis.setup import redis_service

from utility.logger import app_logger
from services.organization.dtos.input import CreateOrganization, UpdateOrganization
from services.organization.dtos.custom_types import OrganizationName
from services.organization.models import Organization as OrganizationModel, OrganizationSearchByName


class Organization:
    _es_client = None
    _db = None
    _cache = None
    _instance: Self = None
    BLOOM_REDIS_ORG_NAME_KEY = "bloom:org_name"


    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Organization, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    async def initialize(self):
        if self._es_client is None:
            self._es_client = await es_cli.get_client()
        if self._db is None:
            self._db = db_cli.db
        if self._cache is None:
            self._cache = redis_service.redis

    async def get_all_organizations(self)-> List[OrganizationModel]:
        query = "SELECT * FROM organization order by created_at"
        app_logger.debug(f"Db Url from inside organization {self._db.url}") 
        data = await self._db.fetch_all(query)

        return [OrganizationModel(**row) for row in data]
    
    async def get_organization_by_name(self, organization_name: OrganizationName)->OrganizationModel:
        query = "SELECT * FROM organization where name=:name"
        values = {"name": organization_name}
        data = await self._db.fetch_one(query, values=values)

        return OrganizationModel(**data) if data else None
    
    async def create_organization(self, organization: CreateOrganization)->OrganizationModel:
        query = "INSERT INTO organization (name, admin_id) VALUES (:name, :admin_id) returning id"
        values = organization.model_dump()
        try:
            new_organization_id = await self._db.fetch_val(query=query, values=values)
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
    
    async def update_organization(self, organization: UpdateOrganization):
        query = "UPDATE organization set name=:name where id=:id"
        values = organization.model_dump()
        app_logger.debug(f"Query and value for updating organization {values} \n {query}")
        data = await self._db.execute(query=query, values=values)

        return data
    
    async def delete_organization(self, organization_id: int):
        query = "DELETE from organization where id=:id;"
        values = {"id": organization_id}
        data = await self._db.execute(query=query, values=values)

        return data
    

    # Elastic Search Queries start from here
    async def search_organization_by_name(self, organization_name: str)->List[OrganizationSearchByName]:
        app_logger.info(f"ES Client present {self._es_client}")
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

        es_response = await self._es_client.search(
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
    
    async def set_org_name_filter_in_cache(self, org_name_filter):
        await self._cache.set(self.BLOOM_REDIS_ORG_NAME_KEY, pickle.dumps(org_name_filter))

        return {"message": "Value set"}
    
    async def get_org_name_filter_in_cache(self):
        data_pickle = await self._cache.get(self.BLOOM_REDIS_ORG_NAME_KEY)
        data = pickle.loads(data_pickle) if data_pickle else None

        return data