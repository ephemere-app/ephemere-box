import json
import uuid

from http import HTTPStatus
from typing import Dict, Generator
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field, UUID4
from redis import Redis

from .settings import Settings


router = APIRouter()


# ------------------------------------------------------------------------------


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


# ------------------------------------------------------------------------------


class BoxCreationSchema(BaseModel):
    content: str = Field(
        ..., title="Box content", description="Content for the box", min_length=1
    )


class BoxCreatedSchema(BaseModel):
    id: UUID4 = Field(..., title="Box ID", description="Unique ID of the box")


class BoxSchema(BaseModel):
    id: UUID4 = Field(..., title="Box ID", description="Unique ID of the box")
    data: BoxCreationSchema = Field(
        ..., title="Box data", description="Box data as object"
    )


def get_db(req: Request) -> Generator[Redis, None, None]:  # pragma: no cover
    settings: Settings = req.app.state.settings
    conn = Redis.from_url(settings.redis_dsn)
    with conn:  # type: ignore
        yield conn


@router.post(
    "/box",
    summary="New box",
    description="Create a new box content",
    response_model=BoxCreatedSchema,
)
def create_box(data: BoxCreationSchema, db: Redis = Depends(get_db)) -> Dict[str, str]:
    box_id = uuid.uuid4()
    db.set(f"box:{box_id}", json.dumps(dict(content=data.content)))
    return dict(id=str(box_id))


@router.get(
    "/box/{box_id}",
    summary="Get box",
    description="Get box content",
    response_model=BoxSchema,
)
def get_box(box_id: uuid.UUID, db: Redis = Depends(get_db)) -> Dict[str, str]:
    box_data = db.get(f"box:{box_id}")
    if box_data is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Box not found")
    return dict(id=str(box_id), data=json.loads(box_data))
