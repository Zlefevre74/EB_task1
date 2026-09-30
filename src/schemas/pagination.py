from pydantic import BaseModel, Field, computed_field
from typing import Generic, TypeVar

T = TypeVar("T")

class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    size: int = Field(10, ge=1, le=100)

    @property
    def offset(self) -> int:
        return (self.page -1) * self.size

class Page(BaseModel, Generic[T]):
    items: list[T]
    page: int
    size: int
    total: int

    @computed_field
    @property
    def total_pages(self) -> int:
        return (self.total + self.size -1) // self.size