from typing import Dict
from fastapi import APIRouter, Request
from pydantic import BaseModel, Field

from .settings import Settings


router = APIRouter()


class ApiInfoSchema(BaseModel):
    title: str = Field(..., title="Title", description="Title of the API")
    description: str = Field(
        ..., title="Description", description="Description of the API"
    )
    version: str = Field(..., title="Version", description="Version of the API")


@router.get(
    "/",
    summary="Information",
    description="Get API information",
    response_model=ApiInfoSchema,
)
def get_api_info(req: Request) -> Dict[str, str]:
    settings: Settings = req.app.state.settings
    data = {
        "title": settings.app_title,
        "description": settings.app_description,
        "version": settings.app_version,
    }

    return data
