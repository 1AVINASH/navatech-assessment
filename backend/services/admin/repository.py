from typing import List, Self

from infra.postgres.setup import db_cli
from infra.elasticsearch.setup import es_cli

from utility.logger import app_logger
from services.admin.models import Admin as AdminModel


class Admin:
    _es_client = None
    _db = None
    _instance: Self = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Admin, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    async def initialize(self):
        if self._es_client is None:
            self._es_client = await es_cli.get_client()
        if self._db is None:
            self._db = db_cli.db

    async def get_all_admins(self)-> List[AdminModel]:
        query = "SELECT * FROM admin order by created_at"
        
        data = await self._db.fetch_all(query)

        return [AdminModel(**row) for row in data]
    
    async def get_admin_by_email_and_password(self, admin: AdminModel)->AdminModel:
        query = "SELECT * FROM admin where email=:email and password=:password"
        values = {"email": admin.email, "password": admin.password}
        data = await self._db.fetch_one(query, values=values)

        return AdminModel(**data) if data else None
    
    async def create_admin(self, admin: AdminModel)->AdminModel:
        query = "INSERT INTO admin (email, password) VALUES (:email, :password) returning id"
        values = admin.model_dump(exclude_none=True)
        app_logger.debug(f"Query and value for creating admin {values} \n {query}")
        new_admin_id = await self._db.fetch_val(query=query, values=values)
        data = AdminModel(**values)
        data.id = new_admin_id

        return data
    
    async def update_admin(self, admin: AdminModel)->AdminModel:
        query = "UPDATE admin set email=:email, password=:password where id=:id returning id"
        values = admin.model_dump()
        app_logger.debug(f"Query and value for updating admin {values} \n {query}")
        data = await self._db.execute(query=query, values=values)
        if data is None:
            raise ValueError("Admin not found or update failed")
        return admin
    
    async def delete_admin(self, admin_id: int):
        query = "DELETE from admin where id=:id;"
        values = {"id": admin_id}
        data = await self._db.execute(query=query, values=values)

        return data
