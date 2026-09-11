from uuid import UUID

from exceptions.base import AppError


class NotFound(AppError):
    status_code: int = 404

    def __init__(self, entity: str, entity_id: str | UUID) -> None:
        self.entity = entity
        self.entity_id = entity_id
        super().__init__(f'{entity} with id {entity_id} not found.')