from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class StandardResponse(BaseModel, Generic[T]):
    success: bool
    data: T | None = None
    error: dict[str, str] | None = None


class APIErrorSchema(BaseModel):
    code: str
    message: str
