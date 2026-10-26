from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID


class PaginationParams(BaseModel):
    last_created_at: datetime | None = None
    last_id: UUID| None = None
    size: int = Field(10, ge=1, le=100)

class Page[T](BaseModel):
    items: list[T]
    size: int
    has_next: bool
