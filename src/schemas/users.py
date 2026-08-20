from pydantic import BaseModel, ConfigDict, field_validator
from datetime import date

import uuid


class UserBase(BaseModel):
    username: str
    email: str
    birth_date: date

    @field_validator('birth_date')
    @classmethod
    def validate_birth_date(cls, v):
        if v > date.today():
            raise ValueError('Birth date must not be in the future')
        return v

    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        if len(v) < 3 or len(v) > 35:
            raise ValueError('Username must be between 3 and 35 characters long')
        return v


class User(UserBase):
    id: uuid.UUID
    is_locked: bool

    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    username: str | None = None
    email: str | None = None
    birth_date: date | None = None


