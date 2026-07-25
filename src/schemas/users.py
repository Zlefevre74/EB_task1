from pydantic import BaseModel, ConfigDict

import uuid


class UserAdd(BaseModel):
    username: str

class User(UserAdd):
    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)
