"""Common Pydantic models, wrappers, and enums."""

from enum import Enum
from typing import Any, Generic, Optional, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


class ServiceStatus(str, Enum):
    READY = "ready"
    NOT_IMPLEMENTED = "not_implemented"
    ERROR = "error"


class ErrorDetail(BaseModel):
    message: str
    status_code: int
    details: Optional[dict[str, Any]] = None


class APIResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str = "Operation completed successfully"
    data: Optional[T] = None
    error: Optional[ErrorDetail] = None
