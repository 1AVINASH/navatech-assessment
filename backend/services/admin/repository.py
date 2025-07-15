from typing import List

from infra.postgres.setup import db

from utility.logger import app_logger
from services.admin.models import Admin as AdminModel


class Admin:
    @staticmethod
    async def get_all_admins()-> List[AdminModel]:
        query = "SELECT * FROM admin order by created_at"
        
        data = await db.fetch_all(query)

        return [AdminModel(**row) for row in data]
    
    @staticmethod
    async def get_admin_by_email_and_password(admin: AdminModel)->AdminModel:
        query = "SELECT * FROM admin where email=:email and password=:password"
        values = {"email": admin.email, "password": admin.password}
        data = await db.fetch_one(query, values=values)

        return AdminModel(**data) if data else None
    
    @staticmethod
    async def create_admin(admin: AdminModel)->AdminModel:
        query = "INSERT INTO admin (email, password) VALUES (:email, :password) returning id"
        values = admin.model_dump(exclude_none=True)
        app_logger.debug(f"Query and value for creating admin {values} \n {query}")
        new_admin_id = await db.fetch_val(query=query, values=values)
        data = AdminModel(**values)
        data.id = new_admin_id

        return data
    
    @staticmethod
    async def update_admin(admin: AdminModel)->AdminModel:
        query = "UPDATE admin set email=:email, password=:password where id=:id returning id"
        values = admin.model_dump()
        app_logger.debug(f"Query and value for updating admin {values} \n {query}")
        data = await db.execute(query=query, values=values)
        if data is None:
            raise ValueError("Admin not found or update failed")
        return admin
    
    @staticmethod
    async def delete_admin(admin_id: int):
        query = "DELETE from admin where id=:id;"
        values = {"id": admin_id}
        data = await db.execute(query=query, values=values)

        return data
    