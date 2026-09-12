from pydantic import BaseModel, ConfigDict, field_validator, ValidationInfo, EmailStr, model_validator
from datetime import date

import uuid

from exceptions import InvalidField, EmptyPayload
from typing import Self, Any


class UserBase(BaseModel):
    username: str
    email: EmailStr
    birth_date: date

    @field_validator('username','birth_date','email')
    @classmethod
    def reject_null(cls, v: Any, info: ValidationInfo) -> Any:
        if v is None:
            raise InvalidField(info.field_name,'must not be null')
        return v


    @field_validator('birth_date')
    @classmethod
    def validate_birth_date(cls, v: date) -> date:
        if v > date.today():
            raise InvalidField('birth_date','must not be in the future')

        return v

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        if len(v) < 3 or len(v) > 35:
            raise InvalidField('username','must be between 3 and 35 characters long')
        return v


class User(UserBase):
    id: uuid.UUID
    is_locked: bool

    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    username: str | None = None
    email: EmailStr | None = None
    birth_date: date | None = None

    @model_validator(mode='after')
    def reject_empty_payload(self) -> Self:
        if not self.model_fields_set:
            raise EmptyPayload()
        return self


