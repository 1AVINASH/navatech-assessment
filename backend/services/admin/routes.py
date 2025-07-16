from typing import List, Any

from fastapi import APIRouter, HTTPException, Depends

from utility.logger import app_logger
from utility.authentication import create_access_token, verify_token
from dtos.output import DefaultOutput

from services.admin.models import Admin as AdminModel
from services.admin.dtos.input import CreateAdmin, Login, UpdateAdmin
from services.admin.repository import Admin as RepositoryAdmin

admins_router = APIRouter(prefix="/admins", tags=["admins"])

@admins_router.get("", response_model=DefaultOutput)
async def get():
    data: List[Any] = await RepositoryAdmin.get_all_admins()    
    return DefaultOutput(message=f"admins fetched successfully", data=data)

@admins_router.post("/login", response_model=DefaultOutput)
async def login(payload: Login):
    data = await RepositoryAdmin.get_admin_by_email_and_password(
        AdminModel(
            email=payload.email,
            password=payload.password
        )
    )
    if not data:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token_info = {
        "admin_id": data.id,
        "email": data.email,
    }
    token = create_access_token(data=access_token_info)
    data = data.model_dump()
    data["token"] = token

    return DefaultOutput(message=f"Admin with id fetched successfully", data=data)

@admins_router.post("", response_model=DefaultOutput)
async def create(
    payload: CreateAdmin,
):
    app_logger.info(f"Received payload for creating admin: {payload}")
    data = await RepositoryAdmin.create_admin(
        AdminModel(
            email=payload.email,
            password=payload.password
        )
    )
    return DefaultOutput(message=f"Admin Created successfully", data=data)

@admins_router.put("/{admin_id}", response_model=DefaultOutput)
async def update(
    admin_id: int, 
    payload: UpdateAdmin,
    token_payload: dict = Depends(verify_token)
):
    app_logger.info(f"Received payload for updating admin: {payload}")
    _ = await RepositoryAdmin.update_admin(
        AdminModel(
            id=admin_id,
            email=payload.email,
            password=payload.password
        )
    )
    return DefaultOutput(message=f"Admin Updated successfully", data=payload)

@admins_router.delete("/{admin_id}", response_model=DefaultOutput)
async def delete(admin_id: int):
    app_logger.info(f"Deleting Admin for id {admin_id}")
    data = await RepositoryAdmin.delete_admin(admin_id=admin_id)
    return DefaultOutput(message=f"Admin Deleted successfully", data={"id": admin_id})
