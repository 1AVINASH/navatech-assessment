import os
from typing import List, Any

from fastapi import APIRouter, Depends

from infra.elasticsearch.setup import get_es_client
from utility.logger import app_logger
from utility.authentication import verify_token
from dtos.output import DefaultOutput

from services.organization.models import Organization
from services.organization.dtos.input import CreateOrganization, UpdateOrganization
from services.organization.dtos.custom_types import OrganizationName
from services.organization.repository import Organization as OrganizationRepository

organizations_router = APIRouter(prefix="/organizations", tags=["organizations"])

organization_repository = OrganizationRepository()

@organizations_router.get("", response_model=DefaultOutput)
async def get(
    token_payload: dict = Depends(verify_token)
):
    data: List[Any] = await organization_repository.get_all_organizations()    
    return DefaultOutput(message=f"All organizations fetched successfully", data=data)

@organizations_router.get("/by-name/{organization_name}", response_model=DefaultOutput)
async def get(
    organization_name: OrganizationName,
    token_payload: dict = Depends(verify_token)
):
    try:
        data = await organization_repository.get_organization_by_name(organization_name=organization_name)
    except Exception as e:
        app_logger.error(f"Error fetching organization by name: {e}")
        return DefaultOutput(message=str(e), data=None, success=False)
    return DefaultOutput(message=f"Organization with name fetched successfully", data=data)

@organizations_router.get("/search/by-name/{organization_name}", response_model=DefaultOutput)
async def search_by_name(
    organization_name: OrganizationName,
    # token_payload: dict = Depends(verify_token)
):
    try:
        data = await organization_repository.search_organization_by_name(organization_name=organization_name)
    except Exception as e:
        app_logger.error(f"Error fetching organization by name: {e}")
        return DefaultOutput(message=str(e), data=None, success=False)
    return DefaultOutput(message=f"Organization with name fetched successfully", data=data)

@organizations_router.post("", response_model=DefaultOutput)
async def create(
    payload: CreateOrganization,
    token_payload: dict = Depends(verify_token)
):
    app_logger.info(f"Received payload for creating organization: {payload}")
    print(f"Token payload: {token_payload}")
    try:
        payload.admin_id = token_payload.get("admin_id")  # Ensure admin_id is set from token
        data = await organization_repository.create_organization(payload)
    except Exception as e:
        app_logger.error(f"Error creating organization: {e}")
        return DefaultOutput(message=str(e), data=None, success=False)
    return DefaultOutput(message=f"Organization Created successfully", data=data)

@organizations_router.put("/{organization_id}", response_model=DefaultOutput)
async def update(
    payload: UpdateOrganization,
    token_payload: dict = Depends(verify_token)
):
    app_logger.info(f"Received payload for updating organization: {payload}")
    try:
        _ = await organization_repository.update_organization(payload)
    except Exception as e:
        app_logger.error(f"Error updating organization: {e}")
    return DefaultOutput(message=f"Organization Updated successfully", data=payload)

@organizations_router.delete("/{organization_id}", response_model=DefaultOutput)
async def delete(
    organization_id: int,
    token_payload: dict = Depends(verify_token)
):
    '''
        Ideally this route would have safety checks to ensure that the organization is being deleted only by an admin or the owner
    '''
    app_logger.info(f"Deleting organization for id {organization_id}")
    await organization_repository.delete_organization(organization_id=organization_id)
    return DefaultOutput(message=f"Organization Deleted successfully", data={"id": organization_id})
